import json
import math
from pathlib import Path

import streamlit as st

import app_i18n
from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    READABILITY_FORMULAS,
    analyze_text,
    collocations,
    detect_language_details,
    detect_language_ngram_details,
    extract_keywords,
    filter_tokens,
    generate_ngrams,
    kwic,
    language_hint_evidence,
    language_hint_hits,
    porter_stem,
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


def render_tool_explanation(tool_name: str, lang: str) -> None:
    """Render a method card in the selected interface language.

    Card *content* is bilingual (``app_i18n.TOOL_CARDS``); the tool name and the
    grouping theme key stay English so code and API remain language-neutral.
    """
    card = app_i18n.TOOL_CARDS[tool_name]
    labels = app_i18n.CARD_LABELS[lang]
    text: dict[str, str] = card[lang]  # type: ignore[assignment]
    theme_label = app_i18n.THEME_LABELS[lang][card["theme"]]
    with st.expander(labels["expander"].format(tool=tool_name), expanded=False):
        st.markdown(f"- **{labels['theme']}:** {theme_label}")
        st.markdown(f"- **{labels['what']}:** {text['what']}")
        st.markdown(f"- **{labels['how']}:** {text['how']}")
        st.markdown(f"- **{labels['why']}:** {text['why']}")
        st.markdown(f"- **{labels['explore']}:** {text['explore']}")


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

ui_language = st.radio(
    "Interface language · Idioma da interface",
    list(app_i18n.LANGUAGES),
    horizontal=True,
)
LANG = app_i18n.LANGUAGES[ui_language]
T = app_i18n.UI[LANG]

st.write(T["intro"])
st.caption(T["intro_caption"])


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


def render_benchmarks(t: dict[str, str]) -> None:
    st.markdown(f"### {t['benchmarks_header']}")
    st.write(t["benchmarks_intro"])
    results_dir = Path(__file__).parent / "evals" / "results"
    result_files = sorted(results_dir.glob("*.json")) if results_dir.exists() else []
    if not result_files:
        st.info(t["benchmarks_none"])
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
    st.caption(t["benchmarks_provenance"])


def render_compare(t: dict[str, str]) -> None:
    st.markdown(f"### {t['compare_header']}")
    st.caption(t["compare_caption"])
    columns = st.columns(2)
    texts: dict[str, str] = {}
    for label, column in zip(("A", "B"), columns, strict=True):
        with column:
            choice = st.selectbox(
                t["compare_sample"].format(label=label),
                [t["compare_paste"], *SAMPLES],
                key=f"sample_{label}",
            )
            default = SAMPLES.get(choice, "")
            # key includes the choice so switching samples refreshes the widget
            texts[label] = st.text_area(
                t["compare_text"].format(label=label),
                value=default,
                height=150,
                key=f"text_{label}_{choice}",
            )
    if not (texts["A"].strip() and texts["B"].strip()):
        st.info(t["compare_need_both"])
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
    st.caption(t["compare_readability_note"])
    for label in ("A", "B"):
        st.markdown(t["compare_top_keywords"].format(label=label, keywords=keyword_summary[label]))


