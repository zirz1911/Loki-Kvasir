# Facebook Ads MCP Server

Model Context Protocol (MCP) server for Meta Marketing API automation. Provides programmatic access to Facebook/Instagram ad campaigns, accounts, and performance insights.

## Features

- **Campaign Management**: List, create, pause campaigns
- **Ad Operations**: Create and manage ads within ad sets
- **Ad Sets**: List and manage ad set configurations
- **Performance Insights**: Campaign, account, and ad-level metrics
- **Account Discovery**: List all Meta ad accounts accessible to token

## Setup

### Requirements
- Python 3.8+
- `requests` library
- Valid Meta Access Token with ads management permissions

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Set environment variables:

```bash
export FB_ACCESS_TOKEN="your_meta_access_token"        # Required
export FB_AD_ACCOUNT_ID="your_ad_account_id"           # Optional (can override per request)
export FB_API_VERSION="v21.0"                          # Default v21.0
export FB_MCP_DEBUG="1"                                # Debug mode (optional)
```

Or use Meta's environment variables:
```bash
export META_ACCESS_TOKEN="..."
export META_AD_ACCOUNT_ID="..."
```

## Running

### Standalone (stdio)
```bash
python3 server.py
```

### With pm2
```bash
pm2 start ecosystem.config.js
pm2 logs facebook-ads
```

### With Claude Code
Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "facebook-ads": {
      "command": "python3",
      "args": ["/path/to/mcp-facebook-ads/server.py"],
      "env": {
        "FB_ACCESS_TOKEN": "your_token",
        "FB_AD_ACCOUNT_ID": "your_account_id"
      }
    }
  }
}
```

## Available Tools

All tools conform to MCP 2024-11-05 protocol.

### Accounts
- `list_ad_accounts` — List Meta ad accounts

### Campaigns
- `list_campaigns` — List campaigns for ad account
- `create_campaign` — Create new campaign (defaults to PAUSED)
- `pause_campaign` — Pause an active campaign
- `get_campaign_insights` — Campaign metrics (impressions, clicks, spend)
- `get_campaign_performance` — Time-series campaign metrics

### Ad Sets
- `list_adsets` — List ad sets in campaign

### Ads
- `list_ads` — List ads in campaign
- `create_ad` — Create ad from existing creative (defaults to PAUSED)
- `pause_ad` — Pause an active ad

### Insights
- `get_account_insights` — Account-level metrics
- `get_top_performing_ads` — Ads sorted by metric (CTR, CPC, spend, etc.)

## Error Handling

API errors return with status code and Meta API payload:
```json
{
  "ok": false,
  "error": "Campaign not found",
  "details": {
    "status_code": 400,
    "payload": { "error": { "message": "..." } }
  }
}
```

## Security Notes

- Token stored in environment variables only, never logged
- All campaigns created default to PAUSED status for safety
- Debug mode (FB_MCP_DEBUG) logs API calls to stderr only
- Private repo — credentials should not be committed

## Architecture

- `server.py` — MCP protocol handler, tool definitions
- `facebook_api.py` — Meta Graph API wrapper, request handling
- `tools/` — Individual tool implementations
  - `campaigns.py` — Campaign operations
  - `ads.py` — Ad operations
  - `adsets.py` — Ad set operations
  - `insights.py` — Performance metrics

## Meta API Reference

- [Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [Marketing API Campaigns](https://developers.facebook.com/docs/marketing-api/reference/campaign)
- [Marketing API Insights](https://developers.facebook.com/docs/marketing-api/insights)

## License

Private repo. Internal use only.
