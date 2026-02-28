<div align="center">

# KimochiBot

**An intelligent, sentiment-aware customer support chatbot with analytics — powered by RAG, FAISS, and local LLMs.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?logo=streamlit&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-0467df)
![License](https://img.shields.io/badge/License-MIT-green)

[Features](#features) · [Architecture](#architecture) · [Quick Start](#quick-start) · [Usage](#usage) · [Contributing](#contributing)

</div>

---

## Why KimochiBot?

Most support chatbots respond with the same flat tone regardless of how a user feels. **KimochiBot** (気持ち = "feeling" in Japanese) detects user sentiment in real time and adjusts its tone — empathetic for frustrated users, cheerful for happy ones — while grounding every answer in an up-to-date knowledge base via Retrieval-Augmented Generation.

It is built as three composable modules that work independently or together:

| Module | Purpose | Stack |
|--------|---------|-------|
| **Task 1 — Analytics Dashboard** | Visualize query volume, satisfaction trends, and top topics | Flask, Pandas, Jinja2 |
| **Task 2 — RAG Chatbot** | Answer questions using embedded documents + local LLM | FAISS, Sentence-Transformers, Ollama |
| **Task 3 — Sentiment Engine** | Classify user emotion and adapt chatbot tone accordingly | NLTK VADER, Streamlit |

---

## Features

- **Retrieval-Augmented Generation** — Embeds source documents with MiniLM, indexes them in FAISS, and retrieves the most relevant chunks for every query.
- **Sentiment-Aware Responses** — VADER-based analysis adjusts tone (positive / neutral / negative) so the bot replies with appropriate empathy.
- **Live Analytics Dashboard** — Flask web UI showing total queries, average satisfaction (color-coded), and a ranked topic chart with progress bars.
- **Auto-Updating Knowledge Base** — Background scheduler re-ingests documents from `sources/` on a configurable interval.
- **Admin CLI** — Terminal tool to inspect sources, view vector DB stats, check last update time, or trigger a manual refresh.
- **Fully Local** — No external API keys required; runs entirely on your machine via Ollama.

---

## Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                      User Interface                      │
│  Streamlit Chat UI (Task-3)   Flask Dashboard (Task-1)   │
└────────────┬─────────────────────────┬───────────────────┘
             │                         │
             ▼                         ▼
┌────────────────────────┐   ┌─────────────────────────────┐
│   RAG Pipeline (Task-2)│   │  Analytics Engine (Task-1)  │
│                        │   │                             │
│  ┌──────────────────┐  │   │  CSV Logger → Pandas →      │
│  │ Sentence-         │  │   │  total_queries()            │
│  │ Transformers      │  │   │  most_common_topics()       │
│  │ (MiniLM encoder)  │  │   │  average_satisfaction()     │
│  └───────┬──────────┘  │   └─────────────────────────────┘
│          ▼             │
│  ┌──────────────────┐  │
│  │  FAISS Vector DB  │  │
│  └───────┬──────────┘  │
│          ▼             │
│  ┌──────────────────┐  │
│  │  Ollama (LLaMA 3) │  │
│  └──────────────────┘  │
└────────────────────────┘
             ▲
             │
┌────────────────────────┐
│ Sentiment Analyzer      │
│ (VADER — Task-3)        │
│ positive / neutral /    │
│ negative → tone guide   │
└─────────────────────────┘
```

---

## Quick Start

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10 + | Tested on 3.10 – 3.12 |
| pip | latest | Comes with Python |
| Ollama | latest | Required only for Task 2 — [install guide](https://ollama.com) |
| Git | any | To clone the repo |

### 1. Clone the repository

```bash
git clone https://github.com/Karthik0000007/KimochiBot.git
cd KimochiBot
```

### 2. Set up each module

<details>
<summary><strong>Task 1 — Analytics Dashboard</strong></summary>

```bash
cd Task-1
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To enable debug mode (development only):

```bash
# Windows PowerShell
$env:FLASK_DEBUG="true"; python app.py

# Linux / macOS
FLASK_DEBUG=true python app.py
```

</details>

<details>
<summary><strong>Task 2 — RAG Chatbot</strong></summary>

```bash
cd Task-2
pip install -r requirements.txt
```

Start the Ollama model in a separate terminal:

```bash
ollama run llama3
```

Then launch the chatbot:

```bash
python -m chatbot.chatbot
```

**Admin CLI** (optional) — manage the knowledge base:

```bash
python -m utils.admin_cli
```

</details>

<details>
<summary><strong>Task 3 — Sentiment-Aware Chat UI</strong></summary>

```bash
cd Task-3
pip install -r requirements.txt
streamlit run app.py
```

The Streamlit UI opens automatically at **http://localhost:8501**.

> **Note:** Task 3 imports the RAG pipeline from Task 2. Make sure Task 2's dependencies are installed and Ollama is running.

</details>

---

## Usage

### Analytics Dashboard (Task 1)

Navigate to `http://127.0.0.1:5000` after starting the Flask server. The dashboard displays:

| Metric | Description |
|--------|-------------|
| **Total Queries** | Number of logged interactions |
| **Avg. Satisfaction** | Mean rating (1–5), color-coded green / yellow / red |
| **Unique Topics** | Count of distinct topic categories |
| **Top Topics** | Ranked list with proportional progress bars |

Interactions are logged to `customer_service_interactions.csv` via the `chatbot_logger` module:

```python
from chatbot_logger import log_interaction

log_interaction(
    user_id="user123",
    message="Where is my order?",
    response="Your order is on the way.",
    topic="Order Status",
    satisfaction=4,
)
```

### RAG Chatbot (Task 2)

```text
$ python -m chatbot.chatbot

Enter your question:
> What's the status of my order? I was promised it would arrive yesterday.

Detected sentiment: negative
Tone: Be empathetic, apologize briefly, and offer clear solutions.

Response:
I'm sorry to hear your order hasn't arrived on time. Let me look into this
for you. Please share your order number and I'll check the latest status...
```

### Sentiment Analyzer (Task 3)

```python
from sentiment.analyzer import analyze_sentiment

analyze_sentiment("I'm really disappointed in this service.")
# → "negative"

analyze_sentiment("Thanks, it was very helpful!")
# → "positive"

analyze_sentiment("This is fine, I guess.")
# → "neutral"
```

---

## Project Structure

```text
KimochiBot/
│
├── Task-1/                          # Analytics Dashboard
│   ├── app.py                       # Flask application entry point
│   ├── analytics_utils.py           # Data loading & metric calculations
│   ├── chatbot_logger.py            # CSV interaction logger
│   ├── customer_service_interactions.csv
│   ├── requirements.txt
│   └── templates/
│       └── dashboard.html           # Jinja2 dashboard template
│
├── Task-2/                          # RAG Chatbot
│   ├── chatbot/
│   │   └── chatbot.py               # RAG pipeline & Ollama integration
│   ├── embeddings/
│   │   └── embedder.py              # MiniLM text chunking & encoding
│   ├── vector_store/
│   │   ├── fiass_db.py              # FAISS index wrapper
│   │   ├── faiss_index              # Serialized FAISS index
│   │   └── last_update.txt          # Timestamp of last DB refresh
│   ├── utils/
│   │   ├── auto_updater.py          # Background scheduler for re-indexing
│   │   └── admin_cli.py             # CLI for knowledge base management
│   ├── sources/
│   │   └── support_ai.txt           # Source documents for embedding
│   └── requirements.txt
│
├── Task-3/                          # Sentiment-Aware Chat UI
│   ├── app.py                       # Streamlit chat interface
│   ├── sentiment/
│   │   ├── analyzer.py              # VADER sentiment classifier
│   │   └── test_analyzer.py         # Sentiment test suite
│   └── requirements.txt
│
└── README.md
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_DEBUG` | `false` | Set to `true` for hot-reload during development |
| Auto-update interval | 30 min | Change in `auto_updater.py` → `start_scheduler(interval_minutes=30)` |
| Sentiment thresholds | ±0.3 | Adjust `compound` cutoffs in `analyzer.py` |
| Ollama model | `llama3` | Change in `chatbot.py` → `query_ollama(prompt, model_name="llama3")` |
| Top-K retrieval | 3 | Adjust in `generate_rag_response(user_query, top_k=3)` |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** — keep commits small and focused.
4. **Test** your changes:
   ```bash
   # Task 3 sentiment tests
   cd Task-3/sentiment
   python test_analyzer.py
   ```
5. **Push** and open a **Pull Request** against `main`.

### Code Style

- Python follows [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use type hints for function signatures.
- Add docstrings to all public functions.
- Use `logging` instead of `print()` for diagnostics.

---

## Roadmap

- [ ] Consolidated `requirements.txt` with pinned versions
- [ ] Docker Compose setup for one-command deployment
- [ ] Unit tests for `analytics_utils.py` and `chatbot.py`
- [ ] WebSocket-based live dashboard updates
- [ ] Transformer-based sentiment model (replacing VADER) for higher accuracy
- [ ] Multi-language support

---

## License

This project is available under the [MIT License](LICENSE).

---

<div align="center">
<sub>Built with care by <a href="https://github.com/Karthik0000007">Karthik</a></sub>
</div>
