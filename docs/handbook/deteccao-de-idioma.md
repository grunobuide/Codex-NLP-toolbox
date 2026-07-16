# Detecção de idioma: palavras-indício e n-gramas de caracteres

> **EN summary** — *Language identification with two transparent methods:
> hint-word counting (a deliberately weak, fully inspectable baseline) and
> character trigram profiles with out-of-place distance (Cavnar & Trenkle
> 1994). Both are hand-computable; both are measured against langdetect on a
> frozen dataset. Functions: `detect_language_details`,
> `language_hint_evidence`, `detect_language_ngram_details`.*

Página do handbook da **Aula 4**. Tudo aqui é verificável com lápis e papel,
e todo número citado está fixado por teste em
`tests/test_lesson_presets.py`.

---

## Método 1 — Palavras-indício (baseline transparente)

### Mecanismo

Cada idioma tem um conjunto minúsculo (6–7) de palavras funcionais de
altíssima frequência:

| Idioma | Indícios |
|---|---|
| English | the, and, is, of, to, with, that |
| Spanish | el, la, que, y, de, para |
| French | le, la, que, et, de, pour |
| German | der, die, und, zu, mit, ist |
| Italian | il, la, che, e, di, per |
| Portuguese | o, a, que, e, de, para |

O texto é tokenizado (minúsculas) e cada idioma ganha **1 ponto por token
que pertence ao seu conjunto**. Vence o idioma com mais pontos. Duas regras
explícitas — e é aqui que moram os vieses:

- **Empate**: resolvido pela ordem fixa English → Spanish → French →
  German → Italian → Portuguese. Não é neutro; é documentado.
- **Evidência zero**: nenhum indício encontrado → English, com
  `fallback=True` sinalizado.

### Exemplo calculado à mão

Frase: **"O gato subiu no telhado e a casa ficou em silêncio, o que
preocupou a vizinha de Capitu."**

Tokens (minúsculas): o, gato, subiu, no, telhado, e, a, casa, ficou, em,
silêncio, o, que, preocupou, a, vizinha, de, capitu.

Agora conte, por idioma, quais tokens estão na tabela de indícios:

| Idioma | Palavras que pontuaram | Pontos |
|---|---|---|
| Portuguese | o ×2, a ×2, e, que, de | **7** |
| Spanish | que, de | 2 |
| French | que, de | 2 |
| Italian | e | 1 |
| English | — | 0 |
| German | — | 0 |

Português vence com 7. Repare que "que" e "de" pontuam para **três**
línguas românicas ao mesmo tempo — parentesco linguístico virando confusão
estrutural. No app: aba *Language profile* → *Language hint matches*
(função `language_hint_evidence`).

### Quando o método quebra (medido, não especulado)

- **Texto curto**: "telhado bonito" não contém nenhum indício → fallback
  English, errado. No conjunto de avaliação, a acurácia cai de **75,6%**
  (sentenças completas) para **28,9%** (2 palavras), com 77% de fallback.
- **Empate ambíguo**: "que de" empata Spanish/French/Portuguese com 2
  pontos cada; a ordem fixa entrega **Spanish** — um viés visível.
- **Fora do escopo**: texto russo → zero indícios → English por convenção
  (fallback declarado).

---

## Método 2 — N-gramas de caracteres (Cavnar–Trenkle 1994)

### Mecanismo

1. **Normalização**: minúsculas; toda sequência de não-letras vira um único
   `_` (marcador de fronteira).
2. **Perfil**: conte todos os **trigramas** (janelas de 3 caracteres) que
   contêm ao menos uma letra; ordene por frequência (empates em ordem
   alfabética). O perfil de um idioma é a lista dos 300 trigramas mais
   frequentes, treinada em três artigos da Wikipédia por idioma
   (proveniência: `nlp_toolbox/resources/ngram_profiles/PROVENANCE.md`).
3. **Distância out-of-place**: para cada trigrama do perfil do texto,
   some `|posição no texto − posição no perfil do idioma|`; trigrama
   ausente do perfil paga a penalidade máxima (o tamanho do perfil).
   **Menor distância = idioma mais próximo.**

### Exemplo calculado à mão (1): construir um perfil

Texto: **"banana"** → normalizado: `_banana_`

Trigramas: `_ba`, `ban`, `ana`, `nan`, `ana`, `na_`

| Trigrama | Frequência |
|---|---|
| ana | 2 |
| _ba, ban, na_, nan | 1 cada |

Perfil ordenado (frequência desc., empate alfabético):
**ana, _ba, ban, na_, nan** — confira com
`build_ngram_profile("banana")`.

### Exemplo calculado à mão (2): distância out-of-place

Perfil do texto A (de "da da da la"): `_da, da_, a_d, _la, a_l, la_`
Perfil da língua B (de "la la da"): `_la, la_, _da, a_d, a_l, da_`

| Trigrama | Posição em A | Posição em B | \|dif\| |
|---|---|---|---|
| _da | 1 | 3 | 2 |
| da_ | 2 | 6 | 4 |
| a_d | 3 | 4 | 1 |
| _la | 4 | 1 | 3 |
| a_l | 5 | 5 | 0 |
| la_ | 6 | 2 | 4 |

Distância A→B = **14**. Um texto "mais parecido com B" teria distância
menor. É só isso: contar, ordenar e somar diferenças de posição.

### Por que funciona melhor em texto curto

Palavras-indício precisam de palavras *específicas*; trigramas existem em
**qualquer** token. "telhado bonito" não tem nenhum indício, mas tem 14
trigramas — e eles aproximam o texto do perfil português (menor distância),
acertando onde o método 1 caiu no fallback. Medido no conjunto congelado:
**98,9% vs 75,6%** em sentenças completas; **61% vs 29%** em entradas de
2 palavras.

### Quando o método quebra (também medido)

- **Entradas ambíguas**: "que de" → French (60), Portuguese (133),
  Spanish (180). O detector por indícios diz Spanish; o de n-gramas diz
  French. **Os dois métodos transparentes discordam** — e a entrada é
  genuinamente ambígua. Não há resposta certa; há evidência inspecionável.
- **Alfabeto fora do treino**: texto cirílico não compartilha nenhum
  trigrama com os perfis latinos → **todas as distâncias empatam na
  penalidade máxima** e a ordem fixa devolve English **sem** flag de
  fallback. Limitação honesta da implementação atual: distância máxima
  uniforme deveria ser tratada como "sem evidência" (candidata a melhoria
  no relatório de erros).
- **Comparação externa**: langdetect faz 99,4% no mesmo conjunto — um erro
  a menos que os n-gramas (179 vs 178 acertos em 180). Conjunto pequeno,
  um gênero (romances), uma obra por língua: diferença indicativa, não
  conclusiva.

---

## Referências

- Cavnar, W. B. & Trenkle, J. M. (1994). *N-gram-based text
  categorization*. SDAIR-94.
- Dados, matrizes de confusão e proveniência: `docs/benchmarks.md`,
  `evals/DATASETS.md`.
- Análise de erros (inerente vs. corrigível): `docs/error-analysis.md`.
- **Ponte moderna**: fastText language ID e o próprio langdetect usam a
  mesma intuição (estatística de caracteres/subpalavras) com modelos
  maiores e treino massivo — o salto é de escala, não de natureza.
