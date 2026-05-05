from .ads import create_ad, list_ads, list_adsets, pause_ad
from .campaigns import create_campaign, get_campaign_insights, list_campaigns, pause_campaign
from .insights import get_account_insights, get_campaign_performance, get_top_performing_ads


TOOL_HANDLERS = {
    "list_ad_accounts": lambda api, args: api.get_ad_accounts(args.get("limit", 25)),
    "list_campaigns": list_campaigns,
    "create_campaign": create_campaign,
    "pause_campaign": pause_campaign,
    "get_campaign_insights": get_campaign_insights,
    "list_ads": list_ads,
    "list_adsets": list_adsets,
    "create_ad": create_ad,
    "pause_ad": pause_ad,
    "get_account_insights": get_account_insights,
    "get_campaign_performance": get_campaign_performance,
    "get_top_performing_ads": get_top_performing_ads,
}
