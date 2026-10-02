import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://ming-history.example",
  output: "static",
  compressHTML: true,
  build: { inlineStylesheets: "auto" },
});
