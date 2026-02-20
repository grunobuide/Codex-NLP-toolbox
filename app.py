import streamlit as st

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    analyze_text,
    detect_language,
    extract_keywords,
    generate_ngrams,
    language_hint_hits,
    readability_score,
    sentiment_analysis,
    split_sentences,
    tokenize_text,
    top_ngrams,
    word_length_distribution,
    filter_tokens,
)

st.set_page_config(page_title="Codex NLP Toolbox", layout="wide")

TOOL_EXPLANATIONS = {
    "analyze_text": {
        "theme": "Descriptive statistics",
        "what": "Counts and ratio-based summary metrics for the current text.",
        "how": "Uses token and sentence counts to compute averages, lexical diversity, and reading-time estimate.",
        "why": "Gives a fast baseline profile before deeper NLP modeling.",
        "explore": "Compare lexical diversity and sentence length between authors, genres, or translations.",
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
        "what": "Flesch Reading Ease estimate.",
        "how": "Uses words per sentence and estimated syllables per word in the Flesch formula.",
        "why": "Provides a rough complexity signal for educational and editorial use.",
        "explore": "Compare Flesch with SMOG and Dale-Chall on the same corpus.",
    },
    "sentiment_analysis": {
        "theme": "Sentiment analysis",
        "what": "Lexicon-based sentiment snapshot.",
        "how": "Counts positive and negative seed words and normalizes by token count.",
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
    "Upload a text file or paste raw text, then explore NLP techniques "
    "across multiple languages."
)
st.caption(
    "This interface is organized by NLP themes and includes method cards "
    "to explain what each tool does, how it works, and where to explore next."
)

with st.sidebar:
    st.header("Input")
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    text_input = st.text_area("Or paste raw text", height=200)
    language_choice = st.selectbox(
        "Language", options=["Auto"] + LANGUAGE_OPTIONS, index=0
    )
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
    show_language_hints = st.checkbox("Language hint matches", value=False)

text_content = ""
if uploaded_file is not None:
    text_content = uploaded_file.read().decode("utf-8", errors="ignore")
else:
    text_content = text_input

if text_content.strip():
    if language_choice == "Auto":
        detected_language = detect_language(text_content)
    else:
        detected_language = language_choice

    config = get_language_config(detected_language)

    st.subheader("Detected language")
    st.write(f"**{detected_language}**")

    sentences = split_sentences(text_content)
    raw_tokens = tokenize_text(text_content, config, lowercase=lowercase_tokens)
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
            score = readability_score(text_content, tokens, sentences)
            st.metric("Flesch Reading Ease", score)
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

    with tabs[1]:
        if show_sentences:
            st.markdown("### Sentence splitting")
            st.write(sentences[:10])
            st.caption(
                f"Showing {min(10, len(sentences))} of {len(sentences)} sentences"
            )
            render_tool_explanation("split_sentences")

        if show_tokens:
            st.markdown("### Tokens")
            st.write(tokens[:max_preview_tokens])
            st.caption(
                f"Showing {min(max_preview_tokens, len(tokens))} of {len(tokens)} tokens"
            )
            render_tool_explanation("tokenize_text")
            render_tool_explanation("filter_tokens")

        if show_ngrams:
            st.markdown("### N-grams")
            n_value = st.slider("N", 2, 5, 2)
            ngrams = generate_ngrams(tokens, n_value)
            st.write(ngrams[:30])
            st.caption(
                f"Showing {min(30, len(ngrams))} of {len(ngrams)} n-grams"
            )
            render_tool_explanation("generate_ngrams")

    with tabs[2]:
        if show_keywords:
            st.markdown("### Keywords")
            keyword_count = st.slider("Top keywords", 5, 30, 10)
            keywords = extract_keywords(tokens, config, top_k=keyword_count)
            st.write(keywords)
            render_tool_explanation("extract_keywords")

    with tabs[3]:
        if show_sentiment:
            st.markdown("### Sentiment snapshot")
            sentiment = sentiment_analysis(tokens)
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
        st.write(
            "Use this as a map of all tools available in this app, grouped by theme."
        )
        for theme in THEME_GROUPS:
            st.markdown(f"#### {theme}")
            themed_tools = [
                name
                for name, details in TOOL_EXPLANATIONS.items()
                if details["theme"] == theme
            ]
            for tool_name in themed_tools:
                render_tool_explanation(tool_name)
else:
    st.info("Upload a text file or paste text to get started.")
