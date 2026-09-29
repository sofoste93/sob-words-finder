<div align="center">
  <img src="static/brand-mark.svg" width="92" alt="SOB Words Finder orbit logo">
  <h1>SOB Words Finder</h1>
  <p><strong>Find the signal inside the noise.</strong></p>
  <p>A private local document scanner wrapped in a bilingual mission-control interface.</p>

  [![Release](https://img.shields.io/github/v/release/sofoste93/sob-words-finder?style=flat-square&color=c8ff63)](https://github.com/sofoste93/sob-words-finder/releases/latest)
  [![Build](https://img.shields.io/github/actions/workflow/status/sofoste93/sob-words-finder/release.yml?style=flat-square&label=release)](https://github.com/sofoste93/sob-words-finder/actions)
  [![License](https://img.shields.io/github/license/sofoste93/sob-words-finder?style=flat-square)](LICENSE)
</div>

## Mission overview

SOB Words Finder searches a word or phrase across a document and returns useful context instead of a bare index. Each hit includes its line, page, or paragraph, the surrounding text, and the number of occurrences at that location.

- **Seven formats:** TXT, Markdown, CSV, LOG, JSON, PDF, and DOCX
- **Private processing:** documents stay in memory and are never sent to a remote service
- **Precise scanning:** optional case-sensitive and whole-word matching
- **Useful reports:** contextual excerpts, occurrence totals, and scanned-location counts
- **Bilingual flight deck:** complete English and French interface
- **Accessible motion:** responsive layout and a persistent reduced-motion setting
- **Portable release:** standalone Windows and Linux builds open in your default browser

## Launch the app

### Standalone release

1. Open the [latest release](https://github.com/sofoste93/sob-words-finder/releases/latest).
2. Download the application for Windows or Linux.
3. Launch it. Mission Control opens at a private local address in your default browser.

The executable starts a local server bound to `127.0.0.1`. It does not expose the app to your network.

### Run from source

Python 3.10 or newer is required.

```bash
git clone https://github.com/sofoste93/sob-words-finder.git
cd sob-words-finder
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# macOS / Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the development server:

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Search behavior

Text-like files are scanned line by line. PDFs are scanned page by page, and DOCX files paragraph by paragraph. Matching is case-insensitive by default. Settings are stored only in browser local storage.

Uploads are limited to 16 MB. The endpoint reads each upload directly into memory; the ignored `uploads/` path exists only to guard against files created by older versions.

## Development

Install the development toolchain and run the tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Build the standalone application on Windows:

```powershell
.\build.ps1
```

The executable is written to `dist/SOB-Words-Finder.exe`. Pushing a `v*` tag runs the release workflow, tests the project, builds Windows and Linux applications, and attaches them to a GitHub release.

## Architecture

```text
app.py                  Flask app and JSON search API
launcher.py             standalone desktop entry point
utils/finder.py         extraction and search engine
templates/index.html    bilingual mission-control interface
static/                 self-contained visual system and client logic
data/                   onboard sample mission log
tests/                  backend and search tests
```

## Français

SOB Words Finder analyse localement vos documents et affiche chaque correspondance avec son contexte et sa position. Aucun fichier n'est envoyé vers un service distant ou conservé après la requête. Téléchargez simplement l'application depuis la [dernière release](https://github.com/sofoste93/sob-words-finder/releases/latest), lancez-la, puis passez l'interface en français depuis **Réglages**.

## Security and contributions

Do not use the development server on a public interface. Report security issues privately to the repository owner. Bug reports and focused pull requests are welcome; please include a test when changing search behavior.

Released under the [Apache License 2.0](LICENSE).
