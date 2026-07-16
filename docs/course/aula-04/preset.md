# Aula 4 — Preset de gravação (versionado)

> Estado de tela reproduzível para gravar a aula. Todos os resultados abaixo
> foram computados com o código deste repositório e estão **fixados por
> teste** em `tests/test_lesson_presets.py` — se algum número mudar, o CI
> quebra e este arquivo deve ser atualizado no mesmo commit.

## Configuração do app

| Controle | Valor |
|---|---|
| Modo | Analyze |
| Interface language | Português (BR) |
| Idioma da análise | Auto |
| Detector automático | começar em **Palavras-indício (baseline)**; trocar para **N-gramas** no passo 5 |
| Tokens em minúsculas | ✔ (padrão) |
| Ferramentas extras | ligar **Correspondências de indícios de idioma** |
| Aba usada | *Perfil linguístico* |

## Inputs e resultados esperados

### Passo 1 — Frase portuguesa (evidência visível)

Colar:

```
O gato subiu no telhado e a casa ficou em silêncio, o que preocupou a vizinha de Capitu.
```

Esperado (tabela de evidência):

| Idioma | Ocorrências | Palavras correspondentes |
|---|---|---|
| Portuguese | **7** | o ×2, a ×2, e, que, de |
| Spanish | 2 | que, de |
| French | 2 | que, de |
| Italian | 1 | e |
| English / German | 0 | — |

Fala-chave: "que" e "de" pontuam para três línguas românicas — o parentesco
é visível na tabela.

### Passo 2 — "que de" (empate e viés de ordem)

Colar: `que de`

Esperado: Spanish, French e Portuguese empatam com **2 pontos cada**;
o app declara o empate no caption e entrega **Spanish** pela ordem fixa.
Fala-chave: o viés não está escondido — está escrito na tela.

### Passo 3 — Texto russo (fallback declarado)

Colar:

```
Я не понимаю, что здесь написано, но всё равно интересно.
```

Esperado: **zero** indícios em todos os idiomas → English com o aviso de
fallback documentado. Limite de escopo, declarado em vez de disfarçado.

### Passo 4 — Degradação medida em texto curto

Colar: `telhado bonito`

Esperado: nenhum indício → fallback English (**errado**). Mostrar em
seguida a tabela do relatório de erros: 75,6% → **28,9%** de acurácia com
entradas de 2 palavras (77% de fallback). Evidência esparsa, não ruído.

### Passo 5 — Trocar para o detector por n-gramas

Trocar **Detector automático** para *N-gramas de caractere* e repetir:

| Input | Palavras-indício | N-gramas de caractere |
|---|---|---|
| Frase portuguesa | Portuguese (7 pontos) | **Portuguese** (menor distância; Spanish em 2º) |
| `telhado bonito` | fallback English ✗ | **Portuguese** ✓ (Portuguese < Spanish) |
| `que de` | Spanish (empate + ordem) | **French** (60) < Portuguese (133) < Spanish (180) |
| Texto russo | fallback English | English com **todas as distâncias iguais** (empate na penalidade máxima, sem flag — limitação honesta) |

Falas-chave:

1. `telhado bonito`: trigramas existem em qualquer palavra — por isso o
   método aguenta texto curto (61% vs 29% medido).
2. `que de`: **os dois detectores transparentes discordam** — a entrada é
   genuinamente ambígua; o que ganhamos é evidência inspecionável, não
   uma resposta mágica.
3. Russo: distância máxima uniforme deveria significar "sem evidência";
   hoje devolve English por ordem fixa sem aviso — uma limitação real da
   implementação, dita na tela.

### Fechamento — Benchmarks

Modo *Benchmarks*: hint-words 75,6% · char-ngrams **98,9%** · langdetect
99,4% — e a leitura honesta: **um erro de diferença** (178 vs 179 acertos
em 180) num conjunto pequeno, de um gênero só. Ponte para a Aula 7.

## Referências do pacote

- Handbook: [`docs/handbook/deteccao-de-idioma.md`](../../handbook/deteccao-de-idioma.md)
- Exercícios + gabarito: [`exercicios.md`](exercicios.md)
- Resultados fixados: `tests/test_lesson_presets.py`
- Roteiro completo: [`../syllabus.md`](../syllabus.md) (Aula 4)
