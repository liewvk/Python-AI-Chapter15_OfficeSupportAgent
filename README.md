# Chapter 15 — Office Productivity and Customer Support AI Agent

Educational Python project for **Visual Studio 2026**, **Ollama**, and **Qwen 3.5**.

## Open in Visual Studio 2026

1. Extract the source ZIP into one folder. **Do not open Folder View.**
2. Open `Chapter15_OfficeSupportAgent.sln` using **Open a project or solution**.
3. Open Developer PowerShell in the folder containing `main.py` and `requirements.txt`.
4. Create your environment and install the required Python package:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Set the project interpreter to `<this-folder>\.venv\Scripts\python.exe` if Visual Studio did not detect it automatically.
6. Ensure Ollama is running and install the model with `ollama pull qwen3.5:9b`.
7. Set `main.py` as Startup File and use **Ctrl+F5**.

For computers with less memory, change `MODEL_NAME` in `settings.py` to `qwen3.5:4b`, then run `ollama pull qwen3.5:4b`.

## Features

1. Draft office emails (preview only; no sending)
2. Summarize short office notes
3. Answer support questions using five **fictional** FAQ entries
4. Classify tickets into a category and priority, pending human review
5. List FAQ topics

The app does not connect to email, a help desk, or a live customer database. Do not enter real customer secrets or confidential information. FAQ retrieval is simple keyword matching: it is not a full RAG vector search.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use a fake Ollama client and can be run without a live Ollama server after dependencies are installed (indeed the tests don't import Ollama until a real client is requested).

## Suggested screenshots

- Solution Explorer showing the `.sln`, Python Environments and four `.py` files
- Menu with five options
- Email draft with Subject line
- Office note summary
- FAQ-based response showing source IDs
- Ticket classification and manual-review reminder

## Project structure

```text
Chapter15_OfficeSupportAgent.sln
Chapter15_OfficeSupportAgent.pyproj
main.py
settings.py
knowledge_base.py
agent.py
requirements.txt
data/support_faq.json
tests/test_agent.py
README.md
.gitignore
```
