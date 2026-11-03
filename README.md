# AI Agent Project

A command-line AI coding agent written in Python. You give it a request in plain English, and it plans and runs a sequence of tool calls (listing files, reading code, running scripts, writing files) until it can give a final answer.

It uses the OpenAI Python SDK pointed at [OpenRouter](https://openrouter.ai), so it runs on free models.

## How it works

1. Your prompt and a system prompt go to the model, along with the schemas of the available tools.
2. If the model asks for a tool call, the agent runs the matching Python function and sends the result back.
3. This loop repeats (up to 20 iterations) until the model replies with a final answer.

### Available tools

| Tool | What it does |
| --- | --- |
| `get_files_info` | Lists the files in a directory, with sizes and whether each is a directory |
| `get_file_content` | Reads a file (truncated at 10,000 characters) |
| `run_python_file` | Runs a `.py` file with optional arguments and returns stdout and stderr |
| `write_file` | Creates or overwrites a file |

### Sandboxing

Every tool call is locked to the `./calculator` working directory. The working directory is injected by the agent, not chosen by the model, and each function rejects any path that resolves outside it.

## Project structure

```
.
├── main.py              # CLI entry point and agent loop
├── call_function.py     # Maps tool calls from the model to Python functions
├── functions/           # Tool implementations and their JSON schemas
├── tests/               # Tests for each tool
└── calculator/          # Sample project the agent works on
```

## Getting started

### Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An [OpenRouter API key](https://openrouter.ai/keys)

### Setup

```bash
git clone https://github.com/danielakinremi1-dev/AI_Agent_project.git
cd AI_Agent_project
uv sync
```

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_key_here
```

### Usage

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to print token usage, each function call's arguments, and tool results:

```bash
uv run main.py "fix the bug in the calculator" --verbose
```

### Example prompts

- `"what files are in the root?"`
- `"read main.py and explain how the calculator renders results"`
- `"run tests.py and tell me if anything fails"`
- `"create a file called notes.txt with a summary of the project"`

## Running tests

```bash
uv run tests/test_get_files_info.py
uv run tests/test_get_file_content.py
uv run tests/test_run_python_file.py
uv run tests/test_write_file.py
```

## Built with

- Python 3.13
- OpenAI Python SDK (via OpenRouter)
- python-dotenv
- uv
