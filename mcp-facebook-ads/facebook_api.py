import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional

import requests


class FacebookApiError(Exception):
    """Raised when the Meta Graph API returns an error response."""

    def __init__(self, message: str, status_code: Optional[int] = None, payload: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}


class FacebookAdsApi:
    def __init__(
        self,
        access_token: str,
        ad_account_id: Optional[str] = None,
        api_version: Optional[str] = None,
        timeout: int = 30,
    ):
        if not access_token:
            raise ValueError("FB_ACCESS_TOKEN or META_ACCESS_TOKEN is required")

        self.access_token = access_token
        self.ad_account_id = self._normalize_ad_account_id(ad_account_id)
        self.api_version = api_version or os.getenv("FB_API_VERSION", "v21.0")
        self.timeout = timeout
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    @staticmethod
    def _normalize_ad_account_id(ad_account_id: Optional[str]) -> Optional[str]:
        if not ad_account_id:
            return None
        ad_account_id = str(ad_account_id).strip()
        return ad_account_id if ad_account_id.startswith("act_") else f"act_{ad_account_id}"

    def account_id(self, override: Optional[str] = None) -> str:
        account_id = self._normalize_ad_account_id(override) or self.ad_account_id
        if not account_id:
            raise FacebookApiError("An ad account ID is required. Set FB_AD_ACCOUNT_ID or pass ad_account_id.")
        return account_id

    def request(self, method: str, path: str, params: Optional[dict] = None, data: Optional[dict] = None) -> dict:
        url = path if path.startswith("https://") else f"{self.base_url}/{path.lstrip('/')}"
        params = self._clean(params or {})
        data = self._clean(data or {})

        last_error: Optional[FacebookApiError] = None
        for attempt in range(3):
            try:
                response = self.session.request(
                    method.upper(),
                    url,
                    params=params,
                    data=data if method.upper() != "GET" else None,
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                last_error = FacebookApiError(f"Network error calling Meta API: {exc}")
                time.sleep(0.5 * (attempt + 1))
                continue

            payload = self._parse_json(response)
            if response.status_code < 400 and "error" not in payload:
                return payload

            message = self._error_message(payload, response.status_code)
            last_error = FacebookApiError(message, response.status_code, payload)
            if response.status_code in {429, 500, 502, 503, 504}:
                time.sleep(0.75 * (attempt + 1))
                continue
            break

        raise last_error or FacebookApiError("Unknown Meta API error")

    def paginate(self, path: str, params: Optional[dict] = None, limit: int = 25) -> dict:
        params = dict(params or {})
        limit = max(1, min(int(limit or 25), 100))
        params["limit"] = limit
        payload = self.request("GET", path, params=params)
        return {
            "data": payload.get("data", []),
            "paging": payload.get("paging", {}),
            "next_cursor": self._next_cursor(payload),
        }

    def get_ad_accounts(self, limit: int = 25) -> dict:
        return self.paginate(
            "/me/adaccounts",
            {
                "fields": "id,account_id,name,account_status,currency,timezone_name,business",
            },
            limit,
        )

    def list_campaigns(self, ad_account_id: Optional[str] = None, limit: int = 25) -> dict:
        account = self.account_id(ad_account_id)
        return self.paginate(
            f"/{account}/campaigns",
            {
                "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,"
                "created_time,updated_time,start_time,stop_time",
            },
            limit,
        )

    def list_adsets(self, campaign_id: str, limit: int = 25) -> dict:
        return self.paginate(
            f"/{campaign_id}/adsets",
            {
                "fields": "id,name,status,effective_status,campaign_id,daily_budget,lifetime_budget,"
                "billing_event,optimization_goal,start_time,end_time",
            },
            limit,
        )

    def list_ads(self, campaign_id: str, limit: int = 25) -> dict:
        return self.paginate(
            f"/{campaign_id}/ads",
            {
                "fields": "id,name,status,effective_status,campaign_id,adset_id,creative,"
                "created_time,updated_time",
            },
            limit,
        )

    def get_insights(
        self,
        object_id: str,
        date_preset: str = "last_7d",
        fields: Optional[Iterable[str]] = None,
        time_increment: Optional[str] = None,
        limit: int = 25,
    ) -> dict:
        params: Dict[str, Any] = {
            "date_preset": date_preset,
            "fields": ",".join(fields or DEFAULT_INSIGHT_FIELDS),
        }
        if time_increment:
            params["time_increment"] = time_increment
        return self.paginate(f"/{object_id}/insights", params, limit)

    def create_campaign(
        self,
        name: str,
        objective: str,
        status: str = "PAUSED",
        ad_account_id: Optional[str] = None,
        special_ad_categories: Optional[List[str]] = None,
        daily_budget: Optional[int] = None,
        lifetime_budget: Optional[int] = None,
        **extra: Any,
    ) -> dict:
        account = self.account_id(ad_account_id)
        data: Dict[str, Any] = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": special_ad_categories or [],
        }
        if daily_budget is not None:
            data["daily_budget"] = int(daily_budget)
        if lifetime_budget is not None:
            data["lifetime_budget"] = int(lifetime_budget)
        data.update(extra)
        return self.request("POST", f"/{account}/campaigns", data=data)

    def create_ad(self, adset_id: str, creative_id: str, name: str, status: str = "PAUSED") -> dict:
        return self.request(
            "POST",
            f"/{self.account_id()}/ads",
            data={
                "name": name,
                "adset_id": adset_id,
                "creative": {"creative_id": creative_id},
                "status": status,
            },
        )

    def update_status(self, object_id: str, status: str) -> dict:
        return self.request("POST", f"/{object_id}", data={"status": status})

    @staticmethod
    def _clean(values: dict) -> dict:
        cleaned = {}
        for key, value in values.items():
            if value is None:
                continue
            if isinstance(value, (dict, list)):
                cleaned[key] = json.dumps(value)
            else:
                cleaned[key] = value
        return cleaned

    @staticmethod
    def _parse_json(response: requests.Response) -> dict:
        try:
            return response.json()
        except ValueError:
            return {"error": {"message": response.text or "Non-JSON response from Meta API"}}

    @staticmethod
    def _error_message(payload: dict, status_code: int) -> str:
        error = payload.get("error") or {}
        message = error.get("message") or payload.get("message") or "Meta API request failed"
        code = error.get("code")
        subcode = error.get("error_subcode")
        parts = [f"HTTP {status_code}", str(message)]
        if code:
            parts.append(f"code={code}")
        if subcode:
            parts.append(f"subcode={subcode}")
        return " | ".join(parts)

    @staticmethod
    def _next_cursor(payload: dict) -> Optional[str]:
        cursors = payload.get("paging", {}).get("cursors", {})
        return cursors.get("after")


DEFAULT_INSIGHT_FIELDS = [
    "account_id",
    "campaign_id",
    "campaign_name",
    "adset_id",
    "adset_name",
    "ad_id",
    "ad_name",
    "spend",
    "impressions",
    "reach",
    "clicks",
    "ctr",
    "cpc",
    "cpm",
    "actions",
    "purchase_roas",
]
