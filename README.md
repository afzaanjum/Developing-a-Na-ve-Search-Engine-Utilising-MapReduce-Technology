# Developing-a-Na-ve-Search-Engine-Utilising-MapReduce-Technology
# Document Indexing and Relevance Analysis using MapReduce

## Introduction
This assignment explores distributed storage and processing using Apache Hadoop's MapReduce framework, focusing on implementing document indexing and relevance analysis. Document indexing involves creating an index of terms and their TF/IDF weights for a collection of documents, while relevance analysis evaluates document relevance to a given query based on TF/IDF representations.

## Approach
The approach utilizes Apache Hadoop's MapReduce paradigm to distribute document indexing and relevance analysis across multiple nodes. Three MapReduce jobs were designed:
1. **DocumentIndexing**: Computes TF/IDF weights for each term in the document collection.
2. **DocumentIndexingWithHashing**: Incorporates hashing to generate term IDs for improved computational efficiency.
3. **DocumentIndexingSparseVectors**: Optimizes document vector representation using sparse vectors to reduce storage and computational overhead.

## Implementation Details
### DocumentIndexing MapReduce Job
- **Mapper**: Tokenizes text, calculates word counts, and emits (word, (article_id, count)) pairs.
- **Reducer**: Aggregates TF/IDF weights for each word in the corpus.

### DocumentIndexingWithHashing MapReduce Job
- **Mapper**: Tokenizes text, calculates word counts, and emits (word_hash, (article_id, count)) pairs.
- **Reducer**: Aggregates TF/IDF weights using hash-based term IDs.

### DocumentIndexingSparseVectors MapReduce Job
- **Mapper**: Tokenizes text, calculates word counts, and emits (article_id, {term_id: tfidf}) pairs.
- **Reducer**: Aggregates TF/IDF weights and emits sparse vector representations of documents.

## Results
MapReduce jobs generated TF/IDF weights for terms and sparse vector representations of documents. Relevance analysis ranked documents based on their relevance to a given query, demonstrating the effectiveness of TF/IDF weighting. Despite its simplicity, the analysis accurately identified relevant documents.

## GitHub Repository Structure
- **document_indexing.py**: Main Python script implementing MapReduce jobs.
- **README.md**: Comprehensive report of the assignment.
- **output.txt**: Results of document indexing and relevance analysis.
- **output_sparse.txt**: Sparse vector representations of documents.

## Conclusion
This assignment provided insights into distributed storage and processing with Apache Hadoop's MapReduce framework. By implementing document indexing and relevance analysis, practical experience in handling big data efficiently was gained. Utilization of hash-based term IDs and sparse vector representations addressed challenges like high dimensionality and computational complexity. Through experimentation and optimization, understanding of TF/IDF weighting and its application in information retrieval systems was deepened.

