# import requests
# import json
# import re
# import string
# import time
# import psutil  
# from concurrent.futures import ThreadPoolExecutor
# from pymongo import MongoClient
# from collections import Counter

# # Custom function to clean and tokenize text
# def clean_and_tokenize(text):
#     # Remove punctuation and tokenize
#     text = text.lower().translate(str.maketrans("", "", string.punctuation))
#     return text.split()

# # Custom keyword extraction without external libraries (simple frequency-based)
# def extract_keywords(text, domain_specific_terms=None, top_n=5):
#     words = clean_and_tokenize(text)
#     # Count the frequency of each word
#     word_freq = Counter(words)
    
#     # If domain-specific terms are provided, prioritize them
#     if domain_specific_terms:
#         domain_keywords = [word for word in words if word in domain_specific_terms]
#         # If we found any domain-specific keywords, return them
#         if domain_keywords:
#             return domain_keywords[:top_n]
    
#     # Otherwise, return the most frequent words
#     return [keyword for keyword, _ in word_freq.most_common(top_n)]

# # Custom summarization based on document length
# def summarize_text(text, doc_length):
#     sentences = text.split('.')
#     if doc_length == 'short':
#         return '. '.join(sentences[:1])  # Short docs get a 1-sentence summary
#     elif doc_length == 'medium':
#         return '. '.join(sentences[:3])  # Medium docs get 3 sentences
#     else:
#         return '. '.join(sentences[:5])  # Long docs get 5 sentences

# # Function to classify document as short, medium, or long
# def classify_document_length(text):
#     word_count = len(clean_and_tokenize(text))
#     if word_count < 100:
#         return 'short'
#     elif word_count < 500:
#         return 'medium'
#     else:
#         return 'long'

# # MongoDB setup 
# def setup_mongodb():
#     try:
#         client = MongoClient('mongodb://localhost:27017/')
#         db = client['pdf_database']
#         return db['pdfs']
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {str(e)}")
#         return None

# # Fetch PDF
# def fetch_pdf(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.content
#         else:
#             print(f"Failed to download {url}: {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"Error fetching {url}: {str(e)}")
#         return None

# # Basic text extraction from PDF 
# def extract_text_from_pdf(pdf_content):
#     try:
#         # Simulated PDF content for testing.
#         return "Simulated PDF content for testing."
#     except Exception as e:
#         print(f"Error processing PDF: {str(e)}")
#         return ""

# # Process each PDF
# def process_pdf(pdf_key, url, pdf_collection, domain_specific_terms):
#     pdf_content = fetch_pdf(url)
#     if pdf_content:
#         text = extract_text_from_pdf(pdf_content)
#         if text:
#             # Classify document length
#             doc_length = classify_document_length(text)
#             # Summarize the text based on length
#             summary = summarize_text(text, doc_length)
#             # Extract domain-specific keywords
#             keywords = extract_keywords(text, domain_specific_terms)
#             document = {
#                 "pdf_key": pdf_key,
#                 "url": url,
#                 "summary": summary,
#                 "keywords": keywords,
#                 "text": text[:500]  # Storing only first 500 characters of text
#             }
#             # Insert into MongoDB
#             pdf_collection.insert_one(document)
#             print(f"Processed and stored {pdf_key}")

# # Load dataset from JSON
# def load_dataset(file_path):
#     try:
#         with open(file_path) as f:
#             return json.load(f)
#     except Exception as e:
#         print(f"Error loading dataset: {str(e)}")
#         return {}

# # Log performance metrics
# def log_performance_metrics(start_time, end_time, pdf_count):
#     elapsed_time = end_time - start_time
#     cpu_usage = psutil.cpu_percent()
#     memory_info = psutil.virtual_memory()

#     print("\nPerformance Report:")
#     print(f"Total PDFs processed: {pdf_count}")
#     print(f"Total processing time: {elapsed_time:.2f} seconds")
#     print(f"CPU usage: {cpu_usage}%")
#     print(f"Memory usage: {memory_info.percent}%")
#     print(f"Memory available: {memory_info.available / (1024 * 1024):.2f} MB")
#     print(f"Memory used: {memory_info.used / (1024 * 1024):.2f} MB")
#     print(f"Memory total: {memory_info.total / (1024 * 1024):.2f} MB")

# # Main function to run the pipeline
# def main():
#     start_time = time.time()  # Start timer
#     dataset = load_dataset('dataset.json')
#     pdf_collection = setup_mongodb()
#     if pdf_collection is None:
#         return  # Exit if MongoDB setup failed

