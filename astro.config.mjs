// @ts-check
import { defineConfig } from "astro/config";

// Static output only. No integrations: no sitemap until phase 9 (AGENTS.md §4).
export default defineConfig({
  output: "static",
});
