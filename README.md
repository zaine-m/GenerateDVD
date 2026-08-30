# GenerateDVD

Generate a DVD using [DVDStyler](https://www.dvdstyler.org/) from a collection of YouTube videos.

The program downloads the selected YouTube videos, processes the required media, and generates a DVDStyler project that can be used to create a playable DVD.

## Requirements

* Python 3.10 or newer
* [DVDStyler](https://www.dvdstyler.org/)
* [Ollama](https://ollama.com/) (if AI-assisted features are enabled)
* A working internet connection for downloading YouTube videos

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/zaine-m/GenerateDVD
cd GenerateDVD
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

**Linux:**

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux:**

```bash
source .venv/bin/activate
```

### 4. Install GenerateDVD

```powershell
pip install -e .
```

This installs the project and its Python dependencies in editable mode.

## Running

After installation, run:

```powershell
generateDVD
```

Alternatively, you can run the module directly:

```powershell
python -m src.main
```

## Configuration

Configuration options will be shown on a pop-up screen when run

## Project Structure

```text
GenerateDVD/
├── src/
│   ├── main.py
│   ├── app.py
│   ├── createImages.py
│   ├── download.py
│   ├── dvd.py
│   ├── scrapChannel.py
│   └── shorten.py
├── Roboto/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Dependencies

The project uses:

* **yt-dlp** — downloading YouTube videos
* **Ollama** — AI functionality
* **Pillow** — image processing
* **setuptools** — Python package/build management

## Development

Because the project is installed with:

```powershell
pip install -e .
```

changes to the source code are immediately available without reinstalling the package.

To run the project during development:

```powershell
generatedvd
```

---

This project is currently under development.
