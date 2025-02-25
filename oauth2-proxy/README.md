# OAuth2 reverse proxy

I find [OAuth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) the best way to restrict access to web apps using email IDs.
This is typically needed in organizations using Google or Microsoft accounts.

It [works with](https://oauth2-proxy.github.io/oauth2-proxy/configuration/integration) Nginx, Traefik, and Caddy.
Caddy is the easiest to setup.

## Setup

- [Download oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy/releases). Pick the latest binary for your OS.
- [Download Caddyfile](https://github.com/caddyserver/caddy/releases). Pick the latest binary for your OS.
- Ensure your app is running. E.g. `caddy file-server --listen :3000` will serve a test backend at `http://localhost:3000`.
- Modify the [Caddyfile](Caddyfile). $SITE_ADDRESS will proxy to $UPSTREAM with restricted access.
  - $SITE_ADDR: Where you host your app. E.g. `app.example.com`, `http://localhost:9988`.
  - $OAUTH_PROXY_HTTP_ADDRESS: Where you host oauth2-proxy. Use `localhost:4180`. But if you host OAuth2-proxy on a different server/port, use that.
  - $BACKEND_ADDR: App to restrict access to. E.g. `localhost:3000`.
- Run `caddy run --config Caddyfile`
- Register your app at:
  - [Google](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/google#usage)
  - [Microsoft](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/ms_entra_id#configure-app-registration)
  - [Others](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/)
- Modify the [oauth2-proxy.cfg](oauth2-proxy.cfg).
  - `http_address`: Use `localhost:4180`. But if you host OAuth2-proxy on a different server/port, use that.
  - `redirect_url`: Use `$SITE_ADDR/oauth2/callback`. This is the OAuth Redirect URL.
  - `upstreams`: Use `$SITE_ADDR`.
  - `email_domains`: Restrict access to specific email domains. E.g. `gramener.com`.
  - `client_id` and `client_secret`: From the app registration.
  - `cookie_secret`: A random string. See [Generating a Cookie Secret](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview#generating-a-cookie-secret).
- Run `oauth2-proxy --config oauth2-proxy.cfg`

## Usage

- Visit `$SITE_ADDR`. You should be redirected to Google/Microsoft to login.
- After login, you should be redirected back to `$SITE_ADDR`.
- This will show exactly with `$BACKEND_ADDR` shows if you log in as a valid user.
- Visit [other endpoints](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints), e.g.:
  - `/oauth2/sign_out` to log out the user.
  - `oauth2/userinfo` gets the user info as JSON. Useful for the backend app to get user details.
