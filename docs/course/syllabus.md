# Linguística de corpus computacional: métodos transparentes

Curso em 7 aulas (15–30 min cada), gravado com o app ao vivo na tela:
https://codex-nlp-toolbox.streamlit.app

**Público:** estudantes de Letras/Linguística. Nenhum pré-requisito de
programação — todo método do curso é verificável com lápis e papel, e o
código fica disponível para quem quiser ir além.

**Tese do curso:** antes de usar (ou criticar) modelos de linguagem, é
preciso dominar os instrumentos clássicos de análise: contagem, frequência,
concordância, léxicos — e, acima de tudo, saber **medir** quando um método
funciona e explicar **por que** falha.

**Materiais por aula:** roteiro de gravação (este diretório), página do
handbook por método (`docs/handbook/`), exercícios com gabarito, e
notebooks executáveis (`examples/`).

---

## Aula 1 — O texto como dados: tokens, sentenças, tipos e ocorrências

**Objetivo:** entender que "o que conta como palavra" é uma decisão
teórica, não um dado natural — e ver as consequências dela em números.

**Conceitos:** token vs. tipo (type/token), tokenização, segmentação de
sentenças, normalização (caixa), diversidade lexical.

**Roteiro de tela:**
1. Abrir o app, carregar o sample *Dom Casmurro Pt* na sidebar.
2. Aba *Text structure*: mostrar os tokens; perguntar à audiência: "não" é
   uma palavra? E "d'água"? Mostrar que `don't` fica inteiro e
   `state-of-the-art` vira 4 tokens — decisão do padrão regex, não verdade
   linguística.
3. Aba *Descriptive statistics* → Basic stats: 140 palavras, 118 tipos,
   diversidade 0,843. Discutir por que texto curto tem diversidade alta.
4. Desligar "Lowercase tokens" e mostrar o vocabulário mudar — "Capitú" e
   "capitú" viram tipos distintos.
5. Mostrar o method card `tokenize_text` (expandir "How this works").

**Exercício:** contar à mão tokens e tipos de uma estrofe de 4 versos e
conferir no app.

---

## Aula 2 — Leis estatísticas da língua: Zipf e o crescimento do vocabulário

**Objetivo:** ver que a língua obedece regularidades estatísticas fortes —
e que isso independe do idioma.

**Conceitos:** lei de Zipf (posto × frequência), lei de Heaps (crescimento
do vocabulário), comparação entre línguas.

**Roteiro de tela:**
1. Carregar *Frankenstein En* (romance inteiro, ~78 mil palavras).
2. Ligar "Zipf rank-frequency": mostrar a descida quase reta em log —
   pouquíssimas palavras dominam o texto.
3. Ligar "Vocabulary growth": a curva achata — palavras novas rareiam
   conforme o texto avança (Heaps).
4. Trocar para os samples de outras línguas e mostrar que o formato das
   curvas se mantém: a regularidade é da linguagem humana, não do inglês.

**Notebook:** *Um romance, seis línguas* — Zipf, diversidade e legibilidade
nos seis excertos do corpus do curso.

**Exercício:** prever (antes de rodar) qual palavra ocupa o posto 1 em
cada língua; conferir e explicar por que são sempre gramaticais.

---

## Aula 3 — Palavras-chave e colocações: frequência, TF-IDF, KWIC e PMI

**Objetivo:** extrair "sobre o que o texto fala" com métodos de contagem —
e entender por que frequência bruta engana.

**Conceitos:** stopwords, frequência vs. TF-IDF, concordância (KWIC),
colocações, PMI / razão de verossimilhança.

**Roteiro de tela:**
1. Carregar *Quijote Es*. Aba *Information extraction*: keywords por
   frequência lado a lado com TF-IDF; mostrar como palavras onipresentes
   caem no TF-IDF (idf = log10(N/df), calculável à mão).
2. Aba *Text structure* → KWIC: concordância de "don" — a ferramenta mais
   antiga da linguística de corpus, ainda insubstituível para ver USO.
3. [Requer C1] Colocações por PMI: pares que aparecem juntos mais do que o
   acaso prevê — de "san — cho" a expressões fixas.

**Exercício:** calcular o TF-IDF de 3 termos num texto de 4 sentenças, à
mão, e conferir no app.

---

## Aula 4 — Que língua é essa? Evidência, empates e fallback

**Objetivo:** transformar "detectar idioma" num problema de evidência
observável — e medir honestamente quando o método falha.

**Conceitos:** palavras funcionais como pistas, evidência e empate,
fallback documentado, n-gramas de caracteres (Cavnar–Trenkle 1994),
code-switching.

