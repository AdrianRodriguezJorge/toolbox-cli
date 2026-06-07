import os
import sys
import subprocess
import importlib.util
import json

# Home configuration path
CONFIG_FILE = os.path.expanduser("~/.toolbox_cli.json")

# Required dependencies: (pip_name, import_name)
REQUIRED_PACKAGES = [
    ("rich", "rich"),
    ("Pillow", "PIL"),
    ("pymupdf", "fitz"),
    ("python-docx", "docx"),
    ("python-pptx", "pptx"),
    ("pandas", "pandas"),
    ("openpyxl", "openpyxl"),
    ("markdown", "markdown")
]

if sys.platform.startswith('win'):
    REQUIRED_PACKAGES.append(("pywin32", "win32com"))

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"language": "en"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

def main():
    print("Verifying system dependencies...")
    print("========================================")
    
    packages_to_install = []
    
    for pip_name, import_name in REQUIRED_PACKAGES:
        installed = False
        try:
            if import_name == "win32com":
                import win32com
                installed = True
            else:
                spec = importlib.util.find_spec(import_name)
                if spec is not None:
                    installed = True
        except Exception:
            pass
            
        if installed:
            print(f"  [OK] {pip_name} (already installed)")
        else:
            print(f"  [MISSING] {pip_name} (will be installed)")
            packages_to_install.append(pip_name)

    if packages_to_install:
        print("========================================")
        print(f"Installing missing dependencies ({len(packages_to_install)})...")
        
        # Silently upgrade pip first
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception:
            pass

        for pkg in packages_to_install:
            print(f"  -> Installing {pkg}... ", end="", flush=True)
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print("Done.")
            except subprocess.CalledProcessError:
                print("ERROR.")
                print(f"\n[ERROR] Failed to install package '{pkg}' globally.")
                print(f"Please run 'pip install {pkg}' manually to diagnose.")
                sys.exit(1)
        print("========================================")
        print("[OK] All dependencies successfully installed.")
    else:
        print("========================================")
        print("[OK] All dependencies are already satisfied.")

    # Configure interface language selection
    print("\n----------------------------------------")
    print("Select interface language / Selecciona el idioma de la interfaz:")
    print("  1. English")
    print("  2. Español")
    print("----------------------------------------")
    
    cfg = load_config()
    current_lang = cfg.get("language", "en")
    lang_display = "English" if current_lang == "en" else "Español"
    
    try:
        choice = input(f"Enter choice / Ingresa tu opcion (1-2) [Current: {lang_display}]: ").strip()
        if choice == "2":
            cfg["language"] = "es"
            print("Language configured: ESPAÑOL")
        elif choice == "1":
            cfg["language"] = "en"
            print("Language configured: ENGLISH")
        else:
            # Keep existing or default to English
            if "language" not in cfg:
                cfg["language"] = "en"
            print(f"Keeping current configuration: {lang_display.upper()}")
    except (KeyboardInterrupt, SystemExit):
        if "language" not in cfg:
            cfg["language"] = "en"
            
    save_config(cfg)
    print("----------------------------------------")

if __name__ == "__main__":
    main()
