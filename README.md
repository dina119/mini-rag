# Mini RAG Application

## Description
This is a mini **Retrieval-Augmented Generation (RAG)** application.  
It combines information retrieval with generative AI to produce accurate and context-aware answers.  
The application retrieves relevant data from a knowledge source and augments the prompt for a language model, improving the quality of the generated responses.

---

## Getting Started

Follow these steps to set up and run the application locally.

### 1. Clone the repository
```bash
git clone git@github.com:username/mini-rag.git
cd mini-rag
```
### 2. Create and activate a virtual environment
It is recommended to use a Python virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
Install all required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```
### 4. Configure environment variables
The application uses environment variables for configuration.

1. Copy the `.env.example` file and create your own `.env` file:
```bash
cp .env.example .env
```
### 5. Run the application
After setting up the environment variables, you can start the application by running:

```bash
python app.py
```
### 5.Run FastAPI server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
