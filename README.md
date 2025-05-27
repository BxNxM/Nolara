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
pip install virtualenv
virtualenv venv

source venv/bin/activate
pip install -r requirements.txt
```


### 1.3. Install models

Current promising models

Chat models

```
gemma3:12b                 f4031aab637d    8.1 GB
gemma2:latest              ff02c3702f32    5.4 GB
```

Reasoning models + Tools

```
qwen3:14b                  7d7da67570e2    9.3 GB
```

## 2. Start the Nolara chat interface

```bash
cd Nolara
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

