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

    tabs = st.tabs(["Overview", "Tokens", "N-grams", "Keywords", "Analytics"])

    with tabs[0]:
        col_left, col_right = st.columns(2)

        if show_analysis:
            with col_left:
                st.markdown("### Basic stats")
                stats = analyze_text(text_content, tokens, sentences)
                st.json(stats)

        if show_sentences:
            with col_right:
                st.markdown("### Sentence splitting")
                st.write(sentences[:10])
                st.caption(
                    f"Showing {min(10, len(sentences))} of {len(sentences)} sentences"
                )

        if show_readability:
            st.markdown("### Readability")
            score = readability_score(text_content, tokens, sentences)
            st.metric("Flesch Reading Ease", score)

        if show_sentiment:
            st.markdown("### Sentiment snapshot")
            sentiment = sentiment_analysis(tokens)
            st.json(sentiment)

    with tabs[1]:
        if show_tokens:
            st.markdown("### Tokens")
            st.write(tokens[:max_preview_tokens])
            st.caption(
                f"Showing {min(max_preview_tokens, len(tokens))} of {len(tokens)} tokens"
            )

    with tabs[2]:
        if show_ngrams:
            st.markdown("### N-grams")
            n_value = st.slider("N", 2, 5, 2)
            ngrams = generate_ngrams(tokens, n_value)
            st.write(ngrams[:30])
            st.caption(
                f"Showing {min(30, len(ngrams))} of {len(ngrams)} n-grams"
            )

        if show_top_ngrams:
            st.markdown("### Top N-grams")
            top_n_value = st.slider("Top N-gram size", 2, 5, 2)
            top_ngram_count = st.slider("Top N-grams", 5, 30, 10)
            top_ngram_stats = top_ngrams(tokens, top_n_value, top_k=top_ngram_count)
            st.write(top_ngram_stats)

    with tabs[3]:
        if show_keywords:
            st.markdown("### Keywords")
            keyword_count = st.slider("Top keywords", 5, 30, 10)
            keywords = extract_keywords(tokens, config, top_k=keyword_count)
            st.write(keywords)

    with tabs[4]:
        if show_word_lengths:
            st.markdown("### Word length distribution")
            length_distribution = word_length_distribution(tokens)
            st.bar_chart(length_distribution)

        if show_language_hints:
            st.markdown("### Language hint matches")
            hint_scores = language_hint_hits(raw_tokens)
            st.bar_chart(hint_scores)
else:
    st.info("Upload a text file or paste text to get started.")
