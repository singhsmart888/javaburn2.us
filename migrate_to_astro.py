#!/usr/bin/env python3
"""
Migrate existing static HTML pages into Astro .astro files using src/layouts/Layout.astro.
Extracts title, description, keywords, canonical, JSON-LD schemas, and main content.
"""
import json
import os
import re

SITE_URL = 'https://javaburn2.us'

PAGES = [
    ('_old-static-site/index.html', 'src/pages/index.astro', {'home': True}),
    ('_old-static-site/about-us.html', 'src/pages/about-us.astro', {}),
    ('_old-static-site/benefits.html', 'src/pages/benefits.astro', {}),
    ('_old-static-site/contact-us.html', 'src/pages/contact-us.astro', {}),
    ('_old-static-site/ingredients.html', 'src/pages/ingredients.astro', {}),
    ('_old-static-site/reviews.html', 'src/pages/reviews.astro', {}),
    ('_old-static-site/privacy-policy.html', 'src/pages/privacy-policy.astro', {}),
    ('_old-static-site/terms-conditions.html', 'src/pages/terms-conditions.astro', {}),
    ('_old-static-site/refund-policy.html', 'src/pages/refund-policy.astro', {}),
    ('_old-static-site/order-tracking.html', 'src/pages/order-tracking.astro', {}),
    ('_old-static-site/404.html', 'src/pages/404.astro', {'noindex': True}),
    ('_old-static-site/java-burn.html', 'src/pages/java-burn.astro', {}),
    ('_old-static-site/java-burn-supplement.html', 'src/pages/java-burn-supplement.astro', {}),
    ('_old-static-site/java-burn-review.html', 'src/pages/java-burn-review.astro', {}),
    ('_old-static-site/java-burn-price.html', 'src/pages/java-burn-price.astro', {}),
    ('_old-static-site/java-burn-discount.html', 'src/pages/java-burn-discount.astro', {}),
    ('_old-static-site/java-burn-sale.html', 'src/pages/java-burn-sale.astro', {}),
    ('_old-static-site/java-burn-buy.html', 'src/pages/java-burn-buy.astro', {}),
    ('_old-static-site/java-burn-order.html', 'src/pages/java-burn-order.astro', {}),
    ('_old-static-site/java-burn-metabolism-booster.html', 'src/pages/java-burn-metabolism-booster.astro', {}),
    ('_old-static-site/java-burn-official-website.html', 'src/pages/java-burn-official-website.astro', {}),
    ('_old-static-site/java-burn-scam.html', 'src/pages/java-burn-scam.astro', {}),
    ('_old-static-site/java-burn-official.html', 'src/pages/java-burn-official.astro', {}),
]


def q(s):
    return s.replace('"', '\\"')


def extract_tag(html, tag, attr=None):
    if attr:
        pattern = rf'<{tag}[^>]*{re.escape(attr)}="([^"]*)"[^>]*>'
    else:
        pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
    m = re.search(pattern, html, re.S | re.I)
    return m.group(1).strip() if m else None


def extract_meta(html, name):
    m = re.search(rf'<meta[^>]*name="{re.escape(name)}"[^>]*content="([^"]*)"', html, re.I)
    if m:
        return m.group(1)
    m = re.search(rf'<meta[^>]*content="([^"]*)"[^>]*name="{re.escape(name)}"', html, re.I)
    return m.group(1) if m else None


def extract_og(html, prop):
    m = re.search(rf'<meta[^>]*property="{re.escape(prop)}"[^>]*content="([^"]*)"', html, re.I)
    return m.group(1) if m else None


def extract_schemas(html):
    schemas = []
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            schemas.append(json.loads(m.group(1)))
        except Exception:
            pass
    return schemas


def extract_main_content(html):
    m = re.search(r'<main\s+id="main"[^>]*>(.*?)</main>', html, re.S | re.I)
    return m.group(1).strip() if m else ''


def extract_pre_main(html):
    m = re.search(r'<body[^>]*>(.*?)<main\s+id="main"[^>]*>', html, re.S | re.I)
    if not m:
        return ''
    content = m.group(1).strip()
    content = re.sub(r'<section\s+class="menu\s+trimology-menu-section".*?</section>\s*', '', content, flags=re.S | re.I)
    content = re.sub(r'<div\s+class="kw-header-bar".*?</div>\s*', '', content, flags=re.S | re.I)
    return content.strip()


def extract_post_main(html):
    m = re.search(r'</main>(.*?)</body>', html, re.S | re.I)
    if not m:
        return ''
    content = m.group(1).strip()
    content = re.sub(r'<footer\s+class="trimology-footer-section".*?</footer>\s*', '', content, flags=re.S | re.I)
    content = re.sub(r'<div\s+class="sticky-footer-cta".*?</div>\s*', '', content, flags=re.S | re.I)
    content = re.sub(r'<script\s+src="alphacur\.min\.js"></script>\s*', '', content, flags=re.S | re.I)
    content = re.sub(r'<script>\s*document\.addEventListener\([\'"]DOMContentLoaded[\'"].*?</script>\s*', '', content, flags=re.S | re.I)
    return content.strip()


