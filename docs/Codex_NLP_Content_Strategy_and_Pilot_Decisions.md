# Estratégia de conteúdo e decisões do piloto

> Fonte de verdade editorial do curso. Decisões de produto ficam em
> `ROADMAP.md`; decisões de conteúdo pedagógico ficam aqui e em
> `CONTENT_ROADMAP.md`. Última revisão: 2026-07-16.

## Diagnóstico

A engenharia da ferramenta está suficientemente madura (métodos, avaliação,
documentação, demo, camada bilíngue testada). O gargalo é transformar
funcionalidades em uma experiência educacional validada, consistente e
publicável. Portanto: **não** produzir handbook completo + 7 roteiros + 7
notebooks + lesson mode antes de validar uma única aula de ponta a ponta.

Sequência adotada:

```
contrato editorial → aula-piloto completa (Aula 4) → feedback → templates → produção em série
```

## Contrato editorial

| Campo | Decisão |
|---|---|
| **Título** | **Fundamentos transparentes de PLN: do texto à avaliação** (substitui "Linguística de corpus computacional: métodos transparentes" — o currículo é mais amplo que linguística de corpus) |
| **Público primário** | Estudantes de Letras/Linguística **sem pré-requisito de programação**. O app é a interface principal; código é opcional |
| **Públicos secundários** | Estudantes de ciência de dados entrando em NLP; professores buscando material de aula |
| **Problema do público** | Cursos de PLN ou pressupõem programação, ou pulam direto para modelos caixa-preta; falta material que ensine os fundamentos *verificáveis à mão* e como **medir** quando um método funciona |
| **Promessa** | Ao final, o aluno domina os instrumentos clássicos de análise de texto, sabe rodá-los num app aberto, e — a assinatura do curso — sabe avaliar métodos com padrão-ouro, métricas e análise de erros |
| **Conhecimentos de entrada** | Leitura acadêmica básica; nenhuma programação |
| **Resultado esperado** | Aluno analisa um corpus próprio no app, interpreta cada número, e explica os modos de falha de cada método |
| **Escopo** | Os 7 temas do syllabus (`docs/course/syllabus.md`), sempre com método transparente + avaliação medida |
| **Não objetivos** | Ensinar programação; cobrir transformers/LLMs (apenas apontar a ponte); competir com cursos de spaCy/NLTK; plataforma de curso complexa |
| **Formato** | Screencast (tela + voz), 15–20 min por aula; o app ao vivo é o material de tela |
| **Idioma** | Vídeos e handbook em PT-BR; título/resumo/referências também em EN; legendas EN quando possível; documentação técnica e GitHub em inglês. **Não** duplicar todo o material em dois idiomas no lançamento |
| **Objetivo principal** | **Autoridade profissional + portfólio** (evidência pública de competência técnica e didática para o mercado de ML/NLP engineering) |
| **Canal** | ⏳ **PENDENTE** — provavelmente plataforma de curso e/ou YouTube. Decidir antes de gravar o piloto (afeta formato de abertura, duração e CTA na tela) |
| **Frequência / ritmo** | ⏳ **PENDENTE** — depende do tempo semanal sustentável, ainda não estimado. Decidir após medir o esforço real do piloto |
| **CTA (hierarquia)** | 1º usar o app + visitar o GitHub (autoridade) · 2º continuar para a próxima aula (retenção) · 3º conhecer o bruno.guide / lista (quando existirem) |
| **Métricas de sucesso** | Piloto: feedback qualitativo de ≥5 pessoas do público-alvo + retenção do vídeo. Temporada: conclusão das 7 aulas, uso do app rastreável (stars/tráfego do demo), 1+ convite decorrente (palestra, aula, entrevista) |

## Decisões de conteúdo (Content QA — 2026-07-16)

