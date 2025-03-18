# DIY Resume Master

DIY Resume Master is a local, on-device AI-powered resume optimization tool. This modular project lays the foundation for our application. In this push, we have built core modules for document extraction, web scraping, LLM inference (via OpenAI’s API), and LaTeX-based PDF generation. **Note:** We still need to work on integrating the local LLM using Ollama.

## Features
- **Document Extraction:** Upload your master resume as a PDF or DOCX.
- **Web Scraping:** Retrieves job descriptions from a URL.
- **LLM Inference:** Uses OpenAI’s API (4o mini engine) for resume optimization. (A stub is provided for future local LLM integration via Ollama.)
- **LaTeX & PDF Generation:** Converts the optimized resume into a nicely formatted PDF using LaTeX.

## Requirements
- Python 3.8+
- **LaTeX Distribution:**  
  For PDF generation, you need to install a LaTeX distribution on your Mac. We recommend using [BasicTeX](https://tug.org/mactex/morepackages.html#basics), which is a lightweight alternative to the full MacTeX.

### Installing BasicTeX on macOS
1. **Install BasicTeX via Homebrew:**
   ```bash
   brew install --cask basictex

### Set Up Your PATH:
- Open your shell configuration file (e.g., ~/.zshrc for zsh or ~/.bash_profile for bash)
   ```bash
   vim ~/.zshrc

- Add the following line:
   ```bash
   export PATH="/Library/TeX/texbin:$PATH"

- Save the file and reload your shell configuration::
   ```bash
   source ~/.zshrc

- Verify that pdflatex is accessible:
   ```bash
   which pdflatex
- You should see something like /Library/TeX/texbin/pdflatex.

- OpenAI API Key: Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"

- Install Dependencies:
   ```bash
   pip install -r requirements.txt

- Run the Streamlit App:
   ```bash
   streamlit run main.py

- Enjoy





