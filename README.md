<div align="center">

# 🤖 Repo Agent

### *AI-powered repository documentation and test generation tool* ✨

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?style=for-the-badge&logo=ollama)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[🚀 **Quick Start**](#-quick-start) • [📖 **Features**](#-features) • [🛠️ **Usage**](#-usage-examples) • [⚙️ **Configuration**](#-configuration)

---

*Automatically generate professional README files, test suites, and development scripts for any GitHub repository using free, local LLMs (Ollama). No API costs, complete privacy.*

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 **Documentation Generation**
- **Professional README.md** with stunning visual design
- **HTML-enhanced layouts** with centered sections
- **Smart badge generation** for tech stack
- **Emoji-rich formatting** matching project type
- **Comprehensive structure** (installation, usage, examples)

</td>
<td width="50%">

### 🧪 **Test & Script Generation**
- **Automated test suites** based on detected framework
- **Development scripts** for common tasks
- **Best-effort validation** with dependency installation
- **Monorepo support** for multi-package projects
- **Timeout protection** prevents hanging processes

</td>
</tr>
</table>

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Ollama** (for local LLM inference)
- **Git** (for repository cloning)

### Quick Start

```bash
# Install Ollama
# Visit: https://ollama.ai/ and download for your OS

# Pull a recommended model
ollama pull llama3.1:8b
# OR for code-focused tasks
ollama pull deepseek-coder:6.7b

# Clone this repository
git clone https://github.com/yourusername/repo-agent.git
cd repo-agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```bash
repo-agent/
├── src/
│   ├── main.py                    # CLI entry point
│   ├── analysis/
│   │   ├── build_context.py       # Extract repo context for LLM
│   │   └── detect_stack.py        # Auto-detect tech stack
│   ├── generate/
│   │   ├── readme.py              # Generate README files
│   │   ├── tests.py               # Generate test suites
│   │   └── scripts.py             # Generate dev scripts
│   ├── ingest/
│   │   └── clone_repo.py          # Clone GitHub repositories
│   ├── llm/
│   │   ├── client.py              # Ollama LLM client
│   │   └── prompts.py             # System prompts & templates
│   └── utils/
│       ├── fs.py                  # File system operations
│       ├── log.py                 # Colored logging
│       ├── run_cmd.py             # Command execution with timeout
│       └── validate.py            # Validation & testing
├── workspace/                     # Generated outputs (gitignored)
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 🎨 Tech Stack

<div align="center">

**Core Framework**  
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)

**AI/LLM**  
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000?style=flat)
![LLaMA](https://img.shields.io/badge/LLaMA-3.1-412991?style=flat)

**Git Integration**  
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github)

</div>

---

## 🎯 Key Features Breakdown

### 🤖 **Smart Stack Detection**
- **Auto-detects** programming language (Python, JavaScript/TypeScript, Go, Rust)
- **Identifies** package managers (npm, yarn, pnpm, pip)
- **Finds** test frameworks (pytest, Jest, etc.)
- **Recognizes** monorepo structures

### 📝 **Context-Aware Generation**
- **Analyzes** repository structure and code
- **Extracts** dependencies, scripts, and key files
- **Builds** comprehensive context for LLM
- **Generates** accurate documentation based on actual code

### 🎨 **Professional README Templates**
- **Centered headers** with HTML styling
- **Badge generation** for tech stack
- **Feature comparison tables** with split layouts
- **Domain-specific emojis** (Web, Gaming, Data Science, etc.)
- **Navigation links** and "Back to Top" buttons
- **Collapsible sections** for detailed content

### ⚡ **Performance & Reliability**
- **Timeout protection** (120s default for commands)
- **Graceful error handling** for missing tools
- **Windows compatibility** with shell=True
- **Monorepo detection** for multi-package projects
- **Skips hanging tests** (watch mode prevention)

---

## 🚀 Usage Examples

### Basic Usage
```bash
# Generate documentation for a repository
python -m src.main --repo https://github.com/username/repo --model llama3.1:8b
```

### Advanced Options
```bash
# Custom workspace and model
python -m src.main \
  --repo https://github.com/username/repo \
  --model deepseek-coder:6.7b \
  --workspace ./my-output \
  --max-files 50 \
  --max-bytes 150000

# Skip scripts and validation
python -m src.main \
  --repo https://github.com/username/repo \
  --model llama3.1:8b \
  --no-scripts \
  --no-validate
```

### CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | *required* | GitHub repository URL |
| `--model` | `llama3.1:8b` | Ollama model name |
| `--workspace` | `workspace` | Output directory |
| `--max-files` | `40` | Max files to analyze |
| `--max-bytes` | `120000` | Max context size |
| `--no-scripts` | `false` | Skip script generation |
| `--no-validate` | `false` | Skip validation |

---

## ⚙️ Configuration

<details>
<summary>Click to expand configuration details</summary>

### Ollama Models

**Recommended Models:**
- **llama3.1:8b** — Best for general documentation (8GB RAM)
- **deepseek-coder:6.7b** — Optimized for code (7GB RAM)
- **codellama:7b** — Code-focused alternative (7GB RAM)

**Pull additional models:**
```bash
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b
```

### Environment Variables

```bash
# Optional: Set Ollama host (default: http://localhost:11434)
export OLLAMA_HOST=http://localhost:11434
```

### Customizing Prompts

Edit `src/llm/prompts.py` to customize:
- **README_SYSTEM** — README generation template
- **TESTS_SYSTEM** — Test generation rules
- **SCRIPTS_SYSTEM** — Script generation rules

</details>

---

## 🧪 Testing

```bash
# Run tests on generated repositories (manual)
cd workspace/username__repo
npm test  # or pytest, cargo test, etc.

# The tool automatically validates after generation
# Use --no-validate to skip
```

---

## 🛠️ Development

### Setup Development Environment
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`
5. Install Ollama and pull models

### Code Structure
- **Modular design** — separate concerns (analysis, generation, ingestion)
- **Type hints** — for better IDE support
- **Error handling** — graceful failures with warnings
- **Logging** — colored console output with log levels
- **Cross-platform** — Windows and Unix compatibility

---

## 🗺️ Roadmap

- [ ] **Support more languages** (Java, Ruby, PHP)
- [ ] **Custom templates** for README generation
- [ ] **Interactive mode** for user feedback
- [ ] **GitHub Actions integration** for CI/CD
- [ ] **Web UI** for easier usage
- [ ] **Batch processing** for multiple repositories
- [ ] **Diff-based updates** for existing READMEs

---

## 🤝 Contributing

- 🐛 **Bug reports** → [Open an issue](https://github.com/yourusername/repo-agent/issues)
- ✨ **Feature requests** → Propose via issues
- 🔧 **Pull requests** → Fork, branch, commit, push, open PR

**Contribution Guidelines:**
1. Follow PEP 8 style guide
2. Add type hints to functions
3. Include docstrings for modules/classes
4. Test on both Windows and Unix if possible
5. Update README if adding features

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author

<div align="center">

### **Your Name**
*Python Developer & AI Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-yourusername-181717?style=for-the-badge&logo=github)](https://github.com/yourusername)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-YourName-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![Email](https://img.shields.io/badge/Email-your%40email.com-EA4335?style=for-the-badge&logo=gmail)](mailto:your@email.com)

</div>

---

<div align="center">

🤖 **Powered by Ollama — Free, Fast, and Private AI** 🚀

⭐ If this tool saves you time, give it a star! ⭐

**[⬆ Back to Top](#-repo-agent)**

</div>
