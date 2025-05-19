# 🧠 Tally AI Infra — Chat-Based Financial Q&A with Local RAG

A minimal, local-first clone of Tally's AI infrastructure. Users ask financial questions in natural language — the system retrieves relevant context from uploaded documents and responds using a local LLM (via Ollama) or remote providers.

## 🚀 Features

- Natural language financial Q&A
- Retrieval-Augmented Generation (RAG) with LangChain
- Embedding & vector search using PostgreSQL + pgvector
- Multi-provider LLM routing (OpenAI, Ollama, etc.)
- Local LLM integration using [Ollama](https://ollama.com/)
- FastAPI backend with async endpoints
- Document upload & ingestion

---

## 📁 Folder Structure

```

tally-ai-infra/
│
├── app/                        # Main FastAPI app
│   ├── main.py                 # FastAPI entrypoint
│   ├── api/                    # API routes
│   │   ├── routes.py           # /ask and /upload endpoints
│   ├── core/                   # Core logic
│   │   ├── rag.py              # RAG pipeline (embed, retrieve, generate)
│   │   ├── embeddings.py       # Embedding logic (e.g., OpenAI/BGE)
│   │   ├── schema.py           # Pydantic schemas
│   │   ├── model\_router.py     # Multi-LLM routing (OSS vs OpenAI)
│   │   └── utils.py
│   └── config.py               # Env var handling, constants
│
├── db/
│   └── dummy_data_apple.txt    # Dummy data to test Apple 2023's financials.
│
├── models/                     # Optional: LLM hosting setup
│   └── local\_model\_server.py         # Entrypoint to run local model
│
├── docker/
│   └── postgres/               # Postgres + pgvector container      (Not yet implemented)
│       └── Dockerfile
│
├── scripts/                    # One-off utils
│   ├── embed\_documents.py      # CLI tool to embed & store documents
│
├── .env                        # API keys, DB URL
├── docker-compose.yml          # Full stack: FastAPI + Postgres + vLLM     (Not yet)
├── requirements.txt            # Python deps
├── README.md                   # Setup & usage guide
└── .gitignore

````

---

## ⚙️ Local Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
````

2. **Enable Ollama and run a local model**

   ```bash
   ollama run llama3
   ```

3. **Start the FastAPI server**

   ```bash
   uvicorn app.main:app --reload --port 6000
   ```

---

## 📤 API Usage

### POST `/api/upload`

Upload a `.txt` file containing financial data to embed.

```bash
curl -X POST http://localhost:6000/api/upload \
  -F "file=@dummy_data_apple.txt"
```

---

### POST `/api/ask`

Ask a question related to the ingested content.

```bash
curl -X POST http://localhost:6000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the revenue of Apple in 2023?"}'
```

#### Example response

```json
{
  "result": {
    "revenue": "$394.3 billion",
    "net_income": "$99.8 billion",
    "period": "Q4 2023"
  }
}
```

---

## 📦 Tech Stack

* **Backend:** FastAPI
* **LLM Runtime:** [Ollama](https://ollama.com)  (Llama3.2:1b)
* **Embedding & Vector DB:** PostgreSQL + pgvector
* **RAG Orchestration:** LangChain
* **Deployment:** Docker (Postgres), Local runtime for LLM

---

## 📝 Roadmap

* [ ] Containerize full stack (FastAPI + Ollama + Postgres)
* [ ] Add support for remote LLM fallback (e.g., OpenAI)
* [ ] Benchmark inference speed & quality (OSS vs GPT-4)
* [ ] Deploy on cloud (EC2 or ECS)

---

## 🧠 Inspired By

[Tally](https://asktally.com/) — Chat-based business intelligence for financial data

> 📌 Currently local-only due to EC2 resource limitations. Full deployment coming soon.
