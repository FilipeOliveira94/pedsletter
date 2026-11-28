// Site configuration. The single indexing switch lives here (AGENTS.md §5).
// It stays false until phase 9, and only Filipe's decision turns it on.
export const indexavel: boolean = false;

export const site = {
  title: "PedsLetter",
  lang: "pt-BR",
} as const;

// Mandatory notices (AGENTS.md §4). Exact wording; do not edit.
export const avisos = {
  curadoriaIA:
    "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original.",
  publico: "Conteúdo destinado a médicos e demais profissionais de saúde.",
} as const;
// F1-01 proof: a deliberate type error that CI must reject. Reverted next commit.
export const quebra: number = "texto";