**Roteiro de tela:**
1. Colar uma frase em português; aba *Language profile*: a tabela de
   evidência mostra QUAIS palavras decidiram.
2. Colar "que de": empate ES/FR/PT resolvido por ordem fixa — viés visível,
   não escondido (mostrar o caption de empate).
3. Colar texto russo: fallback para English com aviso — limite de escopo
   declarado.
4. Mostrar a tabela do relatório de erros: acurácia despenca de 75,6% para
   28,9% com 2 palavras — evidência esparsa, não ruído.
5. [Requer C1] Ligar o detector por n-gramas de caracteres e repetir os
   casos: a acurácia em texto curto salta — e o método continua
   interpretável (perfis de frequência de trigramas).

**Notebook:** *Por que a detecção falha em textos curtos* — hint-words vs.
n-gramas em entradas de tamanho de tweet.

---

## Aula 5 — Sentimento com dicionários: léxicos, morfologia e negação

**Objetivo:** construir a intuição do método lexical — e conhecer seus
três modos de falha (cobertura, morfologia, negação), todos medidos.

**Conceitos:** léxico de polaridade, cobertura, flexão morfológica,
stemming (Porter), escopo da negação.

**Roteiro de tela:**
1. Colar "Que dia maravilhoso, estou muito feliz!" → positivo, com
   contagens visíveis.
2. Colar "this is not good at all" → positivo (!). Discutir: bag-of-words
   não vê sintaxe; a negação é invisível. Mostrar que o benchmark quantifica
   isso: 76,7% vs. 80% do VADER.
3. Mostrar `zero_evidence_fraction` = 48%: quase metade das sentenças não
   tem NENHUMA palavra do léxico — cobertura é o gargalo, não o algoritmo.
4. [Requer C1] Stemming: "schrecklicher" → "schrecklich"; o Porter como
   exemplo de normalização por regras, com os erros clássicos dele
   ("university" → "univers").

**Notebook:** *Qual o tamanho ideal de um léxico?* — acurácia em função do
tamanho do léxico, usando o harness de avaliação.

---

## Aula 6 — Legibilidade e estilo: fórmulas por língua e comparação de traduções

**Objetivo:** usar métricas de superfície para comparar estilos — sabendo
que cada fórmula é calibrada para UMA língua.

**Conceitos:** sílabas e sentenças como aproximações de complexidade,
fórmulas calibradas (Flesch, Fernández Huerta, Kandel–Moles, Amstad,
Franchina–Vacca, Martins), comparação intra vs. inter-língua.

**Roteiro de tela:**
1. Modo *Compare two texts*: *Dom Casmurro Pt* vs. *Promessi Sposi It* —
   tabela lado a lado: língua detectada, diversidade, legibilidade (cada um
   na sua fórmula), sentimento, keywords.
2. Ponto crítico: NÃO comparar o número de legibilidade entre línguas —
   fórmulas e escalas diferentes (mostrar o caption de aviso).
3. Machado vs. Machado: colar dois capítulos diferentes e comparar o mesmo
   autor consigo mesmo — comparação legítima.

**Exercício:** escolher duas traduções de um mesmo texto (Gutenberg) e
escrever 3 conclusões defensáveis + 1 conclusão INDEFENSÁVEL (e explicar
por quê).

---

## Aula 7 — Como saber se funciona? Ouro, métricas e análise de erros

**Objetivo:** a aula-assinatura do curso — avaliar métodos como a
linguística computacional séria faz, e ler uma matriz de confusão como
quem lê um fenômeno linguístico.

**Conceitos:** padrão-ouro, acurácia, precisão/revocação/F1, macro-F1,
matriz de confusão, proveniência de dados, análise de erros
(inerente vs. corrigível).

**Roteiro de tela:**
1. Modo *Benchmarks*: as três tarefas, com n, SHA do dataset e commit —
   todo número é rastreável.
2. Ler a matriz de confusão do langid como linguista: fr→es 9 vezes. Por
   quê? "de", "que", "la" são pistas de TRÊS línguas românicas — a confusão
   é estrutural, herança do parentesco.
3. Abrir `docs/error-analysis.md`: a tabela inerente vs. corrigível.
   Mensagem final: método bom não é o que não erra — é o que tem os erros
   mapeados, medidos e explicados.

**Exercício final do curso:** escolher um método do toolbox, prever seus
dois piores tipos de erro, verificar no relatório — e propor (em prosa,
sem código) uma correção interpretável.
