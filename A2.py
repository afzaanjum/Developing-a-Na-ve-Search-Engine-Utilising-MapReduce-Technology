# Assignment 02
# Group Members
# Ali Tanveer (21I-1692) 
# Afza Anjum (21I-1724) 
# Ruwaid Imran (21I-1728)


# Importing necessary libraries
from mrjob.job import MRJob
import re
from collections import defaultdict
import math
import sys
import hashlib

# Define the documents
documents = {
    1: "I wonder how many miles I’ve fallen by this time?",
    2: "According to the latest census, the population of Moscow is more than two million.",
    3: "It was a warm, bright day at the end of August.",
    4: "To be, or not to be?",
    5: "The population, the population, the population"
}

class DocumentIndexing(MRJob):
    
    def mapper(self, _, line):
        """
        Mapper function: Tokenizes the section text, calculates word counts, 
        and emits (word, (article_id, count)) pairs.
        """
        article_id, section_text = line.split(',', 1)
        words = re.findall(r'\w+', section_text.lower())
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        for word, count in word_count.items():
            yield word, (article_id, count)
    
    def reducer(self, word, article_counts):
        """
        Reducer function: Calculates TF/IDF weights for each word in the corpus.
        """
        total_docs_with_word = 0
        doc_word_count = defaultdict(int)
        for article_id, count in article_counts:
            total_docs_with_word += 1
            doc_word_count[article_id] = count
        idf = math.log(1 + (1 / total_docs_with_word))
        for article_id, count in doc_word_count.items():
            tfidf = count * idf
            yield word, (article_id, tfidf)

def calculate_tf(document):
    """
    Calculate Term Frequency (TF) for a given document.
    """
    # Tokenize the document
    tokens = document.split()
    # Count the frequency of each term
    term_frequency = {}
    for term in tokens:
        term_frequency[term] = term_frequency.get(term, 0) + 1
    # Normalize the frequencies
    max_frequency = max(term_frequency.values())
    tf = {term: frequency / max_frequency for term, frequency in term_frequency.items()}
    return tf

def calculate_idf(documents):
    """
    Calculate Inverse Document Frequency (IDF) for the given documents.
    """
    # Count the number of documents containing each term
    doc_frequency = {}
    for tf in documents.values():
        for term in tf.keys():
            doc_frequency[term] = doc_frequency.get(term, 0) + 1
    # Calculate IDF for each term
    total_documents = len(documents)
    idf = {term: math.log(total_documents / frequency) for term, frequency in doc_frequency.items()}
    return idf

def convert_to_sparse_vector(tfidf_weights):
    """
    Convert TF/IDF weights to sparse vector representation.
    """
    sparse_vector = {}
    for term_id, weight in tfidf_weights.items():
        if weight != 0:
            sparse_vector[term_id] = weight
    return sparse_vector

def generate_hash(word, hash_range):
    """
    Generate a hash ID for a word within the specified range.
    """
    hash_id = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16) % hash_range
    return hash_id

class DocumentIndexingWithHashing(MRJob):
    
    def mapper(self, _, line):
        """
        Mapper function: Tokenizes the section text, calculates word counts, 
        and emits (word_hash, (article_id, count)) pairs.
        """
        article_id, section_text = line.split(',', 1)
        words = re.findall(r'\w+', section_text.lower())
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        for word, count in word_count.items():
            word_hash = generate_hash(word, 1000)  # Adjust hash range as needed
            yield word_hash, (article_id, count)
    
    def reducer(self, word_hash, article_counts):
        """
        Reducer function: Calculates TF/IDF weights for each word in the corpus.
        """
        word = str(word_hash)  # Convert hash back to string
        total_docs_with_word = 0
        doc_word_count = defaultdict(int)
        for article_id, count in article_counts:
            total_docs_with_word += 1
            doc_word_count[article_id] = count
        idf = math.log(1 + (1 / total_docs_with_word))
        for article_id, count in doc_word_count.items():
            tfidf = count * idf
            yield word, (article_id, tfidf)

class DocumentIndexingSparseVectors(MRJob):
    
    def mapper(self, _, line):
        """
        Mapper function: Tokenizes the section text, calculates word counts, 
        and emits (article_id, {term_id: tfidf}) pairs.
        """
        article_id, section_text = line.split(',', 1)
        words = re.findall(r'\w+', section_text.lower())
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        for word, count in word_count.items():
            yield int(generate_hash(word, 1000)), (int(article_id), count)
    
    def reducer(self, term_id, article_counts):
        """
        Reducer function: Calculates TF/IDF weights for each term in the corpus.
        """
        idf = math.log(1 + (1 / total_docs_with_word))
        for article_id, count in article_counts:
            tfidf = count * idf
            yield article_id, {term_id: tfidf}

# Calculate TF for each document
tf_documents = {doc_id: calculate_tf(doc) for doc_id, doc in documents.items()}

# Calculate IDF for the given documents
idf_values = calculate_idf(tf_documents)

# Output TF and IDF values
with open("output.txt", "w") as f:
    f.write("Term Frequency (TF):\n")
    for doc_id, tf in tf_documents.items():
        f.write(f"Document {doc_id}: {tf}\n")

    f.write("\nInverse Document Frequency (IDF):\n")
    for term, idf in idf_values.items():
        f.write(f"{term}: {idf}\n")

    # Convert TF/IDF weights to sparse vectors
    sparse_vectors = {doc_id: convert_to_sparse_vector(tfidf_weights) for doc_id, tfidf_weights in tf_documents.items()}

    f.write("\nSparse Vectors:\n")
    for doc_id, vector in sparse_vectors.items():
        f.write(f"Document {doc_id}: {vector}\n")

