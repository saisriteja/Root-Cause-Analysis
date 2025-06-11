# Root Cause Analysis Project

## Project Overview
This project provides tools for Root Cause Analysis (RCA) and Corrective/Preventive Actions (CAPA) using AI-powered analysis. It includes both command-line and web interface versions of the tools.

## Features
- Root Cause Analysis using Fishbone (Ishikawa) method
- Corrective and Preventive Actions (CAPA) generation
- Image-based safety checklist generation
- Web interface for easy interaction
- Command-line tools for programmatic usage

## Prerequisites
- Python 3.8 or higher
- Ollama installed and running
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone 
cd Root-Cause-Analysis
```

2. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start Ollama service:
```bash
ollama serve
```

5. Pull the required model:
```bash
ollama pull llama2
```

## Usage

### Web Interface

1. Start the RCA-CAPA Analysis Tool:
```bash
streamlit run rca_capa_app.py
```
- Open your browser at http://localhost:8501
- Enter the situation to analyze
- Click "Run RCA-CAPA Analysis" to get results

2. Start the Safety Checklist Tool:
```bash
streamlit run checklist_app.py
```
- Open your browser at http://localhost:8501
- Upload an image for analysis
- View the generated safety checklist

### Command Line Interface

1. Run RCA-CAPA Analysis:
```bash
python rca_capa_main.py
```
- Edit the situation in the script to analyze different scenarios
- Results will be displayed in JSON format

2. Run Safety Checklist Generation:
```bash
python checklist_main.py
```
- Place images in the `sample_images` directory
- Edit the image path in the script
- Results will be displayed in the console

## Project Structure

```
curl -fsSL https://ollama.com/install.sh | sh
```

run the ollama 3.2 models in the terminal
```
ollama run llama3.2
```