#     domain_specific_terms = ['technology', 'innovation', 'ai', 'development', 'research']

#     # Using concurrency to process multiple PDFs at once
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         futures = [executor.submit(process_pdf, pdf_key, url, pdf_collection, domain_specific_terms) for pdf_key, url in dataset.items()]

#     # Wait for all futures to complete
#     for future in futures:
#         future.result()  # This will block until the future is done

#     end_time = time.time()  # End timer

#     # Log performance metrics
#     log_performance_metrics(start_time, end_time, len(dataset))

#     # Fetch and display results from MongoDB
#     for pdf in pdf_collection.find():
#         print(f"PDF Key: {pdf['pdf_key']}, Summary: {pdf['summary']}, Keywords: {pdf['keywords']}")

# if __name__ == "__main__":
#     main()

import requests
import json
import re
import string
import time
import psutil
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from collections import Counter

# Custom function to clean and tokenize text
def clean_and_tokenize(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return text.split()

# Custom keyword extraction
def extract_keywords(text, domain_specific_terms=None, top_n=5):
    words = clean_and_tokenize(text)
    word_freq = Counter(words)
    
    if domain_specific_terms:
        domain_keywords = [word for word in words if word in domain_specific_terms]
        if domain_keywords:
            return domain_keywords[:top_n]
    
    return [keyword for keyword, _ in word_freq.most_common(top_n)]

# Summarization based on document length
def summarize_text(text, doc_length):
    sentences = text.split('. ')
    if doc_length == 'short':
        return sentences[0].strip()  # Short docs get a 1-sentence summary
    elif doc_length == 'medium':
        return '. '.join([s.strip() for s in sentences[:3]]).strip()  # Medium docs get 3 sentences
    else:
        return '. '.join([s.strip() for s in sentences[:5]]).strip()  # Long docs get 5 sentences

# Classify document length
def classify_document_length(text):
    word_count = len(clean_and_tokenize(text))
    if word_count < 100:
        return 'short'
    elif word_count < 500:
        return 'medium'
    else:
        return 'long'

# MongoDB setup
def setup_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['pdf_database']
        return db['pdfs']
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None

# Fetch PDF
def fetch_pdf(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

# Basic text extraction from PDF 
def extract_text_from_pdf(pdf_content):
    return "Simulated PDF content for testing. This is the second sentence. This is the third sentence. This is the fourth sentence."

# Process each PDF
def process_pdf(pdf_key, url, pdf_collection, domain_specific_terms):
    pdf_content = fetch_pdf(url)
    if pdf_content:
        text = extract_text_from_pdf(pdf_content)
        if text:
            doc_length = classify_document_length(text)
            summary = summarize_text(text, doc_length)
            keywords = extract_keywords(text, domain_specific_terms)
            document = {
                "pdf_key": pdf_key,
                "url": url,
                "summary": summary,
                "keywords": keywords,
                "text": text[:500]
            }
            pdf_collection.insert_one(document)
            print(f"Processed and stored {pdf_key}")

# Load dataset from JSON
def load_dataset(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return {}

# Log performance metrics
def log_performance_metrics(start_time, end_time, pdf_count):
    elapsed_time = end_time - start_time
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()

    print("\nPerformance Report:")
    print(f"Total PDFs processed: {pdf_count}")
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory usage: {memory_info.percent}%")
    print(f"Memory available: {memory_info.available / (1024 * 1024):.2f} MB")
    print(f"Memory used: {memory_info.used / (1024 * 1024):.2f} MB")
    print(f"Memory total: {memory_info.total / (1024 * 1024):.2f} MB")

# Main function to run the pipeline
def main():
    start_time = time.time()
    dataset = load_dataset('dataset.json')
    pdf_collection = setup_mongodb()
    if pdf_collection is None:
        return

    domain_specific_terms = ['technology', 'innovation', 'ai', 'development', 'research']

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_pdf, pdf_key, url, pdf_collection, domain_specific_terms) for pdf_key, url in dataset.items()]

    for future in futures:
        future.result()

    end_time = time.time()
    log_performance_metrics(start_time, end_time, len(dataset))

    for pdf in pdf_collection.find():
        print(f"PDF Key: {pdf['pdf_key']}, Summary: {pdf['summary']}, Keywords: {pdf['keywords']}")

if __name__ == "__main__":
    main()
