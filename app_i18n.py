"""Bilingual (English / Brazilian Portuguese) didactic strings for the app.

Only on-screen *didactic* text is translated — code, APIs, tool names, metric
keys and JSON output stay English. This lets the recorded course read in
Portuguese while everything a developer touches stays language-neutral.

Structure:
* ``LANGUAGES``    — display name -> internal code ("en"/"pt"); order = UI order.
* ``THEME_ORDER``  — internal theme keys (English), used for grouping order.
* ``THEME_LABELS`` — per-language display label for each theme key.
* ``CARD_LABELS``  — per-language field labels used by the method cards.
* ``TOOL_CARDS``   — per-tool ``theme`` + ``en``/``pt`` what/how/why/explore.
* ``UI``           — per-language flat dict of every other on-screen string.

The tool names keying ``TOOL_CARDS`` are the same internal identifiers the app
uses everywhere else; ``en``/``pt`` sub-dicts always carry the same field keys.
"""

LANGUAGES: dict[str, str] = {"English": "en", "Português (BR)": "pt"}

THEME_ORDER: list[str] = [
    "Descriptive statistics",
    "Sentiment analysis",
    "Information extraction",
    "Language profile",
    "Text structure",
]

THEME_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "Descriptive statistics": "Descriptive statistics",
        "Sentiment analysis": "Sentiment analysis",
        "Information extraction": "Information extraction",
        "Language profile": "Language profile",
        "Text structure": "Text structure",
    },
    "pt": {
        "Descriptive statistics": "Estatística descritiva",
        "Sentiment analysis": "Análise de sentimento",
        "Information extraction": "Extração de informação",
        "Language profile": "Perfil linguístico",
        "Text structure": "Estrutura do texto",
    },
}

CARD_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "expander": "How this works: `{tool}`",
        "theme": "Theme",
        "what": "What it does",
        "how": "How it works",
        "why": "Why it matters",
        "explore": "Explore next",
    },
    "pt": {
        "expander": "Como funciona: `{tool}`",
        "theme": "Tema",
        "what": "O que faz",
        "how": "Como funciona",
        "why": "Por que importa",
        "explore": "Explore a seguir",
    },
}

