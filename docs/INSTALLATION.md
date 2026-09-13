# Installation Instructions

## Requirements

- Python 3.10 or newer
- Git

## 1. Clone the repository

```bash
git clone https://github.com/ShanmukhJonnalagadda/Personal-sleep-recovery-privacy.git
cd Personal-sleep-recovery-privacy
```

Replace the URL if you choose a different repository name.

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Run the demo

```bash
streamlit run app.py
```

Open the local address displayed by Streamlit, normally `http://localhost:8501`.

## 6. Regenerate synthetic data (optional)

```bash
python scripts/generate_synthetic_data.py
```

The script uses a fixed random seed, so it produces reproducible demo data.

## 7. Regenerate the architecture image (optional)

```bash
python scripts/generate_architecture_diagram.py
```

## Environment variables

The sanitized demo does not require credentials. `.env.example` documents the variable names that a private production implementation may use. If you develop your own authenticated integration, copy it to `.env`, add the real values locally, and keep `.env` out of version control.

## Troubleshooting

Run `python scripts/check_demo.py` to validate the synthetic dataset and exercise app startup and all three date filters. This package was checked with Python 3.12, Streamlit 1.63.0, Pandas 2.2.3, NumPy 2.3.5, Plotly 6.9.0, and Pillow 12.3.0. Other allowed dependency versions have not all been tested.

The README lists private-project capabilities separately from the smaller public demo. There is no production OAuth handler, database schema, or synchronization workflow to install from this package.

- Run commands from the repository root.
- Confirm that the virtual environment is active before installing packages.
- If port 8501 is occupied, use `streamlit run app.py --server.port 8502`.
- If the data file is missing, regenerate it using the command above.
