import json
import random
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

with open("dataset/student_queries.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# --------------------------------------------------
# NLTK setup
# --------------------------------------------------

stop_words = set(stopwords.words("english"))

# Add common conversational words
custom_stopwords = {
    "tell",
    "me",
    "about",
    "what",
    "when",
    "where",
    "how",
    "can",
    "could",
    "would",
    "please",
    "do",
    "does",
    "did",
    "is",
    "are",
    "was",
    "were",
    "the",
    "a",
    "an",
    "i",
    "my",
    "your",
    "you",
    "we",
    "they",
    "it",
    "to",
    "for",
    "of",
    "in",
    "on",
    "at",
    "and",
    "or",
    "any",
    "some",
    "there",
}

stop_words.update(custom_stopwords)

stemmer = PorterStemmer()


# --------------------------------------------------
# Text preprocessing
# --------------------------------------------------

def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and stem words
    processed_words = []

    for word in tokens:

        if word not in stop_words:
            processed_words.append(stemmer.stem(word))

    return processed_words


# --------------------------------------------------
# Normalize text
# --------------------------------------------------

def normalize_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Find user intent
# --------------------------------------------------

def find_intent(user_input):

    normalized_input = normalize_text(user_input)

    user_words = set(preprocess_text(user_input))

    # --------------------------------------------------
    # STEP 1: Exact normalized pattern match
    # --------------------------------------------------

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            normalized_pattern = normalize_text(pattern)

            if normalized_input == normalized_pattern:
                return intent


    # --------------------------------------------------
    # STEP 2: Strong keyword matching
    # --------------------------------------------------

    best_match = None
    highest_score = 0

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            pattern_words = set(preprocess_text(pattern))

            if not pattern_words:
                continue

            common_words = user_words.intersection(pattern_words)

            if not common_words:
                continue

            # Percentage of pattern keywords matched
            pattern_score = len(common_words) / len(pattern_words)

            # Percentage of user's keywords matched
            user_score = len(common_words) / max(len(user_words), 1)

            # Combined score
            score = (pattern_score * 0.6) + (user_score * 0.4)

            if score > highest_score:

                highest_score = score
                best_match = intent


    # --------------------------------------------------
    # Minimum confidence
    # --------------------------------------------------

    if highest_score < 0.35:
        return None

    return best_match


# --------------------------------------------------
# Generate response
# --------------------------------------------------

def get_response(user_input):

    intent = find_intent(user_input)

    if intent is None:

        return (
            "Sorry, I don't have information about that. "
            "Please ask me about courses, fees, admission, "
            "exams, timings, attendance, scholarships, "
            "or contact information."
        )

    return random.choice(intent["responses"])