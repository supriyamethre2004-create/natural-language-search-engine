import streamlit as st
import sys
from pathlib import Path

# Add src folder to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from search import search


# Page configuration
st.set_page_config(
    page_title="Natural Language Search Engine",
    page_icon="🔎",
    layout="wide"
)


# Title
st.title("🔎 Natural Language Search Engine")

st.write(
    "Search across your PDF documents using semantic and keyword-based retrieval."
)


# Search box
query = st.text_input(
    "Enter your search query",
    placeholder="Example: What is self-attention?"
)


# Number of results
top_k = st.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=5
)


# Search button
if st.button("Search", type="primary"):

    if not query.strip():

        st.warning("Please enter a search query.")

    else:

        with st.spinner("Searching documents..."):

            results = search(
                query,
                top_k=top_k
            )

        st.subheader("Search Results")

        for rank, result in enumerate(results, start=1):

            st.markdown(
                f"### {rank}. {result['source']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"📄 **Page:** {result['page']}")

            with col2:
                st.write(
                    f"🧠 **Semantic Score:** "
                    f"{result['semantic_score']:.4f}"
                )

            with col3:
                st.write(
                    f"🔑 **BM25 Score:** "
                    f"{result['bm25_score']:.4f}"
                )

            st.write(
                f"⭐ **Combined Score:** "
                f"{result['combined_score']:.4f}"
            )

            with st.expander("View relevant text"):

                st.write(result["text"])

            st.divider()