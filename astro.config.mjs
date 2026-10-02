import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://ming-history.kuige.me",
  output: "static",
  compressHTML: true,
  integrations: [sitemap()],
  build: { inlineStylesheets: "auto" },
});
