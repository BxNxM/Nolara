# Nolara is a locally-run AI assistant

> Powered by Ollama and cutting-edge open models. Designed for privacy, speed, and versatility, Nolara offers intelligent, offline-friendly assistance without relying on the cloud. Whether you’re coding, creating, or just curious, Nolara is your ever-present, whisper-smart companion—right on your machine.

![NolaraTUI](./media/NolaraTUI.png?raw=true)

## 1. Prerequisite

### 1.1. Install ollama

```bash
https://ollama.com
```

### 1.2 Build nolara app

```bash
cd Nolara
./build.bash
```

### 1.3 Run nolara app

```bash
nolara
```

Other examples:

```bash
nolara --help
cat README | nolara -p "Summarize please"
```

> Then you have system wide `nolara` command available.

![NolaraTUI2](./media/NolaraTUI2.png?raw=true)

## Customzation

### 💬 system_prompts

Add **custom system prompts** under

```bash
(.venv) ➜  Nolara git:(main) ✗ ll ~/.nolara/system_prompts/
total 16
-rw-r--r--@ 1 usr  staff    52B May 31 16:39 basic.txt
-rw-r--r--@ 1 usr  staff    68B May 31 12:52 short.txt
```

### 🛠️ tools

Add **custom tools** under

```bash
(.venv) ➜  Nolara git:(main) ✗ ll ~/.nolara/tools/
total 8
-rw-r--r--@ 1 usr  staff   606B May 31 18:14 basic.py
-rw-r--r--@ 1 usr  staff     0B May 31 18:34 websearch.py
```

## Configuration

```bash
cat ~/.nolara/config.json
```

```json
{
  "tools": ["*", "!micros_tools.py"],
  "language":"en-US",
  "models": ["qwen3:4b", "llama3.2:1b", "gemma2:latest"]
}
```

> **tools**: Select tools for agentic models (Nolara/tools/*.py), `*` or `all` means select all tools. Disable tool with `!`. You can add modules individually as well.

> **language**: Under development

> **models**: required models with autoinstall (ollama pull)

## Nolara as a command line tool (beta)

```bash
(.venv) ➜  Nolara git:(main) ✗ cat README.md | ./main.py -p "Summarize the content in few sentences"

.../usr_config.json already exists
Check config updates...
	No updates needed.
[1/2] Model qwen3:4b already available.
[2/2] Model gemma2:latest already available.

Processing...

Nolara is a privacy-focused, open-source AI assistant powered by Ollama and
cutting-edge models. It runs locally on your machine without relying on the
cloud, offering intelligent assistance for coding, creative tasks, and general
inquiries.

To use Nolara, you need to install Ollama, set up a Python virtual environment,
install required dependencies, and download the desired models. You can then
start the Nolara chat interface and customize it with system prompts and tools.
The project also provides configuration options for selecting specific models
and tools.
```


## Model handling TL;DR

#### Manual install:

**Small profile example**

```bash
ollama pull gemma2:latest
ollama pull gemma3:4b
ollama pull qwen3:4b
```

**Medium profile example**

```bash
ollama pull gemma2:latest
ollama pull gemma3:12b
ollama pull qwen3:8b
```


#### Model info

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


## Development envoronment 

### Setting Up a Python Virtual Environment and Installing Requirements

Follow these steps to create a virtual environment using `virtualenv`, install dependencies from `requirements.txt`, and activate the environment.

```bash
cd Nolara/

# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install base dependencies
pip install -r ./nolara/requirements/requirements-base.txt

# Install Audio dependencies (optional)
pip install -r ./nolara/requirements/requirements-audio.txt
```


> This command you will need to activate the virtual environment: `source .venv/bin/activate`


### Start the Nolara chat interface

```bash
cd Nolara
source .venv/bin/activate
./nolara/main.py
```

---------------------------------------------------------------
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

