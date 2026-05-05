from typing import Any, Dict


def list_ads(api, args: Dict[str, Any]) -> dict:
    return api.list_ads(args["campaign_id"], args.get("limit", 25))


def list_adsets(api, args: Dict[str, Any]) -> dict:
    return api.list_adsets(args["campaign_id"], args.get("limit", 25))


def create_ad(api, args: Dict[str, Any]) -> dict:
    return api.create_ad(
        adset_id=args["adset_id"],
        creative_id=args["creative_id"],
        name=args["name"],
        status=args.get("status", "PAUSED"),
    )


def pause_ad(api, args: Dict[str, Any]) -> dict:
    return api.update_status(args["ad_id"], "PAUSED")
