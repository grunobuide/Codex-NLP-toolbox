import streamlit as st

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    analyze_text,
    detect_language,
    extract_keywords,
    generate_ngrams,
    split_sentences,
    tokenize_text,
)

st.set_page_config(page_title="Codex NLP Toolbox", layout="wide")

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
    st.header("Tools")
    show_analysis = st.checkbox("Basic stats", value=True)
    show_sentences = st.checkbox("Sentence splitting", value=True)
    show_tokens = st.checkbox("Tokenization", value=True)
    show_ngrams = st.checkbox("N-grams", value=False)
    show_keywords = st.checkbox("Keyword extraction", value=True)

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

    col_left, col_right = st.columns(2)

    if show_analysis:
        with col_left:
            st.markdown("### Basic stats")
            stats = analyze_text(text_content)
            st.json(stats)

    if show_sentences:
        with col_right:
            st.markdown("### Sentence splitting")
            sentences = split_sentences(text_content)
            st.write(sentences[:10])
            st.caption(f"Showing {min(10, len(sentences))} of {len(sentences)} sentences")

    if show_tokens:
        st.markdown("### Tokens")
        tokens = tokenize_text(text_content, config)
        st.write(tokens[:50])
        st.caption(f"Showing {min(50, len(tokens))} of {len(tokens)} tokens")

    if show_ngrams:
        st.markdown("### N-grams")
        n_value = st.slider("N", 2, 5, 2)
        ngrams = generate_ngrams(tokens, n_value)
        st.write(ngrams[:30])
        st.caption(f"Showing {min(30, len(ngrams))} of {len(ngrams)} n-grams")

    if show_keywords:
        st.markdown("### Keywords")
        keyword_count = st.slider("Top keywords", 5, 30, 10)
        keywords = extract_keywords(tokens, config, top_k=keyword_count)
        st.write(keywords)
else:
    st.info("Upload a text file or paste text to get started.")
