# AI Student Query Chatbot - College Minor Project

An end-to-end Machine Learning web-based AI Chatbot designed to automate student enquiries regarding Admissions, Courses, Fees, Examinations, Internships, Placements, and Campus Facilities.

## Tech Stack
- **Backend Framework:** Python & Flask
- **Machine Learning & NLP:** Scikit-Learn (TF-IDF Vectorization, Multinomial Naive Bayes), NLTK
- **Frontend Interface:** HTML5, CSS3, JavaScript (Fetch API, Session Storage)
- **Dataset Format:** CSV (`dataset.csv`)

## Project Architecture
1. **Data Preprocessing Pipeline:** Lowercasing, noise removal, tokenization, stop-word removal, and Lemmatization via `NLTK`.
2. **Feature Extraction:** `TfidfVectorizer` (Unigram + Bigram feature representation).
3. **Intent Classifier:** `MultinomialNB` model predicting probability distributions across candidate intents.
4. **Confidence Thresholding:** Requests falling below a probability threshold of 0.35 trigger an automated fallback mechanism.
5. **RESTful Web Service:** Flask API routing user requests to model inference and returning JSON responses.

## Setup & Installation

### Step 1: Clone or Set Up Directory
Create the project folder and structure as outlined in the documentation.

### Step 2: Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
