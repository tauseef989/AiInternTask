import unittest
from pdf_processor import classify_document_length, summarize_text

class TestPDFProcessor(unittest.TestCase):

    def test_classify_document_length_short(self):
        self.assertEqual(classify_document_length("Short text."), 'short')

    def test_classify_document_length_medium(self):
        # Create a text that is definitely medium length (100-499 words)
        text = ("This is a medium length text. " * 10)  # 10 sentences, approx. 50 words
        text += ("It contains multiple sentences to ensure it is classified correctly. " * 5)  # Approx. 40 more words
        text += ("Adding more content to reach the medium length classification. " * 5)  # Approx. 50 more words
        self.assertEqual(classify_document_length(text), 'medium')

    def test_classify_document_length_long(self):
        # Create a long text (more than 500 words)
        long_text = "This is a long document. " * 20  # 20 sentences, approx. 100 words
        long_text += "This additional sentence ensures it crosses the limit. " * 30  # 30 additional sentences, approx. 150 more words
        long_text += "Here we go with even more text to surpass 500 words. " * 20  # Additional sentences
        self.assertEqual(classify_document_length(long_text), 'long')

    def test_summarize_text_short(self):
        text = "This is a short sentence."
        expected = "This is a short sentence."  # Ensure this matches your implementation's output
        self.assertEqual(summarize_text(text, 'short'), expected)

    def test_summarize_text_medium(self):
        text = "Sentence one. Sentence two. Sentence three."
        expected = "Sentence one. Sentence two. Sentence three."  # Adjust if your function alters this
        self.assertEqual(summarize_text(text, 'medium'), expected)

    def test_summarize_text_long(self):
        text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
        expected = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."  # Adjust if your function alters this
        self.assertEqual(summarize_text(text, 'long'), expected)

if __name__ == "__main__":
    unittest.main()




