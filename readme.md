# Image Classification Project on Instagram Content

This repository contains:
- A **Label Studio labeling interface** (`label_config.xml`)
- A **taxonomy & annotation guidelines** (`TAXONOMY.md`)
- A **class list** (`classes.json`) for reference
- Setup instructions for installing and running **Label Studio**
- A **script** to extract outputs from **Label Studio** (`parse_labelstudio_export.py`

The goal of this project is to annotate **visual content posted by anti-Israel groups**.  
Labels include **emotional content, text presence, scene types, potential support for terrorism, stance, and emotional impact**.  

⚠️ **Important note on ethics:** This taxonomy is for **research purposes only**. Annotators should describe content **neutrally** and avoid amplifying harmful or extremist material.

---

## Installation

### Prerequisites
- **Python 3.8+**
- [Docker](https://docs.docker.com/get-docker/) (optional, alternative setup)
- A terminal / command line:
  - macOS: Terminal
  - Windows: PowerShell or Command Prompt
  - Linux: your shell (e.g., bash)

### Option 1: Install via pip
```bash
# Create a virtual environment
python3 -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows

# Install Label Studio
pip install label-studio

# Run Label Studio
label-studio
```
### Option 2: Install via Homebrew (macOS only)
```bash
brew tap humansignal/tap
brew install humansignal/tap/label-studio
label-studio
```

### Option 3: Run with Docker (Any OS)
```bash
docker pull heartexlabs/label-studio:latest
docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest
```


<div style="font-size: 0.2em; color: #555; margin-top: 2em;">
  <p>
    All materials in this repository were created by <a href="https://damieh1.github.io/">Daniel Miehling</a>, unless otherwise noted.
  </p>
  <p>
    Please contact <a href="mailto:damieh@iu.edu">damieh@iu.edu</a> for reuse permissions or collaboration inquiries.
  </p>
</div>
