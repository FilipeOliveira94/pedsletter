import avisosJson from "./avisos.json";

// Site configuration. The single indexing switch lives here (AGENTS.md §5).
// It stays false until phase 9, and only Filipe's decision turns it on.
export const indexavel: boolean = false;

export const site = {
  title: "PedsLetter",
  lang: "pt-BR",
} as const;

// Mandatory notices (AGENTS.md §4). Exact wording; do not edit. The text lives
// in avisos.json so that scripts/site_check.py checks the same copy (F1-03).
export const avisos = avisosJson;
