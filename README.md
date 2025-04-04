# Github's repo semantic graph generation

## Description

Our project is dedicated to graph constuction of the most important code repository semantic components. We use LLM and several stages of applying prompt to retreive significat and relevant information without putting all codebase in the context.

## Gradio

![alt](./imgs/demo.gif)

## How to run

### Prerequisites

- [uv](https://docs.astral.sh/uv/#installation)
- [ollama](https://ollama.com/download)

### Python 3.12

```bash
uv python install 3.12
```

### Sync project's dependencies state

```bash
uv sync
```

### Ollama pull model

```bash
uvx ollama pull qwen2.5-coder
```

### Debug

```bash
uvx gradio main.py
```

### Run

```bash
uv run main.py
```

### Run via docker

```bash
docker compose up
```

---

## Contributors

- Alexey Tkachenko <a.tkachenko@innopolis.university>
- Anatoly Soldatov <a.soldatov@innopolis.university>
