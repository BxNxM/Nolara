# Nolara is a locally-run AI assistant

> Powered by Ollama and cutting-edge open models. Designed for privacy, speed, and versatility, Nolara offers intelligent, offline-friendly assistance without relying on the cloud. Whether you’re coding, creating, or just curious, Nolara is your ever-present, whisper-smart companion—right on your machine.

![NolaraTUI](./media/NolaraTUI.png?raw=true)

## 1. Prerequisite

### 1.1. Install ollama

```bash
https://ollama.com
```

### 1.2. Setting Up a Python Virtual Environment and Installing Requirements

Follow these steps to create a virtual environment using `virtualenv`, install dependencies from `requirements.txt`, and activate the environment.

```bash
# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> This command you will need to activate the virtual environment: `source .venv/bin/activate`


### 1.3. Install models

**Small profile**

```bash
ollama pull gemma2:latest
ollama pull gemma3:4b
ollama pull qwen3:8b
```

**Medium profile**

```bash
ollama pull gemma2:latest
ollama pull gemma3:12b
ollama pull qwen3:14b
```


#### Model informations

Current promising models

[gemma2 details](https://ollama.com/library/gemma2)

[gemma3 details](https://ollama.com/library/gemma3)

[qwen3 details](https://ollama.com/library/qwen3)

```bash
ollama list

gemma2:latest              ff02c3702f32    5.4 GB
gemma3:12b                 f4031aab637d    8.1 GB
```

Reasoning models + Tools

```bash
qwen3:14b                  7d7da67570e2    9.3 GB
```

## 2. Start the Nolara chat interface

```bash
cd Nolara
source .venv/bin/activate
./tui.py
```

---------------------------------------------------------------

## Additional models for Ollama Coding Buddy

Coding models (Continue plugin)

[continue.dev](https://docs.continue.dev/customize/model-providers/ollama/)

```
codellama:13b              9f438cb9cd58    7.4 GB
qwen2.5-coder:7b           2b0496514337    4.7 GB

Embedding:
nomic-embed-text:latest    0a109f422b47    274 MB
```

git push -u origin main

