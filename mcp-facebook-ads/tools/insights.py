from typing import Any, Dict


def get_account_insights(api, args: Dict[str, Any]) -> dict:
    account = api.account_id(args.get("ad_account_id"))
    return api.get_insights(
        account,
        date_preset=args.get("date_preset", "last_7d"),
        time_increment=args.get("time_increment"),
        limit=args.get("limit", 25),
    )


def get_campaign_performance(api, args: Dict[str, Any]) -> dict:
    return api.get_insights(
        args["campaign_id"],
        date_preset=args.get("date_preset", "last_30d"),
        time_increment=args.get("time_increment", "1"),
        limit=args.get("limit", 100),
    )


def get_top_performing_ads(api, args: Dict[str, Any]) -> dict:
    account = api.account_id(args.get("ad_account_id"))
    payload = api.get_insights(
        account,
        date_preset=args.get("date_preset", "last_30d"),
        fields=[
            "ad_id",
            "ad_name",
            "campaign_id",
            "campaign_name",
            "spend",
            "impressions",
            "clicks",
            "ctr",
            "cpc",
            "purchase_roas",
            "actions",
        ],
        limit=args.get("limit", 25),
    )
    sort_by = args.get("sort_by", "ctr")
    reverse = sort_by not in {"cpc", "spend"}
    payload["data"] = sorted(payload.get("data", []), key=lambda row: _numeric(row.get(sort_by)), reverse=reverse)
    return payload


def _numeric(value) -> float:
    if isinstance(value, list):
        if not value:
            return 0.0
        value = value[0].get("value", 0)
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
