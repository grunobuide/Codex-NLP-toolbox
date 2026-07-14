import json
import math
from pathlib import Path

import streamlit as st

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    READABILITY_FORMULAS,
    analyze_text,
    detect_language_details,
    extract_keywords,
    filter_tokens,
    generate_ngrams,
    kwic,
    language_hint_hits,
    readability_score,
    sentiment_analysis,
    split_sentences,
    tfidf_keywords,
    tokenize_text,
    top_ngrams,
    vocabulary_growth,
    word_length_distribution,
    zipf_table,
)

st.set_page_config(page_title="Codex NLP Toolbox", layout="wide")

TOOL_EXPLANATIONS = {
    "analyze_text": {
        "theme": "Descriptive statistics",
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
    "split_sentences": {
        "theme": "Text structure",
        "what": "Rule-based sentence boundary detection.",
        "how": "Splits on whitespace that follows sentence-ending punctuation.",
        "why": "Creates sentence units for readability and downstream analysis.",
        "explore": "Benchmark this regex method against spaCy or Stanza sentence segmentation.",
    },
    "tokenize_text": {
        "theme": "Text structure",
        "what": "Word-level tokenization.",
        "how": "Extracts unicode word-like chunks with a regular expression.",
        "why": "Produces the base representation used by most other tools.",
        "explore": "Compare regex tokens with subword tokenizers (BPE, WordPiece) on noisy text.",
    },
    "generate_ngrams": {
        "theme": "Text structure",
        "what": "Sequential phrase construction from tokens.",
        "how": "Builds contiguous windows of size N across the token list.",
        "why": "Captures local word order and common phrase patterns.",
        "explore": "Try skip-grams and PMI scoring to detect collocations beyond adjacency.",
    },
    "top_ngrams": {
        "theme": "Descriptive statistics",
        "what": "Most frequent N-gram ranking.",
        "how": "Counts generated N-grams and returns the highest-frequency entries.",
        "why": "Highlights repeated phrasing and stylistic motifs quickly.",
        "explore": "Track top N-grams over chapters or time slices for trend analysis.",
    },
    "extract_keywords": {
        "theme": "Information extraction",
        "what": "Frequency-based keyword extraction.",
        "how": "Removes stopwords and ranks remaining tokens by count.",
        "why": "Surfaces likely content-bearing terms without heavy models.",
        "explore": "Compare frequency keywords against TF-IDF, RAKE, and KeyBERT outputs.",
    },
    "readability_score": {
        "theme": "Descriptive statistics",
        "what": "Readability estimate using a formula calibrated for the detected language.",
        "how": (
            "Words per sentence and estimated syllables per word, weighted by "
            "language-specific coefficients (Flesch EN, Fernández Huerta ES, "
            "Kandel–Moles FR, Amstad DE, Franchina–Vacca IT, Martins et al. PT)."
        ),
        "why": "Provides a rough complexity signal for educational and editorial use.",
        "explore": "Compare Flesch with SMOG and Dale-Chall on the same corpus.",
    },
    "sentiment_analysis": {
        "theme": "Sentiment analysis",
        "what": "Lexicon-based sentiment snapshot.",
        "how": (
            "Counts hits from the hand-curated lexicon of the detected language "
            "(v1, ~75-100 words per polarity) and normalizes by token count. "
            "No negation handling - see docs/resources.md."
        ),
        "why": "Fast interpretable polarity estimate for teaching and quick diagnostics.",
        "explore": "Compare this lexicon baseline with VADER and transformer sentiment models.",
    },
    "word_length_distribution": {
        "theme": "Language profile",
        "what": "Histogram of token lengths.",
        "how": "Counts how many filtered tokens have each character length.",
        "why": "Reveals writing style and lexical complexity patterns.",
        "explore": "Contrast distributions across languages and reading levels.",
    },
    "detect_language": {
        "theme": "Language profile",
        "what": "Hint-based language detection.",
        "how": "Tokenizes text and scores each language by overlap with language hint sets.",
        "why": "Provides a transparent automatic language pick for the pipeline.",
        "explore": "Compare hint matching with fastText language ID on short vs long text.",
    },
    "language_hint_hits": {
        "theme": "Language profile",
        "what": "Per-language evidence table.",
        "how": "Counts matched tokens from each language hint vocabulary.",
        "why": "Explains why auto-detection favored one language over another.",
        "explore": "Add confusion tests for mixed-language and code-switched inputs.",
    },
    "tfidf_keywords": {
        "theme": "Information extraction",
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
    "kwic": {
        "theme": "Text structure",
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
    "zipf_table": {
        "theme": "Descriptive statistics",
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
    "vocabulary_growth": {
        "theme": "Descriptive statistics",
        "what": "Vocabulary size as the text is read (type-token growth).",
        "how": "Counts distinct tokens after every N tokens seen.",
        "why": "Flattening growth (Heaps' law) reveals lexical richness and text homogeneity.",
        "explore": "Compare authors or translations of the same work.",
    },
    "filter_tokens": {
        "theme": "Text structure",
        "what": "Token cleaning and pruning.",
        "how": "Optionally removes stopwords and short tokens based on user controls.",
        "why": "Reduces noise so counts and rankings reflect content terms.",
        "explore": "Evaluate stemming/lemmatization and domain-specific stopword lists.",
    },
}

THEME_GROUPS = [
    "Descriptive statistics",
    "Sentiment analysis",
    "Information extraction",
    "Language profile",
    "Text structure",
]


def render_tool_explanation(tool_name: str) -> None:
    details = TOOL_EXPLANATIONS[tool_name]
    with st.expander(f"How this works: `{tool_name}`", expanded=False):
        st.markdown(f"- **Theme:** {details['theme']}")
        st.markdown(f"- **What it does:** {details['what']}")
        st.markdown(f"- **How it works:** {details['how']}")
        st.markdown(f"- **Why it matters:** {details['why']}")
        st.markdown(f"- **Explore next:** {details['explore']}")


st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, rgba(224, 123, 255, 0.12), transparent 45%),
                    radial-gradient(circle at 20% 20%, rgba(110, 241, 255, 0.12), transparent 40%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(34, 26, 46, 0.7);
        border-radius: 999px;
        padding: 0.35rem 0.6rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #e9dbff;
        border-radius: 999px;
        padding: 0.35rem 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(224, 123, 255, 0.2);
        border: 1px solid rgba(224, 123, 255, 0.35);
    }
    section[data-testid="stSidebar"] {
        background: rgba(20, 16, 26, 0.92);
        border-right: 1px solid rgba(224, 123, 255, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Codex NLP Toolbox")
st.write(
    "Upload a text file or paste raw text, then explore NLP techniques across multiple languages."
)
st.caption(
    "This interface is organized by NLP themes and includes method cards "
    "to explain what each tool does, how it works, and where to explore next."
)


@st.cache_data
def _load_samples() -> dict[str, str]:
    """Licensed sample texts (provenance: data/samples/README.md), truncated for the UI."""
    samples_dir = Path(__file__).parent / "data" / "samples"
    out: dict[str, str] = {}
    if samples_dir.exists():
        for file in sorted(samples_dir.glob("*.txt")):
            text = file.read_text(encoding="utf-8", errors="replace")[:4000]
            out[file.stem.replace("_", " ").title()] = text
    return out


SAMPLES = _load_samples()


def render_benchmarks() -> None:
    st.markdown("### Benchmarks")
    st.write(
        "Toolbox baselines measured against external systems on small, licensed, "
        "frozen datasets. Reproduce: `uv sync --group evals && "
        "uv run python -m evals.run --task <task>`."
    )
    results_dir = Path(__file__).parent / "evals" / "results"
    result_files = sorted(results_dir.glob("*.json")) if results_dir.exists() else []
    if not result_files:
        st.info("No eval results found. Run the eval harness to generate them.")
        return
    for result_file in result_files:
        data = json.loads(result_file.read_text(encoding="utf-8"))
        st.subheader(data["task"])
        st.caption(
            f"dataset `{data['dataset']['path']}` (n={data['dataset']['n']}) · "
            f"commit `{data['git_sha'][:10]}` · {data['timestamp_utc']}"
        )
        rows = []
        for name, scores in data["systems"].items():
            row: dict[str, object] = {"system": name}
            row.update(
                {key: value for key, value in scores.items() if isinstance(value, int | float)}
            )
            rows.append(row)
        st.dataframe(rows, use_container_width=True)
    st.caption(
        "Dataset provenance: `evals/DATASETS.md` · failure analysis: `docs/error-analysis.md`"
    )


def render_compare() -> None:
    st.markdown("### Compare two texts")
    st.caption("Two translations, two authors, two registers — every metric side by side.")
    columns = st.columns(2)
    texts: dict[str, str] = {}
    for label, column in zip(("A", "B"), columns, strict=True):
        with column:
            choice = st.selectbox(
                f"Sample {label}", ["(paste below)", *SAMPLES], key=f"sample_{label}"
            )
            default = SAMPLES.get(choice, "")
            # key includes the choice so switching samples refreshes the widget
            texts[label] = st.text_area(
                f"Text {label}", value=default, height=150, key=f"text_{label}_{choice}"
            )
    if not (texts["A"].strip() and texts["B"].strip()):
        st.info("Provide both texts to compare.")
        return
    metric_rows: list[dict[str, object]] = []
    keyword_summary: dict[str, str] = {}
    for label, text in texts.items():
        detection = detect_language_details(text)
        language = detection.language
        config = get_language_config(language)
        sentences = split_sentences(text)
        tokens = tokenize_text(text)
        content_tokens = filter_tokens(tokens, config)
        stats = analyze_text(text, tokens, sentences)
        sentiment = sentiment_analysis(tokens, language)
        keyword_summary[label] = ", ".join(
            str(row["term"]) for row in extract_keywords(content_tokens, config, top_k=6)
        )
        column_values: dict[str, object] = {
            "language (detected)": language,
            "words": stats["words"],
            "sentences": stats["sentences"],
            "avg sentence length": stats["avg_sentence_length"],
            "lexical diversity": stats["lexical_diversity"],
            "readability (language formula)": readability_score(text, tokens, sentences, language),
            "sentiment score": sentiment["score"],
        }
        if not metric_rows:
            metric_rows = [{"metric": key} for key in column_values]
        for row in metric_rows:
            row[f"Text {label}"] = column_values[str(row["metric"])]
    st.dataframe(metric_rows, use_container_width=True)
    st.caption(
        "Readability formulas differ per language — compare readability across texts "
        "only when both are in the same language (see docs/error-analysis.md)."
    )
    for label in ("A", "B"):
        st.markdown(f"**Top keywords {label}:** {keyword_summary[label]}")


mode = st.radio(
    "Mode",
    ["Analyze", "Compare two texts", "Benchmarks"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "Benchmarks":
    render_benchmarks()
elif mode == "Compare two texts":
    render_compare()
else:
    with st.sidebar:
        st.header("Input")
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
        text_input = st.text_area("Or paste raw text", height=200)
        sample_names = list(SAMPLES)
        sample_choice = st.selectbox("Or load a sample text", ["None", *sample_names])
        language_choice = st.selectbox("Language", options=["Auto"] + LANGUAGE_OPTIONS, index=0)
        st.header("Customizations")
        lowercase_tokens = st.checkbox("Lowercase tokens", value=True)
        remove_stopwords = st.checkbox("Remove stopwords", value=True)
        min_token_length = st.slider("Minimum token length", 1, 8, 1)
        max_preview_tokens = st.slider("Tokens to preview", 10, 200, 50, step=10)
        st.header("Tools")
        show_analysis = st.checkbox("Basic stats", value=True)
        show_sentences = st.checkbox("Sentence splitting", value=True)
        show_tokens = st.checkbox("Tokenization", value=True)
        show_ngrams = st.checkbox("N-grams", value=False)
        show_keywords = st.checkbox("Keyword extraction", value=True)
        show_top_ngrams = st.checkbox("Top N-grams", value=True)
        show_readability = st.checkbox("Readability", value=True)
        show_sentiment = st.checkbox("Sentiment snapshot", value=True)
        show_word_lengths = st.checkbox("Word length distribution", value=True)
        show_zipf = st.checkbox("Zipf rank-frequency", value=False)
        show_vocab_growth = st.checkbox("Vocabulary growth", value=False)
        show_tfidf = st.checkbox("TF-IDF keywords", value=True)
        show_kwic = st.checkbox("KWIC concordance", value=False)
        show_language_hints = st.checkbox("Language hint matches", value=False)

    text_content = ""
    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8", errors="ignore")
    elif text_input.strip():
        text_content = text_input
    elif sample_choice != "None":
        text_content = SAMPLES[sample_choice]

    if text_content.strip():
        detection = detect_language_details(text_content)
        detected_language = detection.language if language_choice == "Auto" else language_choice

        config = get_language_config(detected_language)

        st.subheader("Detected language")
        st.write(f"**{detected_language}**")
        if language_choice == "Auto" and detection.fallback:
            st.caption("No hint word matched - defaulted to English (documented fallback).")
        elif language_choice == "Auto" and detection.tied_with:
            st.caption(
                f"Tie with {', '.join(detection.tied_with)} - resolved by fixed language order."
            )

        sentences = split_sentences(text_content)
        raw_tokens = tokenize_text(text_content, lowercase=lowercase_tokens)
        tokens = filter_tokens(
            raw_tokens, config, remove_stopwords=remove_stopwords, min_length=min_token_length
        )

        tabs = st.tabs(
            [
                "Descriptive statistics",
                "Text structure",
                "Information extraction",
                "Sentiment analysis",
                "Language profile",
                "Method catalog",
            ]
        )

        with tabs[0]:
            if show_analysis:
                st.markdown("### Basic stats")
                stats = analyze_text(text_content, tokens, sentences)
                st.json(stats)
                render_tool_explanation("analyze_text")

            if show_readability:
                st.markdown("### Readability")
                score = readability_score(text_content, tokens, sentences, detected_language)
                formula = READABILITY_FORMULAS.get(
                    detected_language, READABILITY_FORMULAS["English"]
                )
                st.metric(formula.name, score)
                st.caption(f"Language-calibrated formula. Reference: {formula.reference}")
                render_tool_explanation("readability_score")

            if show_top_ngrams:
                st.markdown("### Top N-grams")
                top_n_value = st.slider("Top N-gram size", 2, 5, 2)
                top_ngram_count = st.slider("Top N-grams", 5, 30, 10)
                top_ngram_stats = top_ngrams(tokens, top_n_value, top_k=top_ngram_count)
                st.write(top_ngram_stats)
                render_tool_explanation("top_ngrams")

            if show_word_lengths:
                st.markdown("### Word length distribution")
                length_distribution = word_length_distribution(tokens)
                st.bar_chart(length_distribution)
                render_tool_explanation("word_length_distribution")

            if show_zipf:
                st.markdown("### Zipf rank-frequency")
                zipf_rows = zipf_table(tokens, top_k=100)
                log_points = {
                    "log10(count)": [math.log10(row["count"]) for row in zipf_rows],
                }
                st.line_chart(log_points)
                st.caption(
                    "x-axis: rank (log-spaced in nature; linear here). Straightish descent = Zipf."
                )
                st.dataframe(zipf_rows[:20])
                render_tool_explanation("zipf_table")

            if show_vocab_growth:
                st.markdown("### Vocabulary growth")
                growth = vocabulary_growth(tokens, step=max(50, len(tokens) // 50 or 1))
                st.line_chart({"vocabulary size": [point["vocabulary_size"] for point in growth]})
                render_tool_explanation("vocabulary_growth")

        with tabs[1]:
            if show_sentences:
                st.markdown("### Sentence splitting")
                st.write(sentences[:10])
                st.caption(f"Showing {min(10, len(sentences))} of {len(sentences)} sentences")
                render_tool_explanation("split_sentences")

            if show_tokens:
                st.markdown("### Tokens")
                st.write(tokens[:max_preview_tokens])
                st.caption(
                    f"Showing {min(max_preview_tokens, len(tokens))} of {len(tokens)} tokens"
                )
                render_tool_explanation("tokenize_text")
                render_tool_explanation("filter_tokens")

            if show_kwic:
                st.markdown("### KWIC concordance")
                kwic_keyword = st.text_input("Keyword", value="")
                if kwic_keyword.strip():
                    kwic_window = st.slider("Context window (tokens)", 2, 10, 5)
                    matches = kwic(
                        tokenize_text(text_content, lowercase=False),
                        kwic_keyword.strip(),
                        window=kwic_window,
                    )
                    st.caption(f"{len(matches)} match(es)")
                    st.dataframe(matches)
                render_tool_explanation("kwic")

            if show_ngrams:
                st.markdown("### N-grams")
                n_value = st.slider("N", 2, 5, 2)
                ngrams = generate_ngrams(tokens, n_value)
                st.write(ngrams[:30])
                st.caption(f"Showing {min(30, len(ngrams))} of {len(ngrams)} n-grams")
                render_tool_explanation("generate_ngrams")

        with tabs[2]:
            if show_keywords or show_tfidf:
                st.markdown("### Keywords")
                keyword_count = st.slider("Top keywords", 5, 30, 10)
                col_freq, col_tfidf = st.columns(2)
                if show_keywords:
                    with col_freq:
                        st.markdown("**Frequency** (stopwords removed)")
                        keywords = extract_keywords(tokens, config, top_k=keyword_count)
                        st.write(keywords)
                if show_tfidf:
                    with col_tfidf:
                        st.markdown("**TF-IDF** (sentences as documents)")
                        sentence_docs = [
                            filter_tokens(tokenize_text(sentence), config) for sentence in sentences
                        ]
                        st.write(tfidf_keywords(sentence_docs, top_k=keyword_count))
                if show_keywords:
                    render_tool_explanation("extract_keywords")
                if show_tfidf:
                    render_tool_explanation("tfidf_keywords")

        with tabs[3]:
            if show_sentiment:
                st.markdown("### Sentiment snapshot")
                sentiment = sentiment_analysis(tokens, detected_language)
                st.json(sentiment)
                render_tool_explanation("sentiment_analysis")

        with tabs[4]:
            st.markdown("### Detected language")
            st.write(f"**{detected_language}**")
            render_tool_explanation("detect_language")

            if show_language_hints:
                st.markdown("### Language hint matches")
                hint_scores = language_hint_hits(raw_tokens)
                st.bar_chart(hint_scores)
                render_tool_explanation("language_hint_hits")

        with tabs[5]:
            st.markdown("### NLP method catalog")
            st.write("Use this as a map of all tools available in this app, grouped by theme.")
            for theme in THEME_GROUPS:
                st.markdown(f"#### {theme}")
                themed_tools = [
                    name for name, details in TOOL_EXPLANATIONS.items() if details["theme"] == theme
                ]
                for tool_name in themed_tools:
                    render_tool_explanation(tool_name)
        st.divider()
        export_payload = {
            "language": detected_language,
            "stats": analyze_text(text_content, tokens, sentences),
            "readability": {
                "formula": READABILITY_FORMULAS.get(
                    detected_language, READABILITY_FORMULAS["English"]
                ).name,
                "score": readability_score(text_content, tokens, sentences, detected_language),
            },
            "sentiment": sentiment_analysis(tokens, detected_language),
            "keywords": extract_keywords(tokens, config, top_k=15),
        }
        st.download_button(
            "Export analysis (JSON)",
            json.dumps(export_payload, ensure_ascii=False, indent=2),
            file_name="codex_nlp_analysis.json",
            mime="application/json",
        )

    else:
        st.info("Upload a text file or paste text to get started.")
