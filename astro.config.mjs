// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://javaburn2.us',
  output: 'static',
  trailingSlash: 'never',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      lastmod: new Date(),
      priority: 0.7,
      entryLimit: 10000,
      serialize(item) {
        // Higher priority for homepage
        if (item.url === 'https://javaburn2.us/') {
          item.priority = 1.0;
        }
        return item;
      }
    })
  ],
  build: {
    format: 'directory'
  }
});
