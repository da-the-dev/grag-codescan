# Github's repo semantic graph generation

## Description

Our project is dedicated to graph constuction of the most important code repository semantic components. We use LLM and several stages of applying prompt to retreive significat and relevant information without putting all codebase in the context.

## Gradio

![alt](./imgs/demo.gif)

## How to run

### Prerequisites

- [uv](https://docs.astral.sh/uv/#installation)

### Python 3.12

```bash
uv python install 3.12
```

### Sync project's dependencies state

```bash
uv sync
```

### Debug

```bash
uvx gradio main.py
```

### Run

```bash
uv run main.py
```

---

## Contributors

- Alexey Tkachenko <a.tkachenko@innopolis.university>
- Anatoly Soldatov <a.soldatov@innopolis.university>
