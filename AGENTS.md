# Java Burn 2.0 — AstroJS Project

## Project Identity
- **Product:** Java Burn 2.0
- **Domain:** https://javaburn2.us
- **Official Website:** https://morningcoffeeritual.net/
- **Stack:** AstroJS (static site generation)
- **Deployment:** Cloudflare Pages
- **Build Output:** `dist/`

## Working Directory
`f:\Published Websites\javaburn2.us`

## Build & Development
```bash
npm install
npm run dev      # local dev server at http://localhost:4321
npm run build    # production build to dist/
npm run preview  # preview production build
```

## Project Structure
- `src/layouts/Layout.astro` — base layout with shared head, navbar, footer, schemas
- `src/pages/*.astro` — one file per route
- `public/` — static assets, images, favicons, config files
- `public/_headers` — Cloudflare Pages security/cache headers
- `public/_redirects` — Cloudflare Pages redirect rules
- `dist/` — build output (gitignored)

## Important Rules
- Use clean URLs in all internal links: `/java-burn`, not `/java-burn.html`
- Keep canonical URLs as `https://javaburn2.us/page-slug`
- Preserve JSON-LD schemas on every page
- `/order/` page must remain `noindex` and redirect to affiliate URL
- Do not add dangerous rewrite rules like `/* /:splat.html 200` in `_redirects`
- Cloudflare Pages natively handles clean URLs

## Deployment
- Push to `main` branch triggers GitHub Actions workflow
- Requires GitHub secrets: `CF_PROJECT_NAME`, `CF_GLOBAL_KEY`, `CF_EMAIL`, `CF_ACCOUNT_ID`
