module.exports = {
  apps: [
    {
      name: 'facebook-ads',
      script: 'server.py',
      interpreter: 'python3',
      cwd: '/home/paji/Loki-Kvasir/mcp-facebook-ads',
      env: {
        FB_ACCESS_TOKEN: '',
        FB_AD_ACCOUNT_ID: '',
        FB_API_VERSION: 'v21.0',
        FB_MCP_DEBUG: '0',
      },
      error_file: './logs/error.log',
      out_file: './logs/out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
    },
  ],
};
