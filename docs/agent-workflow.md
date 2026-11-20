# Prompts de trabalho para agentes

Três prompts conduzem uma issue: planejar, implementar e fechar. Eles não dependem de ferramenta; as regras ficam no [`AGENTS.md`](../AGENTS.md). Troque os marcadores, rode primeiro o prompt de plano e aprove o plano antes de qualquer mudança em arquivo.

---

## 1. Planejar (sem editar arquivos)

```text
Siga o AGENTS.md.

Quero trabalhar na issue: <ID-DA-ISSUE> — <título>.

Primeiro inspecione o código, a documentação, o roadmap, o aceite e o status atual do projeto. Não edite arquivos ainda.

Devolva:
1. Estado atual e arquivos relevantes.
2. Dependências e pré-requisitos.
3. Um plano de implementação pequeno e ordenado.
4. Critérios de aceite e como cada um será conferido.
5. Riscos, premissas e pontos de compatibilidade.
6. Comandos exatos a rodar.
7. Arquivos que devem ser criados ou modificados.
8. Nome da branch de feature (AGENTS.md §13) e quais itens do §12 "Checklist de fechamento de issue" e do §4 "Regras de conteúdo" a issue toca.

Mantenha o escopo nesta issue. Não implemente fases futuras nem mude a arquitetura em silêncio. Espere a minha aprovação antes de editar.
```

## 2. Implementar (depois do plano aprovado)

```text
Siga o AGENTS.md.

Implemente só o plano que acabamos de combinar.
- Trabalhe na branch de feature da issue, nunca na main.
- Mantenha o diff focado. Explique qualquer desvio antes de fazê-lo.
- Acrescente ou atualize os testes do comportamento alterado.
- Não implemente tarefas de fases futuras.
- Não acrescente dependências ou serviços fora do plano aprovado.
- Não rode comandos destrutivos nem contrate nada pago sem a minha aprovação explícita.
- Rode as verificações e relate a saída real.
- Atualize a documentação e o PROJECT_STATUS.md só para o que foi de fato verificado.
- Não faça commit; o fechamento faz.

Ao final, informe arquivos alterados, verificações rodadas, resultados, aceite atendido e não atendido, limitações e a próxima tarefa recomendada.
```

## 3. Fechar

```text
Siga o AGENTS.md.

Revise o diff atual contra o plano combinado e o aceite. Não acrescente funcionalidade.
- Procure mudanças fora do escopo, segredos, arquivos gerados, testes fracos, desvio de configuração e comportamento não documentado.
- Confira o diff, a mensagem de commit e o texto do PR contra o §4 "Regras de conteúdo": nenhum nome de profissional, nenhuma recomendação de dose.
- Rode os comandos de validação e relate a saída real.
- Aponte os critérios de aceite não atendidos ou não verificados.
- Aplique o §12 "Checklist de fechamento de issue".
- Faça um Conventional Commit na branch de feature, dê push dela, abra o PR e analise o CI. Nunca dê push na main e nunca faça merge; o merge é do Filipe (AGENTS.md §13).

Devolva um relatório curto de conclusão, o SHA do commit, o texto sugerido para o PR (com o ID da issue e o aceite conferido) e a próxima tarefa útil.
```

---

## Outra ferramenta

Cole os mesmos três prompts na outra ferramenta e aponte para o `AGENTS.md`. Não mantenha arquivos de regras próprios dessa ferramenta no repositório, para que as regras tenham uma fonte só. A política de Git está no AGENTS.md §13 e as regras de conteúdo no §4, então a outra ferramenta também as recebe.