1. **Aula 2 / corpus**: o app demonstra em excertos (~1.800 chars, versionados
   em `data/samples/`); o experimento com romances completos vive no notebook.
   Papel de cada um explícito no roteiro. (Opção "app para demonstração,
   notebook para experimento de corpus".)
2. **Aula 5 / Porter**: exemplos exclusivamente ingleses (`running → run`,
   `relational → relat`, `university`/`universal → univers`), com ponte
   explícita: stemming é dependente de língua e o toolbox só cobre inglês.
3. **Aula 4 / evidência**: a API foi ampliada (`language_hint_evidence`)
   para retornar **quais tokens** pontuaram por idioma e quantas vezes; o
   app mostra a tabela Language / Hits / Matched words. A promessa "mostra
   quais palavras decidiram" agora é literalmente verdadeira.
4. **Números fixos em roteiros**: proibidos. Todo valor citado em aula deve
   vir de um preset versionado (sample + configuração + resultado esperado
   conferido), entregue no pacote da aula. O Lesson Mode (futuro) automatiza
   isso; até lá, o gabarito da aula cumpre o papel.
5. **"Seis línguas como cidadãs de primeira classe"** significa, com precisão:
   - **Interface e recursos** (stopwords, léxicos de sentimento, fórmulas de
     legibilidade, perfis n-gram, samples): as 6 línguas, paridade real.
   - **Avaliação**: identificação de idioma cobre as 6; sentimento e
     segmentação são avaliados **apenas em inglês** (datasets ouro EN).
   - **Métodos específicos de língua**: Porter stemmer é apenas inglês.
   - A promessa pública (README, curso) deve sempre distinguir esses níveis.

## Aula-piloto: Aula 4 — "Que língua é essa?"

Escolhida por ter a melhor narrativa educacional do projeto: baseline
simples → evidência observável → vieses (empate "que de", fallback) →
degradação medida em texto curto (75,6% → 28,9%) → n-gramas de caracteres →
melhoria medida (98,9%; 61% vs 29% em 2 palavras) → comparação honesta com
langdetect (um erro de diferença no conjunto pequeno) → limitações do
conjunto de avaliação. Demonstra simultaneamente linguística, implementação
interpretável, avaliação, análise de erros, proveniência e pensamento
crítico.

### Entregáveis do pacote-piloto

1. Vídeo principal (15–20 min, tela + voz).
2. Página da aula (objetivos, conceitos, referências, resumo).
3. Página de handbook sobre hints e n-gramas (a primeira do handbook).
4. Preset do app (inputs e opções predefinidos, versionados).
5. Exercício com 3–4 casos.
6. Gabarito comentado.
7. Notebook opcional: acurácia × tamanho do texto de entrada.
8. Dados e resultados esperados versionados.
9. Um conteúdo curto derivado (ex.: 2 min sobre por que "que de" é ambíguo).

### Checklist de validação pós-piloto

- [ ] Onde as pessoas se perdem?
- [ ] Os method cards bastam como apoio de tela?
- [ ] 15–20 min comportam o conteúdo?
- [ ] O público quer mais teoria ou mais demonstração?
- [ ] O notebook é realmente necessário?
- [ ] O app funciona bem como material de tela?
- [ ] Esforço real de produção (horas) → define ritmo sustentável e canal

## Sistema de conteúdo (pós-piloto)

**Obrigatório por aula:** vídeo · objetivo de aprendizagem · app preset ·
uma explicação conceitual · um exemplo manual · uma limitação · um
exercício · gabarito · referências.

**Opcional:** notebook · dataset adicional · vídeo curto · artigo · slides.

Notebooks apenas onde agregam experimento real: Zipf/crescimento (Aula 2),
idioma × tamanho de entrada (Aula 4), tamanho do léxico (Aula 5), avaliação
e matrizes de confusão (Aula 7). Tokenização, KWIC e legibilidade se ensinam
com app + exercícios.

**Ordem de produção** (publicação continua 1–7): Aula 4 (piloto) → 7
(assinatura) → 1 (entrada) → 3 → 2 → 5 → 6.

## Riscos monitorados

- Produzir sete aulas antes de validar uma. ← mitigado pelo piloto
- Título mais estreito que o currículo. ← resolvido (novo título)
- Duplicar todo o material em dois idiomas. ← resolvido (PT-first)
- Roteiros com resultados que não correspondem ao app. ← resolvido (QA + presets)
- Handbook + notebooks + vídeos + lesson mode simultâneos. ← mitigado (fases)
- Toolbox virar plataforma de curso complexa. ← não objetivo declarado
- Volume acima de clareza e consistência. ← contrato por aula

## Pendências abertas

| # | Decisão | Prazo sugerido |
|---|---|---|
| 1 | Canal de publicação (plataforma e/ou YouTube) | antes de gravar o piloto |
| 2 | Tempo semanal sustentável → ritmo (temporada/semanal/bloco) | após medir esforço do piloto |
| 3 | bruno.guide: seção do curso e integração com CTA | junto com a publicação do piloto |
