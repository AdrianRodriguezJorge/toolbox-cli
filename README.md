# 🛠️ Toolbox CLI (`tb`)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Offline Ready](https://img.shields.io/badge/Offline-100%25-green.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](#)

**Toolbox CLI** is a powerful file conversion and compression toolbox written in Python. It is designed to automate the conversion and optimization of documents, spreadsheets, images, and videos locally, quickly, and privately.

Unlike traditional online web converters, **Toolbox CLI** processes all files locally on your machine. No data is ever uploaded to external servers, guaranteeing absolute confidentiality for your sensitive information.

---

## 🚀 Quick Start & Global Installation

Follow these steps to install **Toolbox CLI** globally on your system:

### 1. Clone the Repository
Open a terminal and clone the repository into your preferred tools directory (e.g., `C:\Program Files\toolbox-cli` or a custom tools folder in your user path):
```bash
git clone https://github.com/AdrianRodriguezJorge/toolbox-cli.git
```

### 2. Run the Installer
Navigate to the cloned directory and run the installer script:
```cmd
cd toolbox-cli
install.bat
```

The installer will automatically:
- Install and upgrade all required Python dependencies (`requirements.txt`) silently in your global environment.
- Register the installation folder in your User `PATH` environment variable.
- Prompt you to select your preferred interface language (English or Spanish).

### 3. Start Using It
Open a **NEW** terminal window (CMD or PowerShell) in any folder containing files you want to convert, type the following command, and press Enter:
```cmd
tb
```


---

## 📂 Repository Directory Structure

Here is a quick overview of the files in the repository:

```text
toolbox-cli/
├── toolbox_cli/            # Main package containing all source code and helper scripts
│   ├── base.py             # Console rendering tools, file utility helpers, and BaseConverter
│   ├── config.py           # Language config file manager (JSON local storage)
│   ├── diagnostics.py      # Real-time checks for FFmpeg, MS Office COM, and Python packages
│   ├── i18n.py             # Dual-language translations (English & Spanish)
│   ├── install_deps.py     # Silent Python packages installer
│   ├── requirements.txt    # Python requirements manifest
│   ├── tools.py            # Implementation of the 13 converter strategies
│   └── toolbox.py          # Main CLI console runner interface
├── install.bat             # Double-click script to install dependencies and register PATH
├── tb.cmd                  # Global CMD/PowerShell launcher alias (command 'tb')
├── LICENSE                 # Open-source MIT License terms
└── README.md               # User guide and documentation (this file)
```

---

## ✨ Key Features

* **🖥️ Interactive Console Interface**: A premium, responsive visual CLI menu built using the `rich` library.
* **📊 Live System Diagnostics**: Upon startup, a dynamic dashboard scans and reports the availability of external dependencies (such as FFmpeg and Microsoft Office COM) to let you know which tools are available.
* **🔒 Microsoft Office COM Isolation**: Word (`.docx`) and PowerPoint (`.pptx`) conversions run in an isolated background COM layer. You can convert files without interfering with or closing other active Office documents you are currently working on.
* **🛡️ Lockfile & Temp File Protection**: Automatically ignores OS and Office temporary/lock files (e.g., files starting with `~$`, `._`, `.tmp`, or `.~lock.`), preventing read errors.
* **📂 Smart Collision Resolution**: Output files will never overwrite existing files. If a filename collision is detected, the script automatically appends an incremental numeric suffix (e.g., `document_1.pdf`).
* **🌐 Offline by Design**: Requires no internet connection to run, making it ideal for highly secure corporate environments and air-gapped systems.

---

## 🛠️ Supported Tools & Formats

| # | Tool Name | Input Formats | Output Format | Key Features |
|---|-----------|---------------|---------------|--------------|
| **1** | **Word to PDF** | `.docx`, `.doc` | `.pdf` | Native Microsoft Office layout conversion. |
| **2** | **PDF to Word** | `.pdf` | `.docx` | Re-flowable layout construction using native MS Word COM. |
| **3** | **Word to Markdown** | `.docx`, `.doc` | `.md` | Paragraph styles and tables extraction to clean Markdown syntax. |
| **4** | **PowerPoint to Markdown** | `.pptx`, `.ppt` | `.md` | Slide text structure mapping (supports modern and legacy formats). |
| **5** | **PDF to Markdown** | `.pdf` | `.md` | Document structure heuristics preservation (headings, lists). |
| **6** | **Markdown to HTML** | `.md` | `.html` | Generates a premium responsive page with auto dark-mode, copy button, and SEO tags. |
| **7** | **Excel to CSV** | `.xlsx`, `.xls` | `.csv` (UTF-8) | Exports every worksheet in a workbook as an independent CSV file. |
| **8** | **CSV to Excel** | `.csv` | `.xlsx` | Compiles raw structured CSVs into a styled workbook. |
| **9** | **Image Converter** | `.png`, `.jpg`, `.webp`, `.bmp` | Multiple choices | Batch or single image format transposition. |
| **10**| **Image to ICO** | `.png`, `.jpg`, `.jpeg`, `.svg` | `.ico` (16px to 256px) | Smart square padding resizing to prevent image distortion. |
| **11**| **PDF to PNG** | `.pdf` | `.png` | High-fidelity individual page extraction at **300 DPI**. |
| **12**| **Image Compression** | `.png`, `.jpg`, `.webp` | Match Input | Space-saving adaptive compression (lossy and lossless modes). |
| **13**| **Video Compression** | `.mp4`, `.mkv`, `.avi`, `.mov`... | `.mp4` (H.264 / H.265) | Quality-targeted local compression using FFmpeg. |

---

## ⚙️ System Requirements

To leverage the full capability of all tools:
1. **Microsoft Office** (Installed locally on Windows) is required for native Word and PowerPoint conversions.
2. **FFmpeg** (Installed and added to your system's PATH) is required for video compression. Get it from [ffmpeg.org](https://ffmpeg.org/).

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
