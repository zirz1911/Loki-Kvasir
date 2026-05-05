from typing import Any, Dict


def list_campaigns(api, args: Dict[str, Any]) -> dict:
    return api.list_campaigns(args.get("ad_account_id"), args.get("limit", 25))


def create_campaign(api, args: Dict[str, Any]) -> dict:
    objective = args.get("objective") or args.get("campaign_objective")
    if not objective:
        raise ValueError("objective is required")
    return api.create_campaign(
        name=args["name"],
        objective=objective,
        status=args.get("status", "PAUSED"),
        ad_account_id=args.get("ad_account_id"),
        special_ad_categories=args.get("special_ad_categories"),
        daily_budget=args.get("daily_budget") or args.get("budget"),
        lifetime_budget=args.get("lifetime_budget"),
        buying_type=args.get("buying_type"),
    )


def pause_campaign(api, args: Dict[str, Any]) -> dict:
    return api.update_status(args["campaign_id"], "PAUSED")


def get_campaign_insights(api, args: Dict[str, Any]) -> dict:
    return api.get_insights(
        args["campaign_id"],
        date_preset=args.get("date_preset", "last_7d"),
        time_increment=args.get("time_increment"),
        limit=args.get("limit", 25),
    )