TOOL_CARDS: dict[str, dict[str, object]] = {
    "analyze_text": {
        "theme": "Descriptive statistics",
        "en": {
            "what": "Counts and ratio-based summary metrics for the current text.",
            "how": (
                "Uses token and sentence counts to compute averages, lexical diversity, "
                "and reading-time estimate."
            ),
            "why": "Gives a fast baseline profile before deeper NLP modeling.",
            "explore": (
                "Compare lexical diversity and sentence length between authors, genres, "
                "or translations."
            ),
        },
        "pt": {
            "what": "Contagens e métricas-resumo baseadas em razões para o texto atual.",
            "how": (
                "Usa contagens de tokens e sentenças para calcular médias, diversidade "
                "lexical e uma estimativa de tempo de leitura."
            ),
            "why": "Dá um perfil de base rápido antes de modelagem de PLN mais profunda.",
            "explore": (
                "Compare diversidade lexical e tamanho de sentença entre autores, gêneros "
                "ou traduções."
            ),
        },
    },
    "split_sentences": {
        "theme": "Text structure",
        "en": {
            "what": "Rule-based sentence boundary detection.",
            "how": "Splits on whitespace that follows sentence-ending punctuation.",
            "why": "Creates sentence units for readability and downstream analysis.",
            "explore": "Benchmark this regex method against spaCy or Stanza sentence segmentation.",
        },
        "pt": {
            "what": "Detecção de fronteiras de sentença baseada em regras.",
            "how": "Divide no espaço em branco que segue pontuação de fim de sentença.",
            "why": "Cria unidades de sentença para legibilidade e análises posteriores.",
            "explore": "Compare este método por regex com a segmentação do spaCy ou do Stanza.",
        },
    },
    "tokenize_text": {
        "theme": "Text structure",
        "en": {
            "what": "Word-level tokenization.",
            "how": "Extracts unicode word-like chunks with a regular expression.",
            "why": "Produces the base representation used by most other tools.",
            "explore": "Compare regex tokens with subword tokenizers (BPE, WordPiece) on noisy text.",
        },
        "pt": {
            "what": "Tokenização em nível de palavra.",
            "how": "Extrai trechos semelhantes a palavras (unicode) com uma expressão regular.",
            "why": "Produz a representação-base usada pela maioria das outras ferramentas.",
            "explore": (
                "Compare os tokens por regex com tokenizadores de subpalavra (BPE, WordPiece) "
                "em texto ruidoso."
            ),
        },
    },
    "generate_ngrams": {
        "theme": "Text structure",
        "en": {
            "what": "Sequential phrase construction from tokens.",
            "how": "Builds contiguous windows of size N across the token list.",
            "why": "Captures local word order and common phrase patterns.",
            "explore": "Try skip-grams and PMI scoring to detect collocations beyond adjacency.",
        },
        "pt": {
            "what": "Construção de sequências de frases a partir dos tokens.",
            "how": "Monta janelas contíguas de tamanho N ao longo da lista de tokens.",
            "why": "Captura a ordem local das palavras e padrões frasais comuns.",
            "explore": (
                "Experimente skip-grams e pontuação por PMI para detectar colocações "
                "além da adjacência."
            ),
        },
    },
    "top_ngrams": {
        "theme": "Descriptive statistics",
        "en": {
            "what": "Most frequent N-gram ranking.",
            "how": "Counts generated N-grams and returns the highest-frequency entries.",
            "why": "Highlights repeated phrasing and stylistic motifs quickly.",
            "explore": "Track top N-grams over chapters or time slices for trend analysis.",
        },
        "pt": {
            "what": "Ranking dos N-gramas mais frequentes.",
            "how": "Conta os N-gramas gerados e retorna as entradas de maior frequência.",
            "why": "Destaca rapidamente repetições e motivos estilísticos.",
            "explore": "Acompanhe os N-gramas principais por capítulo ou período para ver tendências.",
        },
    },
    "extract_keywords": {
        "theme": "Information extraction",
        "en": {
            "what": "Frequency-based keyword extraction.",
            "how": "Removes stopwords and ranks remaining tokens by count.",
            "why": "Surfaces likely content-bearing terms without heavy models.",
            "explore": "Compare frequency keywords against TF-IDF, RAKE, and KeyBERT outputs.",
        },
        "pt": {
            "what": "Extração de palavras-chave por frequência.",
            "how": "Remove stopwords e ordena os tokens restantes pela contagem.",
            "why": "Revela termos provavelmente informativos sem modelos pesados.",
            "explore": "Compare as palavras-chave por frequência com TF-IDF, RAKE e KeyBERT.",
        },
    },
    "readability_score": {
        "theme": "Descriptive statistics",
        "en": {
            "what": "Readability estimate using a formula calibrated for the detected language.",
            "how": (
                "Words per sentence and estimated syllables per word, weighted by "
                "language-specific coefficients (Flesch EN, Fernández Huerta ES, "
                "Kandel–Moles FR, Amstad DE, Franchina–Vacca IT, Martins et al. PT)."
            ),
            "why": "Provides a rough complexity signal for educational and editorial use.",
            "explore": "Compare Flesch with SMOG and Dale-Chall on the same corpus.",
        },
        "pt": {
            "what": "Estimativa de legibilidade com fórmula calibrada para o idioma detectado.",
            "how": (
                "Palavras por sentença e sílabas estimadas por palavra, ponderadas por "
                "coeficientes específicos do idioma (Flesch EN, Fernández Huerta ES, "
                "Kandel–Moles FR, Amstad DE, Franchina–Vacca IT, Martins et al. PT)."
            ),
            "why": "Oferece um sinal aproximado de complexidade para uso didático e editorial.",
            "explore": "Compare o Flesch com o SMOG e o Dale-Chall no mesmo corpus.",
        },
    },
    "sentiment_analysis": {
        "theme": "Sentiment analysis",
        "en": {
            "what": "Lexicon-based sentiment snapshot.",
            "how": (
                "Counts hits from the hand-curated lexicon of the detected language "
                "(v1, ~75-100 words per polarity) and normalizes by token count. "
                "No negation handling - see docs/resources.md."
            ),
            "why": "Fast interpretable polarity estimate for teaching and quick diagnostics.",
            "explore": "Compare this lexicon baseline with VADER and transformer sentiment models.",
        },
        "pt": {
            "what": "Retrato de sentimento baseado em léxico.",
            "how": (
                "Conta ocorrências do léxico curado à mão do idioma detectado "
                "(v1, ~75-100 palavras por polaridade) e normaliza pela contagem de tokens. "
                "Sem tratamento de negação - ver docs/resources.md."
            ),
            "why": "Estimativa de polaridade rápida e interpretável para ensino e diagnóstico.",
            "explore": "Compare este baseline por léxico com o VADER e modelos transformer.",
        },
    },
    "word_length_distribution": {
        "theme": "Language profile",
        "en": {
            "what": "Histogram of token lengths.",
            "how": "Counts how many filtered tokens have each character length.",
            "why": "Reveals writing style and lexical complexity patterns.",
            "explore": "Contrast distributions across languages and reading levels.",
        },
        "pt": {
            "what": "Histograma dos tamanhos de token.",
            "how": "Conta quantos tokens filtrados têm cada comprimento em caracteres.",
            "why": "Revela padrões de estilo de escrita e complexidade lexical.",
            "explore": "Contraste as distribuições entre idiomas e níveis de leitura.",
        },
    },
    "detect_language": {
        "theme": "Language profile",
        "en": {
            "what": "Hint-based language detection.",
            "how": "Tokenizes text and scores each language by overlap with language hint sets.",
            "why": "Provides a transparent automatic language pick for the pipeline.",
            "explore": "Compare hint matching with fastText language ID on short vs long text.",
        },
        "pt": {
            "what": "Detecção de idioma por palavras-indício.",
            "how": (
                "Tokeniza o texto e pontua cada idioma pela sobreposição com os conjuntos "
                "de palavras-indício."
            ),
            "why": "Oferece uma escolha automática e transparente de idioma para o pipeline.",
            "explore": (
                "Compare a correspondência por indícios com o fastText em textos curtos e longos."
            ),
        },
    },
    "language_hint_hits": {
        "theme": "Language profile",
        "en": {
            "what": "Per-language evidence table showing the exact words that matched.",
            "how": (
                "Counts matched tokens from each language hint vocabulary and lists "
                "each matching word with its number of occurrences."
            ),
            "why": "Explains why auto-detection favored one language over another, word by word.",
            "explore": "Add confusion tests for mixed-language and code-switched inputs.",
        },
        "pt": {
            "what": "Tabela de evidências por idioma mostrando as palavras exatas que corresponderam.",
            "how": (
                "Conta os tokens correspondentes em cada vocabulário de indícios e lista "
                "cada palavra correspondente com seu número de ocorrências."
            ),
            "why": "Explica, palavra por palavra, por que a autodetecção favoreceu um idioma.",
            "explore": "Adicione testes de confusão para entradas multilíngues e com code-switching.",
        },
    },
    "tfidf_keywords": {
        "theme": "Information extraction",
        "en": {
            "what": "TF-IDF keyword ranking, using sentences as documents.",
            "how": (
                "score(t) = tf(t) x log10(N/df(t)): total frequency weighted down "
                "when a term appears in many sentences."
            ),
            "why": (
                "Shows why plain frequency overrates ubiquitous words - "
                "the classic step beyond counting."
            ),
            "explore": "Compare freq vs TF-IDF rankings side by side; then try BM25 and KeyBERT.",
        },
        "pt": {
            "what": "Ranking de palavras-chave por TF-IDF, usando sentenças como documentos.",
            "how": (
                "score(t) = tf(t) x log10(N/df(t)): a frequência total é reduzida "
                "quando o termo aparece em muitas sentenças."
            ),
            "why": (
                "Mostra por que a frequência pura superestima palavras onipresentes - "
                "o passo clássico além da contagem."
            ),
            "explore": "Compare os rankings de frequência e TF-IDF lado a lado; depois BM25 e KeyBERT.",
        },
    },
    "kwic": {
        "theme": "Text structure",
        "en": {
            "what": "Keyword-in-context concordance (KWIC).",
            "how": (
                "Finds case-insensitive whole-token matches and shows a window of surrounding tokens."
            ),
            "why": (
                "The classic corpus-linguistics view: see how a word is actually used "
                "before trusting any statistic about it."
            ),
            "explore": "Compare contexts of near-synonyms, or the same word across two texts.",
        },
        "pt": {
            "what": "Concordância de palavra-em-contexto (KWIC).",
            "how": (
                "Encontra correspondências de token inteiro (sem distinguir maiúsculas) e "
                "mostra uma janela de tokens ao redor."
            ),
            "why": (
                "A visão clássica da linguística de corpus: veja como a palavra é de fato "
                "usada antes de confiar em qualquer estatística sobre ela."
            ),
            "explore": "Compare os contextos de quase-sinônimos, ou da mesma palavra em dois textos.",
        },
    },
    "zipf_table": {
        "theme": "Descriptive statistics",
        "en": {
            "what": "Rank-frequency table and plot (Zipf's law).",
            "how": (
                "Sorts tokens by frequency; rank 1 = most frequent. Natural text gives "
                "a straight line in log-log scale (slope near -1)."
            ),
            "why": (
                "One of the most robust empirical laws of language - "
                "and a two-minute sanity check of any corpus."
            ),
            "explore": "Compare the slope across languages and against shuffled or synthetic text.",
        },
        "pt": {
            "what": "Tabela e gráfico de frequência por posto (lei de Zipf).",
            "how": (
                "Ordena os tokens por frequência; posto 1 = mais frequente. Texto natural "
                "dá uma reta em escala log-log (inclinação perto de -1)."
            ),
            "why": (
                "Uma das leis empíricas mais robustas da língua - "
                "e uma checagem de sanidade de dois minutos para qualquer corpus."
            ),
            "explore": "Compare a inclinação entre idiomas e contra texto embaralhado ou sintético.",
        },
    },
    "vocabulary_growth": {
        "theme": "Descriptive statistics",
        "en": {
            "what": "Vocabulary size as the text is read (type-token growth).",
            "how": "Counts distinct tokens after every N tokens seen.",
            "why": "Flattening growth (Heaps' law) reveals lexical richness and text homogeneity.",
            "explore": "Compare authors or translations of the same work.",
        },
        "pt": {
            "what": "Tamanho do vocabulário conforme o texto é lido (crescimento tipo-ocorrência).",
            "how": "Conta os tokens distintos a cada N tokens vistos.",
            "why": (
                "O achatamento do crescimento (lei de Heaps) revela riqueza lexical e "
                "homogeneidade do texto."
            ),
            "explore": "Compare autores ou traduções da mesma obra.",
        },
    },
    "collocations": {
        "theme": "Information extraction",
        "en": {
            "what": "Collocations: adjacent word pairs ranked by log-likelihood (with PMI).",
            "how": (
                "PMI = log2(p(xy)/(p(x)p(y))) rewards pairs that co-occur beyond chance; "
                "LLR (Dunning 1993) keeps rare-pair noise under control via a min-count floor."
            ),
            "why": "Fixed expressions and multiword units are invisible to single-word counts.",
            "explore": "Compare PMI vs LLR rankings; try window-based (non-adjacent) collocations.",
        },
        "pt": {
            "what": "Colocações: pares de palavras adjacentes ordenados por log-verossimilhança (com PMI).",
            "how": (
                "PMI = log2(p(xy)/(p(x)p(y))) premia pares que coocorrem além do acaso; "
                "a LLR (Dunning 1993) controla o ruído de pares raros com um piso de contagem."
            ),
            "why": "Expressões fixas e unidades multipalavra são invisíveis à contagem de palavras isoladas.",
            "explore": "Compare os rankings PMI e LLR; experimente colocações por janela (não adjacentes).",
        },
    },
    "detect_language_ngram": {
        "theme": "Language profile",
        "en": {
            "what": "Character n-gram language detection (Cavnar-Trenkle 1994).",
            "how": (
                "Builds the text's ranked trigram profile and measures the out-of-place "
                "distance to each language's stored profile (trained on Wikipedia extracts)."
            ),
            "why": (
                "Character statistics exist in every token, so short texts still carry "
                "evidence - measured: 61% vs 29% accuracy on 2-word inputs."
            ),
            "explore": "Inspect the shipped profiles in nlp_toolbox/resources/ngram_profiles/.",
        },
        "pt": {
            "what": "Detecção de idioma por n-gramas de caractere (Cavnar-Trenkle 1994).",
            "how": (
                "Constrói o perfil de trigramas ordenado do texto e mede a distância "
                "out-of-place ao perfil de cada idioma (treinado com extratos da Wikipédia)."
            ),
            "why": (
                "Estatísticas de caractere existem em todo token, então textos curtos ainda "
                "carregam evidência - medido: 61% vs 29% de acurácia em entradas de 2 palavras."
            ),
            "explore": "Inspecione os perfis em nlp_toolbox/resources/ngram_profiles/.",
        },
    },
    "porter_stem": {
        "theme": "Text structure",
        "en": {
            "what": "Porter stemmer (English): rule-based suffix stripping.",
            "how": "Five ordered rule steps conditioned on the measure (vowel-consonant patterns).",
            "why": (
                "The classic worked example of rule-based morphology - including its "
                "famous over-stemming: university and universal collide into univers."
            ),
            "explore": "Compare with lemmatization; try Snowball stemmers for other languages.",
        },
        "pt": {
            "what": "Stemmer de Porter (inglês): remoção de sufixos baseada em regras.",
            "how": (
                "Cinco etapas de regras ordenadas, condicionadas à medida "
                "(padrões vogal-consoante)."
            ),
            "why": (
                "O exemplo clássico de morfologia baseada em regras - incluindo seu famoso "
                "excesso de radicalização: university e universal colidem em univers."
            ),
            "explore": "Compare com lematização; experimente stemmers Snowball para outros idiomas.",
        },
    },
    "filter_tokens": {
        "theme": "Text structure",
        "en": {
            "what": "Token cleaning and pruning.",
            "how": "Optionally removes stopwords and short tokens based on user controls.",
            "why": "Reduces noise so counts and rankings reflect content terms.",
            "explore": "Evaluate stemming/lemmatization and domain-specific stopword lists.",
        },
        "pt": {
            "what": "Limpeza e poda de tokens.",
            "how": "Opcionalmente remove stopwords e tokens curtos conforme os controles do usuário.",
            "why": "Reduz o ruído para que contagens e rankings reflitam termos de conteúdo.",
            "explore": "Avalie stemming/lematização e listas de stopwords específicas de domínio.",
        },
    },
}

