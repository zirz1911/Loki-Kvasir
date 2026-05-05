#!/usr/bin/env python3
"""
MCP Server - Facebook Ads

Private stdio MCP server for Meta Marketing API automation.
Reads token from FB_ACCESS_TOKEN or META_ACCESS_TOKEN.
"""

import json
import os
import sys
import traceback
from typing import Any, Callable, Dict, Optional

from facebook_api import FacebookAdsApi, FacebookApiError
from tools import TOOL_HANDLERS


SERVER_NAME = "facebook-ads"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"


def tool_definitions() -> list:
    common_limit = {
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "description": "Maximum records to return. Default 25, max 100.",
        }
    }
    return [
        {
            "name": "list_ad_accounts",
            "description": "List Meta ad accounts available to the token.",
            "inputSchema": {"type": "object", "properties": common_limit},
        },
        {
            "name": "list_campaigns",
            "description": "List campaigns for the configured or provided ad account.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ad_account_id": {"type": "string", "description": "Optional ad account ID, with or without act_."},
                    **common_limit,
                },
            },
        },
        {
            "name": "create_campaign",
            "description": "Create a Meta campaign. Defaults to PAUSED status for safety.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "objective": {"type": "string", "description": "Meta campaign objective, such as OUTCOME_TRAFFIC."},
                    "status": {"type": "string", "enum": ["PAUSED", "ACTIVE"], "default": "PAUSED"},
                    "daily_budget": {"type": "integer", "description": "Budget in minor currency units, e.g. cents."},
                    "lifetime_budget": {"type": "integer", "description": "Budget in minor currency units, e.g. cents."},
                    "special_ad_categories": {"type": "array", "items": {"type": "string"}},
                    "ad_account_id": {"type": "string"},
                },
                "required": ["name", "objective"],
            },
        },
        {
            "name": "pause_campaign",
            "description": "Pause an existing campaign by campaign ID.",
            "inputSchema": {
                "type": "object",
                "properties": {"campaign_id": {"type": "string"}},
                "required": ["campaign_id"],
            },
        },
        {
            "name": "get_campaign_insights",
            "description": "Get campaign insight metrics.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "campaign_id": {"type": "string"},
                    "date_preset": {"type": "string", "default": "last_7d"},
                    "time_increment": {"type": "string", "description": "Use 1 for daily rows."},
                    **common_limit,
                },
                "required": ["campaign_id"],
            },
        },
        {
            "name": "list_ads",
            "description": "List ads in a campaign.",
            "inputSchema": {
                "type": "object",
                "properties": {"campaign_id": {"type": "string"}, **common_limit},
                "required": ["campaign_id"],
            },
        },
        {
            "name": "list_adsets",
            "description": "List ad sets in a campaign.",
            "inputSchema": {
                "type": "object",
                "properties": {"campaign_id": {"type": "string"}, **common_limit},
                "required": ["campaign_id"],
            },
        },
        {
            "name": "create_ad",
            "description": "Create an ad from an existing ad set and creative. Defaults to PAUSED status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "adset_id": {"type": "string"},
                    "creative_id": {"type": "string"},
                    "name": {"type": "string"},
                    "status": {"type": "string", "enum": ["PAUSED", "ACTIVE"], "default": "PAUSED"},
                },
                "required": ["adset_id", "creative_id", "name"],
            },
        },
        {
            "name": "pause_ad",
            "description": "Pause an ad by ad ID.",
            "inputSchema": {
                "type": "object",
                "properties": {"ad_id": {"type": "string"}},
                "required": ["ad_id"],
            },
        },
        {
            "name": "get_account_insights",
            "description": "Get insight metrics for the configured or provided ad account.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ad_account_id": {"type": "string"},
                    "date_preset": {"type": "string", "default": "last_7d"},
                    "time_increment": {"type": "string"},
                    **common_limit,
                },
            },
        },
        {
            "name": "get_campaign_performance",
            "description": "Get time-series campaign performance metrics.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "campaign_id": {"type": "string"},
                    "date_preset": {"type": "string", "default": "last_30d"},
                    "time_increment": {"type": "string", "default": "1"},
                    **common_limit,
                },
                "required": ["campaign_id"],
            },
        },
        {
            "name": "get_top_performing_ads",
            "description": "Return ad insights sorted by a metric such as ctr, cpc, spend, or clicks.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ad_account_id": {"type": "string"},
                    "date_preset": {"type": "string", "default": "last_30d"},
                    "sort_by": {"type": "string", "default": "ctr"},
                    **common_limit,
                },
            },
        },
    ]


def initialize_api() -> FacebookAdsApi:
    token = os.getenv("FB_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN")
    account_id = os.getenv("FB_AD_ACCOUNT_ID") or os.getenv("META_AD_ACCOUNT_ID")
    return FacebookAdsApi(token or "", account_id)


def ok(data: Any) -> dict:
    return {"content": [{"type": "text", "text": json.dumps({"ok": True, "data": data}, indent=2)}]}


def tool_error(message: str, details: Optional[dict] = None) -> dict:
    payload = {"ok": False, "error": message}
    if details:
        payload["details"] = details
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}], "isError": True}


def handle_list_tools() -> dict:
    return {"tools": tool_definitions()}


def handle_call_tool(api_factory: Callable[[], FacebookAdsApi], name: str, arguments: Optional[dict]) -> dict:
    if name not in TOOL_HANDLERS:
        return tool_error(f"Unknown tool: {name}")
    args = arguments or {}
    try:
        api = api_factory()
        result = TOOL_HANDLERS[name](api, args)
        return ok(result)
    except FacebookApiError as exc:
        return tool_error(str(exc), {"status_code": exc.status_code, "payload": exc.payload})
    except KeyError as exc:
        return tool_error(f"Missing required argument: {exc.args[0]}")
    except Exception as exc:
        return tool_error(str(exc))


def make_response(request_id: Any, result: Optional[dict] = None, error: Optional[dict] = None) -> dict:
    response = {"jsonrpc": "2.0", "id": request_id}
    if error:
        response["error"] = error
    else:
        response["result"] = result or {}
    return response


def handle_request(request: dict) -> Optional[dict]:
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    if method == "notifications/initialized":
        return None
    if method == "initialize":
        return make_response(
            request_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )
    if method == "tools/list":
        return make_response(request_id, handle_list_tools())
    if method == "tools/call":
        return make_response(
            request_id,
            handle_call_tool(initialize_api, params.get("name", ""), params.get("arguments", {})),
        )

    return make_response(request_id, error={"code": -32601, "message": f"Unknown method: {method}"})


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        request_id = None
        try:
            request = json.loads(line)
            request_id = request.get("id")
            response = handle_request(request)
            if response is not None:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError as exc:
            print(json.dumps(make_response(request_id, error={"code": -32700, "message": str(exc)})), flush=True)
        except Exception as exc:
            if os.getenv("FB_MCP_DEBUG"):
                traceback.print_exc(file=sys.stderr)
            print(json.dumps(make_response(request_id, error={"code": -32603, "message": str(exc)})), flush=True)


if __name__ == "__main__":
    main()
