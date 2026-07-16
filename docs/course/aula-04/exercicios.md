# Aula 4 — Exercícios

> Regras: os exercícios 1–3 se resolvem **com lápis e papel**, usando só a
> tabela de indícios do handbook
> ([`deteccao-de-idioma.md`](../../handbook/deteccao-de-idioma.md));
> confira depois no app. O exercício 4 usa o app diretamente.

## Exercício 1 — Contar evidência à mão

Frase: **"A menina disse que o mar e a areia eram de outro mundo."**

a) Liste os tokens (minúsculas).
b) Monte a tabela de pontos por idioma (indício por indício).
c) Qual idioma vence, e com quantos pontos?
d) Quais palavras pontuaram para mais de um idioma?

## Exercício 2 — Construir um empate

Escreva uma sequência de **no máximo 4 palavras** que produza empate entre
pelo menos duas línguas na tabela de indícios. Diga quais línguas empatam,
com quantos pontos, e **qual será a resposta do detector** (lembre da ordem
fixa English → Spanish → French → German → Italian → Portuguese).

## Exercício 3 — Perfil de trigramas à mão

Palavra: **"arara"**.

a) Escreva a forma normalizada (fronteiras `_`).
b) Liste todos os trigramas e suas frequências.
c) Escreva o perfil ordenado (frequência decrescente; empate alfabético).

## Exercício 4 — Prever antes de rodar (app)

Para cada entrada, **preveja** o que dirá cada detector (indícios e
n-gramas) e só depois cole no app para conferir:

a) `de la` — b) `guten morgen` — c) `the o and e`

Para cada caso, explique em uma frase *por que* o resultado saiu como saiu
(evidência, empate, fallback ou distância).

---

# Gabarito comentado

## Exercício 1

a) Tokens: a, menina, disse, que, o, mar, e, a, areia, eram, de, outro,
mundo.

b/c) Pontos:

| Idioma | Palavras que pontuaram | Pontos |
|---|---|---|
| **Portuguese** | a ×2, que, o, e, de | **6** |
| Spanish | que, de | 2 |
| French | que, de | 2 |
| Italian | e | 1 |
| English, German | — | 0 |

Português vence com **6 pontos**.

d) "que" e "de" pontuam para Portuguese, Spanish **e** French; "e" pontua
para Portuguese e Italian; "a" e "o" só para Portuguese (nos conjuntos
deste toolbox). Comentário: é exatamente essa sobreposição românica que
gera a confusão fr→es do benchmark (Aula 7).

## Exercício 2

Resposta modelo: `que de` empata Spanish, French e Portuguese com 2 pontos
cada → o detector responde **Spanish**, o primeiro da ordem fixa entre os
empatados. Qualquer combinação só de indícios compartilhados funciona
(`la de` empata Spanish e French → Spanish; `que e` empata Portuguese e
Italian? — cuidado: "que" não é indício italiano, "che" é; então `que e`
dá Portuguese 2 × Italian 1 × Spanish/French 1 — **não** é empate no topo).
O erro comum é esquecer de conferir palavra por palavra na tabela — que é
o ponto do exercício.

## Exercício 3

a) `_arara_`

b) Trigramas: `_ar`, `ara`, `rar`, `ara`, `ra_` → frequências: **ara ×2**;
_ar, ra_, rar ×1.

c) Perfil: **ara, _ar, ra_, rar** (ara primeiro por frequência; os demais
empatados em 1 entram em ordem alfabética: `_ar` < `ra_` < `rar`, porque
`_` ordena antes de letra e `a` < `r`). Confira com
`build_ngram_profile("arara")`.

## Exercício 4

a) `de la` — Indícios: "de" pontua ES/FR/PT; "la" pontua ES/FR **e IT**
("la" está no conjunto italiano — pegadinha que a tabela revela). Placar:
ES 2, FR 2, IT 1, PT 1 → empate ES/FR no topo → **Spanish** pela ordem
fixa (empate declarado no caption). N-gramas: **French** vence (os três
primeiros são French < Spanish < Italian — todas românicas, próximas).
Os dois detectores discordam de novo, como em `que de`: entrada
genuinamente ambígua, e o que ganhamos é a evidência inspecionável, não
uma "resposta certa" que a entrada não tem.

b) `guten morgen` — Indícios: **nenhuma** das duas palavras está em
conjunto algum (der/die/und/zu/mit/ist não incluem "guten"/"morgen") →
**fallback English, errado**. N-gramas: trigramas como `gut`, `ten`,
`mor`, `gen` são frequentes no perfil alemão → **German**, correto. É o
mesmo contraste do `telhado bonito` do preset: indícios precisam de
palavras específicas; trigramas existem em qualquer palavra.

c) `the o and e` — Pegadinha: "the" e "and" pontuam English (2); "o" e "e"
pontuam Portuguese (2); "e" também pontua Italian (1). Empate
English/Portuguese no topo → **English** pela ordem fixa. N-gramas:
também **English** (English < Portuguese na tabela de distâncias — os
trigramas de "the"/"and" pesam mais que as vogais soltas). Moral: nenhum
dos detectores "entende" a mistura — eles contam. Entradas com
code-switching são um modo de falha documentado (ver
`docs/error-analysis.md`), e a resposta honesta é mostrar a evidência dos
dois lados, que é o que a tabela faz.