UI: dict[str, dict[str, str]] = {
    "en": {
        "interface_language": "Interface language",
        "intro": (
            "Upload a text file or paste raw text, then explore NLP techniques across "
            "multiple languages."
        ),
        "intro_caption": (
            "This interface is organized by NLP themes and includes method cards to explain "
            "what each tool does, how it works, and where to explore next."
        ),
        "mode_analyze": "Analyze",
        "mode_compare": "Compare two texts",
        "mode_benchmarks": "Benchmarks",
        "sidebar_input": "Input",
        "upload": "Upload a text file",
        "paste": "Or paste raw text",
        "sample": "Or load a sample text",
        "sample_none": "None",
        "analysis_language": "Analysis language",
        "auto_detector": "Auto detector",
        "auto_detector_ngram": "Character n-grams (recommended)",
        "auto_detector_hints": "Hint words (baseline)",
        "auto_detector_help": (
            "Which detector drives analysis in Auto mode (stopwords, readability, sentiment, "
            "language config). Char n-grams scored 98.9% vs 75.6% for hint words on the "
            "language-ID benchmark. Hint words stay available as a transparent, inspectable "
            "baseline."
        ),
        "customizations": "Customizations",
        "lowercase": "Lowercase tokens",
        "remove_stopwords": "Remove stopwords",
        "min_token_length": "Minimum token length",
        "tokens_preview": "Tokens to preview",
        "tools": "Tools",
        "cb_basic_stats": "Basic stats",
        "cb_sentences": "Sentence splitting",
        "cb_tokens": "Tokenization",
        "cb_ngrams": "N-grams",
        "cb_keywords": "Keyword extraction",
        "cb_top_ngrams": "Top N-grams",
        "cb_readability": "Readability",
        "cb_sentiment": "Sentiment snapshot",
        "cb_word_lengths": "Word length distribution",
        "cb_zipf": "Zipf rank-frequency",
        "cb_vocab_growth": "Vocabulary growth",
        "cb_tfidf": "TF-IDF keywords",
        "cb_kwic": "KWIC concordance",
        "cb_collocations": "Collocations (PMI/LLR)",
        "cb_stems": "Porter stems (English)",
        "cb_language_hints": "Language hint matches",
        "tab_descriptive": "Descriptive statistics",
        "tab_structure": "Text structure",
        "tab_extraction": "Information extraction",
        "tab_sentiment": "Sentiment analysis",
        "tab_language": "Language profile",
        "tab_catalog": "Method catalog",
        "detected_language": "Detected language",
        "active_detector": "Active detector: **{detector}** — drives every language-dependent method.",
        "detector_ngram_name": "char n-grams (Cavnar-Trenkle)",
        "detector_hints_name": "hint words",
        "compare_hints": "For comparison, hint words say: **{language}**",
        "compare_ngram": "For comparison, char n-grams say: **{language}**",
        "fallback_ngram": "No letters found - defaulted to English (documented fallback).",
        "fallback_hints": "No hint word matched - defaulted to English (documented fallback).",
        "tie_note": "Tie with {langs} - resolved by fixed language order.",
        "h_basic_stats": "Basic stats",
        "h_readability": "Readability",
        "readability_caption": "Language-calibrated formula. Reference: {reference}",
        "h_top_ngrams": "Top N-grams",
        "top_ngram_size": "Top N-gram size",
        "top_ngram_count": "Top N-grams",
        "h_word_lengths": "Word length distribution",
        "h_zipf": "Zipf rank-frequency",
        "zipf_caption": "x-axis: rank (log-spaced in nature; linear here). Straightish descent = Zipf.",
        "h_vocab_growth": "Vocabulary growth",
        "vocab_growth_label": "vocabulary size",
        "h_sentences": "Sentence splitting",
        "sentences_caption": "Showing {shown} of {total} sentences",
        "h_tokens": "Tokens",
        "tokens_caption": "Showing {shown} of {total} tokens",
        "h_stems": "Porter stems (English)",
        "h_kwic": "KWIC concordance",
        "kwic_keyword": "Keyword",
        "kwic_window": "Context window (tokens)",
        "kwic_matches": "{count} match(es)",
        "h_ngrams": "N-grams",
        "ngrams_n": "N",
        "ngrams_caption": "Showing {shown} of {total} n-grams",
        "h_keywords": "Keywords",
        "keyword_count": "Top keywords",
        "keywords_freq": "**Frequency** (stopwords removed)",
        "keywords_tfidf": "**TF-IDF** (sentences as documents)",
        "h_collocations": "Collocations",
        "colloc_min_count": "Minimum pair frequency",
        "colloc_over_filtered": "Collocations over filtered token sequence",
        "colloc_filtered_caption": (
            "Adjacency may differ from the original text: stopwords and short tokens were "
            "removed before pairing."
        ),
        "colloc_original_caption": "Adjacent bigrams over the original token sequence.",
        "h_sentiment": "Sentiment snapshot",
        "h_ngram_detection": "Char n-gram detection",
        "ngram_closest": "**{language}** — closest profile (lowest distance)",
        "distance_caption": (
            "Out-of-place distance: LOWER = closer to the language profile. Rank 1 is the "
            "detector's pick."
        ),
        "distance_fallback": "No letters in the text - defaulted to English (documented fallback).",
        "col_rank": "Rank",
        "col_language": "Language",
        "col_distance": "Distance",
        "col_closest": "Closest",
        "closest_marker": "◀ closest",
        "h_language_hints": "Language hint matches",
        "col_hits": "Hits",
        "col_matched": "Matched words",
        "hint_evidence_caption": (
            "Full explainability: these are the exact words that scored for each language. "
            "The winning language is simply the row with the most hits."
        ),
        "h_catalog": "NLP method catalog",
        "catalog_intro": "Use this as a map of all tools available in this app, grouped by theme.",
        "export_button": "Export analysis (JSON)",
        "get_started": "Upload a text file or paste text to get started.",
        "benchmarks_header": "Benchmarks",
        "benchmarks_intro": (
            "Toolbox baselines measured against external systems on small, licensed, frozen "
            "datasets. Reproduce: `uv sync --group evals && uv run python -m evals.run "
            "--task <task>`."
        ),
        "benchmarks_none": "No eval results found. Run the eval harness to generate them.",
        "benchmarks_provenance": (
            "Dataset provenance: `evals/DATASETS.md` · failure analysis: `docs/error-analysis.md`"
        ),
        "compare_header": "Compare two texts",
        "compare_caption": "Two translations, two authors, two registers — every metric side by side.",
        "compare_sample": "Sample {label}",
        "compare_paste": "(paste below)",
        "compare_text": "Text {label}",
        "compare_need_both": "Provide both texts to compare.",
        "compare_readability_note": (
            "Readability formulas differ per language — compare readability across texts only "
            "when both are in the same language (see docs/error-analysis.md)."
        ),
        "compare_top_keywords": "**Top keywords {label}:** {keywords}",
    },
    "pt": {
        "interface_language": "Idioma da interface",
        "intro": (
            "Envie um arquivo de texto ou cole texto bruto e explore técnicas de PLN em "
            "vários idiomas."
        ),
        "intro_caption": (
            "Esta interface é organizada por temas de PLN e inclui cartões de método que "
            "explicam o que cada ferramenta faz, como funciona e para onde explorar em seguida."
        ),
        "mode_analyze": "Analisar",
        "mode_compare": "Comparar dois textos",
        "mode_benchmarks": "Benchmarks",
        "sidebar_input": "Entrada",
        "upload": "Envie um arquivo de texto",
        "paste": "Ou cole texto bruto",
        "sample": "Ou carregue um texto de exemplo",
        "sample_none": "Nenhum",
        "analysis_language": "Idioma da análise",
        "auto_detector": "Detector automático",
        "auto_detector_ngram": "N-gramas de caractere (recomendado)",
        "auto_detector_hints": "Palavras-indício (baseline)",
        "auto_detector_help": (
            "Qual detector conduz a análise no modo Auto (stopwords, legibilidade, sentimento, "
            "configuração do idioma). Os n-gramas de caractere obtiveram 98,9% vs 75,6% das "
            "palavras-indício no benchmark de identificação de idioma. As palavras-indício "
            "seguem disponíveis como baseline transparente e inspecionável."
        ),
        "customizations": "Personalizações",
        "lowercase": "Tokens em minúsculas",
        "remove_stopwords": "Remover stopwords",
        "min_token_length": "Tamanho mínimo do token",
        "tokens_preview": "Tokens para pré-visualizar",
        "tools": "Ferramentas",
        "cb_basic_stats": "Estatísticas básicas",
        "cb_sentences": "Segmentação de sentenças",
        "cb_tokens": "Tokenização",
        "cb_ngrams": "N-gramas",
        "cb_keywords": "Extração de palavras-chave",
        "cb_top_ngrams": "N-gramas mais frequentes",
        "cb_readability": "Legibilidade",
        "cb_sentiment": "Retrato de sentimento",
        "cb_word_lengths": "Distribuição de tamanho de palavra",
        "cb_zipf": "Frequência por posto (Zipf)",
        "cb_vocab_growth": "Crescimento do vocabulário",
        "cb_tfidf": "Palavras-chave TF-IDF",
        "cb_kwic": "Concordância KWIC",
        "cb_collocations": "Colocações (PMI/LLR)",
        "cb_stems": "Radicais de Porter (inglês)",
        "cb_language_hints": "Correspondências de indícios de idioma",
        "tab_descriptive": "Estatística descritiva",
        "tab_structure": "Estrutura do texto",
        "tab_extraction": "Extração de informação",
        "tab_sentiment": "Análise de sentimento",
        "tab_language": "Perfil linguístico",
        "tab_catalog": "Catálogo de métodos",
        "detected_language": "Idioma detectado",
        "active_detector": "Detector ativo: **{detector}** — conduz todo método dependente de idioma.",
        "detector_ngram_name": "n-gramas de caractere (Cavnar-Trenkle)",
        "detector_hints_name": "palavras-indício",
        "compare_hints": "Para comparação, as palavras-indício indicam: **{language}**",
        "compare_ngram": "Para comparação, os n-gramas de caractere indicam: **{language}**",
        "fallback_ngram": "Nenhuma letra encontrada - assumiu inglês (fallback documentado).",
        "fallback_hints": "Nenhuma palavra-indício correspondeu - assumiu inglês (fallback documentado).",
        "tie_note": "Empate com {langs} - resolvido pela ordem fixa de idiomas.",
        "h_basic_stats": "Estatísticas básicas",
        "h_readability": "Legibilidade",
        "readability_caption": "Fórmula calibrada por idioma. Referência: {reference}",
        "h_top_ngrams": "N-gramas mais frequentes",
        "top_ngram_size": "Tamanho do N-grama",
        "top_ngram_count": "Quantos N-gramas",
        "h_word_lengths": "Distribuição de tamanho de palavra",
        "h_zipf": "Frequência por posto (Zipf)",
        "zipf_caption": ("eixo x: posto (log na natureza; linear aqui). Queda quase reta = Zipf."),
        "h_vocab_growth": "Crescimento do vocabulário",
        "vocab_growth_label": "tamanho do vocabulário",
        "h_sentences": "Segmentação de sentenças",
        "sentences_caption": "Mostrando {shown} de {total} sentenças",
        "h_tokens": "Tokens",
        "tokens_caption": "Mostrando {shown} de {total} tokens",
        "h_stems": "Radicais de Porter (inglês)",
        "h_kwic": "Concordância KWIC",
        "kwic_keyword": "Palavra-chave",
        "kwic_window": "Janela de contexto (tokens)",
        "kwic_matches": "{count} ocorrência(s)",
        "h_ngrams": "N-gramas",
        "ngrams_n": "N",
        "ngrams_caption": "Mostrando {shown} de {total} n-gramas",
        "h_keywords": "Palavras-chave",
        "keyword_count": "Palavras-chave principais",
        "keywords_freq": "**Frequência** (stopwords removidas)",
        "keywords_tfidf": "**TF-IDF** (sentenças como documentos)",
        "h_collocations": "Colocações",
        "colloc_min_count": "Frequência mínima do par",
        "colloc_over_filtered": "Colocações sobre a sequência de tokens filtrada",
        "colloc_filtered_caption": (
            "A adjacência pode diferir do texto original: stopwords e tokens curtos foram "
            "removidos antes do emparelhamento."
        ),
        "colloc_original_caption": "Bigramas adjacentes sobre a sequência de tokens original.",
        "h_sentiment": "Retrato de sentimento",
        "h_ngram_detection": "Detecção por n-gramas de caractere",
        "ngram_closest": "**{language}** — perfil mais próximo (menor distância)",
        "distance_caption": (
            "Distância out-of-place: MENOR = mais próximo do perfil do idioma. O posto 1 é a "
            "escolha do detector."
        ),
        "distance_fallback": "Nenhuma letra no texto - assumiu inglês (fallback documentado).",
        "col_rank": "Posto",
        "col_language": "Idioma",
        "col_distance": "Distância",
        "col_closest": "Mais próximo",
        "closest_marker": "◀ mais próximo",
        "h_language_hints": "Correspondências de indícios de idioma",
        "col_hits": "Ocorrências",
        "col_matched": "Palavras correspondentes",
        "hint_evidence_caption": (
            "Explicabilidade total: estas são exatamente as palavras que pontuaram para cada "
            "idioma. O idioma vencedor é simplesmente a linha com mais ocorrências."
        ),
        "h_catalog": "Catálogo de métodos de PLN",
        "catalog_intro": (
            "Use isto como um mapa de todas as ferramentas do app, agrupadas por tema."
        ),
        "export_button": "Exportar análise (JSON)",
        "get_started": "Envie um arquivo de texto ou cole texto para começar.",
        "benchmarks_header": "Benchmarks",
        "benchmarks_intro": (
            "Baselines do toolbox medidos contra sistemas externos em conjuntos pequenos, "
            "licenciados e congelados. Reproduza: `uv sync --group evals && uv run python -m "
            "evals.run --task <task>`."
        ),
        "benchmarks_none": "Nenhum resultado de avaliação encontrado. Rode o harness para gerá-los.",
        "benchmarks_provenance": (
            "Proveniência dos dados: `evals/DATASETS.md` · análise de erros: `docs/error-analysis.md`"
        ),
        "compare_header": "Comparar dois textos",
        "compare_caption": (
            "Duas traduções, dois autores, dois registros — cada métrica lado a lado."
        ),
        "compare_sample": "Exemplo {label}",
        "compare_paste": "(cole abaixo)",
        "compare_text": "Texto {label}",
        "compare_need_both": "Forneça os dois textos para comparar.",
        "compare_readability_note": (
            "As fórmulas de legibilidade diferem por idioma — compare a legibilidade entre "
            "textos apenas quando ambos estiverem no mesmo idioma (ver docs/error-analysis.md)."
        ),
        "compare_top_keywords": "**Palavras-chave principais {label}:** {keywords}",
    },
}