def fix_paths(content):
    content = re.sub(r'href="alphacur\.min\.css"', 'href="/alphacur.min.css"', content)
    content = re.sub(r'href="alphacur-main\.min\.css"', 'href="/alphacur-main.min.css"', content)
    content = re.sub(r'href="javaburn-theme\.css"', 'href="/javaburn-theme.css"', content)
    content = re.sub(r'src="alphacur\.min\.js"', 'src="/alphacur.min.js"', content)
    content = re.sub(r'src="assets/images/', 'src="/assets/images/', content)
    content = re.sub(r'href="/order/index\.html"', 'href="/order"', content)
    return content


def indent_block(content, spaces=2):
    indent = ' ' * spaces
    return '\n'.join(indent + line if line.strip() else line for line in content.split('\n'))


def convert_page(src, dest, extra):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    title = extract_tag(html, 'title') or 'Java Burn'
    desc = extract_meta(html, 'description') or ''
    keywords = extract_meta(html, 'keywords') or ''
    canonical = extract_tag(html, 'link', 'rel="canonical"') or None
    og_title = extract_og(html, 'og:title') or title
    og_desc = extract_og(html, 'og:description') or desc

    schemas = extract_schemas(html)
    filtered = []
    for s in schemas:
        t = s.get('@type')
        if t in ('Organization', 'WebPage'):
            continue
        filtered.append(s)

    main_content = fix_paths(extract_main_content(html))
    pre_main = fix_paths(extract_pre_main(html))
    post_main = fix_paths(extract_post_main(html))

    fm_lines = ['---', 'import Layout from "../layouts/Layout.astro";']
    fm_lines.append(f'const title = "{q(title)}";')
    fm_lines.append(f'const description = "{q(desc)}";')
    if keywords:
        fm_lines.append(f'const keywords = "{q(keywords)}";')
    if canonical:
        fm_lines.append(f'const canonical = "{canonical}";')
    if og_title != title:
        fm_lines.append(f'const ogTitle = "{q(og_title)}";')
    if og_desc != desc:
        fm_lines.append(f'const ogDescription = "{q(og_desc)}";')
    if filtered:
        fm_lines.append(f'const extraSchemas = {json.dumps(filtered)};')
    if extra.get('noindex'):
        fm_lines.append('const noindex = true;')
    if extra.get('home'):
        fm_lines.append('const showStickyFooter = true;')
        fm_lines.append('const ogType = "website";')
    fm_lines.append('---')

    body_lines = ['<Layout']
    body_lines.append('  title={title}')
    body_lines.append('  description={description}')
    if keywords:
        body_lines.append('  keywords={keywords}')
    if canonical:
        body_lines.append('  canonical={canonical}')
    if og_title != title:
        body_lines.append('  ogTitle={ogTitle}')
    if og_desc != desc:
        body_lines.append('  ogDescription={ogDescription}')
    if filtered:
        body_lines.append('  extraSchemas={extraSchemas}')
    if extra.get('noindex'):
        body_lines.append('  noindex={true}')
    if extra.get('home'):
        body_lines.append('  showStickyFooter={true}')
        body_lines.append('  ogType="website"')
    body_lines.append('>')

    if pre_main:
        body_lines.append('  <Fragment slot="header-bar">')
        body_lines.append(indent_block(pre_main, 4))
        body_lines.append('  </Fragment>')

    body_lines.append(indent_block(main_content, 2))

    if post_main:
        body_lines.append('  <Fragment slot="post-main">')
        body_lines.append(indent_block(post_main, 4))
        body_lines.append('  </Fragment>')

    body_lines.append('</Layout>')

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fm_lines) + '\n' + '\n'.join(body_lines) + '\n')
    print(f'Converted: {src} -> {dest}')


def main():
    for src, dest, extra in PAGES:
        convert_page(src, dest, extra)

    os.makedirs('src/pages/order', exist_ok=True)
    with open('src/pages/order/index.astro', 'w', encoding='utf-8') as f:
        f.write('''---
import Layout from "../../layouts/Layout.astro";
const title = "Java Burn Order";
const description = "Redirecting to the official Java Burn order page.";
---
<Layout title={title} description={description} noindex={true}>
  <div style="text-align:center;padding:80px 20px;">
    <h1>Redirecting to Official Java Burn Order Page...</h1>
    <p>Please wait while we take you to the secure checkout.</p>
  </div>
  <script is:inline>
    window.location.replace("https://mwebxara.com/12271/227/3/?subid=HHC_javaburn");
  </script>
</Layout>
''')
    print('Created: src/pages/order/index.astro')


if __name__ == '__main__':
    main()
