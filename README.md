# UNICC AI Safety Lab
## Project 3 — Testing, User Experience, and Integration

**Student:** Galaxy Okoro — Project 3
**Course:** NYU MASY GC-4100 Applied Project Capstone — Spring 2026
**Team:** Coreece Lopez (P1) · Feruza Jubaeva (P2) · Galaxy Okoro (P3)

---

## What This Project Is

Project 3 provides the user-facing web interface for the UNICC AI Safety Lab. A UNICC staff member opens it in a browser, types a description of an AI agent they want to evaluate, clicks Evaluate, and receives a formatted safety report showing each judge's individual assessment and a final SAFE or UNSAFE verdict.

---

## How to Run — Two Options

### Option 1 — Local (No API Key Needed)
1. Install Ollama from https://ollama.com
2. Run: ollama pull mistral:7b-instruct
3. Run: ollama serve
4. Run: pip install -r requirements.txt
5. Run: streamlit run app.py
6. A browser window opens automatically

### Option 2 — Sandbox and Automated Environments
1. Set your API key: export ANTHROPIC_API_KEY=your_key_here
2. Run: pip install -r requirements.txt
3. Run: streamlit run app.py

The system automatically uses Ollama if it is running. If Ollama is not available it switches to the Anthropic API using the key in your environment.

---

## For DGX Sandbox Evaluators

Add this environment variable in your sandbox settings before running:

Name: ANTHROPIC_API_KEY
Value: your_anthropic_api_key

Then submit the GitHub repo link and run the project check.

---

## Understanding the Results

| Score | Meaning |
|-------|---------|
| 0.0 to 0.49 | Low risk — no significant concerns found |
| 0.50 to 0.74 | Moderate risk — some concerns identified |
| 0.75 to 1.0 | High risk — significant concerns found |

Final verdict requires two of three judges to agree. One judge cannot approve or block an agent alone.

---

## Running Tests

pytest tests/

---

## Repository Structure

UNICC_galaxy_project3/
├── app.py                 Galaxy's web interface — run this
├── main.py                Feruza's CLI entry point
├── requirements.txt       requests, pytest, anthropic, streamlit
├── README.md              This file
├── judges/                Feruza's three judge modules
├── council/               Council orchestration and arbitration
├── output/                Report assembly
└── tests/                 Test suite
