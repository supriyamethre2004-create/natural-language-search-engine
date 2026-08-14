# Natural Language Search Engine

An NLP-based search engine that retrieves relevant information from a collection of documents using keyword-based and semantic search techniques.

## Project Overview

Traditional search engines primarily rely on exact keyword matching, which can fail when the user's query and the relevant document use different words to express the same concept.

This project aims to build a natural language search engine that combines:

- Keyword-based retrieval using BM25
- Semantic search using text embeddings
- Hybrid ranking
- Retrieval-Augmented Generation (RAG)
- Source-aware question answering

## Planned Architecture

Documents → Text Extraction → Chunking →  
BM25 Search + Semantic Search → Hybrid Retrieval →  
RAG → Answer with Sources

## Planned Features

- PDF document processing
- Text extraction and preprocessing
- Intelligent document chunking
- BM25 keyword retrieval
- Semantic search using embeddings
- Hybrid search and ranking
- RAG-based question answering
- Source/page references
- Search evaluation
- Streamlit web interface

## Technologies

- Python
- Natural Language Processing
- BM25
- Sentence Transformers
- FAISS
- RAG
- Large Language Models
- Streamlit

## Project Status

🚧 **Currently under development**

The project is being developed incrementally, starting with document processing and retrieval before implementing the RAG pipeline and user interface.