mode = st.radio(
    "Mode",
    ["analyze", "compare", "benchmarks"],
    format_func=lambda key: T[f"mode_{key}"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "benchmarks":
    render_benchmarks(T)
elif mode == "compare":
    render_compare(T)
else:
    with st.sidebar:
        st.header(T["sidebar_input"])
        uploaded_file = st.file_uploader(T["upload"], type=["txt"])
        text_input = st.text_area(T["paste"], height=200)
        sample_names = list(SAMPLES)
        sample_choice = st.selectbox(
            T["sample"],
            ["None", *sample_names],
            format_func=lambda key: T["sample_none"] if key == "None" else key,
        )
        language_choice = st.selectbox(
            T["analysis_language"], options=["Auto"] + LANGUAGE_OPTIONS, index=0
        )
        auto_detector = st.selectbox(
            T["auto_detector"],
            options=["ngram", "hints"],
            index=0,
            format_func=lambda key: T[f"auto_detector_{key}"],
            help=T["auto_detector_help"],
        )
        st.header(T["customizations"])
        lowercase_tokens = st.checkbox(T["lowercase"], value=True)
        remove_stopwords = st.checkbox(T["remove_stopwords"], value=True)
        min_token_length = st.slider(T["min_token_length"], 1, 8, 1)
        max_preview_tokens = st.slider(T["tokens_preview"], 10, 200, 50, step=10)
        st.header(T["tools"])
        show_analysis = st.checkbox(T["cb_basic_stats"], value=True)
        show_sentences = st.checkbox(T["cb_sentences"], value=True)
        show_tokens = st.checkbox(T["cb_tokens"], value=True)
        show_ngrams = st.checkbox(T["cb_ngrams"], value=False)
        show_keywords = st.checkbox(T["cb_keywords"], value=True)
        show_top_ngrams = st.checkbox(T["cb_top_ngrams"], value=True)
        show_readability = st.checkbox(T["cb_readability"], value=True)
        show_sentiment = st.checkbox(T["cb_sentiment"], value=True)
        show_word_lengths = st.checkbox(T["cb_word_lengths"], value=True)
        show_zipf = st.checkbox(T["cb_zipf"], value=False)
        show_vocab_growth = st.checkbox(T["cb_vocab_growth"], value=False)
        show_tfidf = st.checkbox(T["cb_tfidf"], value=True)
        show_kwic = st.checkbox(T["cb_kwic"], value=False)
        show_collocations = st.checkbox(T["cb_collocations"], value=False)
        show_stems = st.checkbox(T["cb_stems"], value=False)
        show_language_hints = st.checkbox(T["cb_language_hints"], value=False)

    text_content = ""
    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8", errors="ignore")
    elif text_input.strip():
        text_content = text_input
    elif sample_choice != "None":
        text_content = SAMPLES[sample_choice]

    if text_content.strip():
        detection = detect_language_details(text_content)
        ngram_detection = detect_language_ngram_details(text_content)
        use_ngram = auto_detector == "ngram"

        if language_choice != "Auto":
            detected_language = language_choice
            detector_used = "manual"
        elif use_ngram:
            detected_language = ngram_detection.language
            detector_used = "char_ngrams"
        else:
            detected_language = detection.language
            detector_used = "hint_words"

        config = get_language_config(detected_language)

        st.subheader(T["detected_language"])
        st.write(f"**{detected_language}**")
        if language_choice == "Auto":
            active = T["detector_ngram_name"] if use_ngram else T["detector_hints_name"]
            st.caption(T["active_detector"].format(detector=active))
            if use_ngram:
                st.caption(T["compare_hints"].format(language=detection.language))
                if ngram_detection.fallback:
                    st.caption(T["fallback_ngram"])
            else:
                st.caption(T["compare_ngram"].format(language=ngram_detection.language))
                if detection.fallback:
                    st.caption(T["fallback_hints"])
                elif detection.tied_with:
                    st.caption(T["tie_note"].format(langs=", ".join(detection.tied_with)))

        sentences = split_sentences(text_content)
        raw_tokens = tokenize_text(text_content, lowercase=lowercase_tokens)
        tokens = filter_tokens(
            raw_tokens, config, remove_stopwords=remove_stopwords, min_length=min_token_length
        )

        tabs = st.tabs(
            [
                T["tab_descriptive"],
                T["tab_structure"],
                T["tab_extraction"],
                T["tab_sentiment"],
                T["tab_language"],
                T["tab_catalog"],
            ]
        )

        with tabs[0]:
            if show_analysis:
                st.markdown(f"### {T['h_basic_stats']}")
                stats = analyze_text(text_content, tokens, sentences)
                st.json(stats)
                render_tool_explanation("analyze_text", LANG)

            if show_readability:
                st.markdown(f"### {T['h_readability']}")
                score = readability_score(text_content, tokens, sentences, detected_language)
                formula = READABILITY_FORMULAS.get(
                    detected_language, READABILITY_FORMULAS["English"]
                )
                st.metric(formula.name, score)
                st.caption(T["readability_caption"].format(reference=formula.reference))
                render_tool_explanation("readability_score", LANG)

            if show_top_ngrams:
                st.markdown(f"### {T['h_top_ngrams']}")
                top_n_value = st.slider(T["top_ngram_size"], 2, 5, 2)
                top_ngram_count = st.slider(T["top_ngram_count"], 5, 30, 10)
                top_ngram_stats = top_ngrams(tokens, top_n_value, top_k=top_ngram_count)
                st.write(top_ngram_stats)
                render_tool_explanation("top_ngrams", LANG)

            if show_word_lengths:
                st.markdown(f"### {T['h_word_lengths']}")
                length_distribution = word_length_distribution(tokens)
                st.bar_chart(length_distribution)
                render_tool_explanation("word_length_distribution", LANG)

            if show_zipf:
                st.markdown(f"### {T['h_zipf']}")
                zipf_rows = zipf_table(tokens, top_k=100)
                log_points = {
                    "log10(count)": [math.log10(row["count"]) for row in zipf_rows],
                }
                st.line_chart(log_points)
                st.caption(T["zipf_caption"])
                st.dataframe(zipf_rows[:20])
                render_tool_explanation("zipf_table", LANG)

            if show_vocab_growth:
                st.markdown(f"### {T['h_vocab_growth']}")
                growth = vocabulary_growth(tokens, step=max(50, len(tokens) // 50 or 1))
                st.line_chart(
                    {T["vocab_growth_label"]: [point["vocabulary_size"] for point in growth]}
                )
                render_tool_explanation("vocabulary_growth", LANG)

        with tabs[1]:
            if show_sentences:
                st.markdown(f"### {T['h_sentences']}")
                st.write(sentences[:10])
                st.caption(
                    T["sentences_caption"].format(
                        shown=min(10, len(sentences)), total=len(sentences)
                    )
                )
                render_tool_explanation("split_sentences", LANG)

            if show_tokens:
                st.markdown(f"### {T['h_tokens']}")
                st.write(tokens[:max_preview_tokens])
                st.caption(
                    T["tokens_caption"].format(
                        shown=min(max_preview_tokens, len(tokens)), total=len(tokens)
                    )
                )
                render_tool_explanation("tokenize_text", LANG)
                render_tool_explanation("filter_tokens", LANG)

            if show_stems:
                st.markdown(f"### {T['h_stems']}")
                stem_rows = [
                    {"token": token, "stem": porter_stem(token)}
                    for token in tokens[:30]
                    if porter_stem(token) != token
                ]
                st.dataframe(stem_rows)
                render_tool_explanation("porter_stem", LANG)

            if show_kwic:
                st.markdown(f"### {T['h_kwic']}")
                kwic_keyword = st.text_input(T["kwic_keyword"], value="")
                if kwic_keyword.strip():
                    kwic_window = st.slider(T["kwic_window"], 2, 10, 5)
                    matches = kwic(
                        tokenize_text(text_content, lowercase=False),
                        kwic_keyword.strip(),
                        window=kwic_window,
                    )
                    st.caption(T["kwic_matches"].format(count=len(matches)))
                    st.dataframe(matches)
                render_tool_explanation("kwic", LANG)

            if show_ngrams:
                st.markdown(f"### {T['h_ngrams']}")
                n_value = st.slider(T["ngrams_n"], 2, 5, 2)
                ngrams = generate_ngrams(tokens, n_value)
                st.write(ngrams[:30])
                st.caption(
                    T["ngrams_caption"].format(shown=min(30, len(ngrams)), total=len(ngrams))
                )
                render_tool_explanation("generate_ngrams", LANG)

        with tabs[2]:
            if show_keywords or show_tfidf:
                st.markdown(f"### {T['h_keywords']}")
                keyword_count = st.slider(T["keyword_count"], 5, 30, 10)
                col_freq, col_tfidf = st.columns(2)
                if show_keywords:
                    with col_freq:
                        st.markdown(T["keywords_freq"])
                        keywords = extract_keywords(tokens, config, top_k=keyword_count)
                        st.write(keywords)
                if show_tfidf:
                    with col_tfidf:
                        st.markdown(T["keywords_tfidf"])
                        sentence_docs = [
                            filter_tokens(tokenize_text(sentence), config) for sentence in sentences
                        ]
                        st.write(tfidf_keywords(sentence_docs, top_k=keyword_count))
                if show_keywords:
                    render_tool_explanation("extract_keywords", LANG)
                if show_tfidf:
                    render_tool_explanation("tfidf_keywords", LANG)

            if show_collocations:
                st.markdown(f"### {T['h_collocations']}")
                min_count = st.slider(T["colloc_min_count"], 2, 10, 2)
                over_filtered = st.checkbox(T["colloc_over_filtered"], value=False)
                if over_filtered:
                    collocation_tokens = tokens
                    st.caption(T["colloc_filtered_caption"])
                else:
                    collocation_tokens = tokenize_text(text_content, lowercase=lowercase_tokens)
                    st.caption(T["colloc_original_caption"])
                st.write(collocations(collocation_tokens, min_count=min_count, top_k=15))
                render_tool_explanation("collocations", LANG)

        with tabs[3]:
            if show_sentiment:
                st.markdown(f"### {T['h_sentiment']}")
                sentiment = sentiment_analysis(tokens, detected_language)
                st.json(sentiment)
                render_tool_explanation("sentiment_analysis", LANG)

        with tabs[4]:
            st.markdown(f"### {T['detected_language']}")
            st.write(f"**{detected_language}**")
            render_tool_explanation("detect_language", LANG)
            ngram_details = detect_language_ngram_details(text_content)
            st.markdown(f"### {T['h_ngram_detection']}")
            st.write(T["ngram_closest"].format(language=ngram_details.language))
            if ngram_details.distances:
                ranked = sorted(ngram_details.distances.items(), key=lambda item: item[1])
                distance_rows = [
                    {
                        T["col_rank"]: rank,
                        T["col_language"]: language,
                        T["col_distance"]: distance,
                        T["col_closest"]: T["closest_marker"] if rank == 1 else "",
                    }
                    for rank, (language, distance) in enumerate(ranked, start=1)
                ]
                st.dataframe(distance_rows, use_container_width=True, hide_index=True)
                st.caption(T["distance_caption"])
            else:
                st.caption(T["distance_fallback"])
            render_tool_explanation("detect_language_ngram", LANG)

            if show_language_hints:
                st.markdown(f"### {T['h_language_hints']}")
                hint_scores = language_hint_hits(raw_tokens)
                hint_evidence = language_hint_evidence(raw_tokens)
                evidence_rows = [
                    {
                        T["col_language"]: language,
                        T["col_hits"]: hint_scores[language],
                        T["col_matched"]: ", ".join(
                            f"{token} ×{count}" if count > 1 else token
                            for token, count in hint_evidence[language].items()
                        ),
                    }
                    for language in sorted(hint_scores, key=lambda lang: -hint_scores[lang])
                ]
                st.dataframe(evidence_rows, use_container_width=True, hide_index=True)
                st.caption(T["hint_evidence_caption"])
                render_tool_explanation("language_hint_hits", LANG)

        with tabs[5]:
            st.markdown(f"### {T['h_catalog']}")
            st.write(T["catalog_intro"])
            for theme in app_i18n.THEME_ORDER:
                st.markdown(f"#### {app_i18n.THEME_LABELS[LANG][theme]}")
                themed_tools = [
                    name for name, card in app_i18n.TOOL_CARDS.items() if card["theme"] == theme
                ]
                for tool_name in themed_tools:
                    render_tool_explanation(tool_name, LANG)
        st.divider()
        export_payload = {
            "language": detected_language,
            "detector": detector_used,
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
            T["export_button"],
            json.dumps(export_payload, ensure_ascii=False, indent=2),
            file_name="codex_nlp_analysis.json",
            mime="application/json",
        )

    else:
        st.info(T["get_started"])
