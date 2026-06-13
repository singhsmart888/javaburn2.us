# Agent Context — New Cloudflare Pages Site

> **NOTE TO USER:** Copy this folder to your new project directory, then update the `PROJECT IDENTITY` section below with your actual domain/repo. If you leave it as-is, the agent will try to auto-detect from the folder name.

## Auto-Detect Rules (Agent Must Follow)
- **Work Directory:** Use the current working directory path.
- **Domain:** If the folder name looks like a domain (contains a dot and a TLD, e.g. `example.com`), use it as the domain. Otherwise ask the user.
- **GitHub User:** `singhsmart888` (default from template). Override if the repo is under a different account/org.
- **GitHub Repo:** `singhsmart888/{domain-with-dots-replaced-by-hyphens}`
  - Example: `example.com` → `singhsmart888/example-com`
  - Example: `sub.example.com` → `singhsmart888/sub-example-com`
- **Cloudflare Pages Project:** Same as the repo slug above (lowercase, hyphens, max 28 chars trimmed).

## Project Identity (Update after copying)
- **Name:** {YOUR_SITE_NAME}
- **Domain:** https://{YOUR_DOMAIN}
- **Local Work Directory:** `{CURRENT_WORKING_DIRECTORY}`
- **GitHub Repo:** https://github.com/{GITHUB_USER}/{REPO_SLUG}
- **Cloudflare Pages Project:** `{REPO_SLUG}`
- **Primary Branch:** `main`

## Affiliate / Bridge Page (if applicable)
- **CTA Destination:** `https://{YOUR_DOMAIN}/order/`
- **Redirect Target:** `{YOUR_AFFILIATE_LINK}`
- All CTA buttons should point to the internal `/order/` bridge page so the raw affiliate URL is not visible to users.

## Deployment
- Push to `main` on GitHub → Cloudflare Pages auto-deploys via `.github/workflows/deploy.yml`.
- `cf-pages-setup.ps1` is a one-time local setup script (contains credentials, do NOT push).
- Required GitHub Secrets are set by `cf-pages-setup.ps1`:
  - `CF_EMAIL`
  - `CF_GLOBAL_KEY`
  - `CF_ACCOUNT_ID`
  - `CF_PROJECT_NAME`

## Project Structure
- Static HTML site (no framework, no build step).
- Root pages: `index.html`, plus any additional `.html` pages you create.
- `order/index.html` — optional noindex bridge/redirect page for affiliate links.
- `assets/` — images, favicon.
- `styles.css` — all custom styles.
- `script.js` — site scripts.
- `_headers` / `_redirects` — Cloudflare Pages config.

## Important Rules
- Use **clean URLs** (no `.html` in internal links or canonical/sitemap).
- Keep schema markup valid JSON-LD.
- Do not push local-only folders/files defined in `.gitignore`.
