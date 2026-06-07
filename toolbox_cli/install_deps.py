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

# Bilingual installer messages
_MSGS = {
    "en": {
        "verifying": "Verifying system dependencies...",
        "ok_installed": "already installed",
        "missing": "will be installed",
        "installing_n": "Installing missing dependencies ({n})...",
        "installing_pkg": "  -> Installing {pkg}... ",
        "done": "Done.",
        "error": "ERROR.",
        "err_install": "[ERROR] Failed to install package '{pkg}' globally.",
        "err_manual": "Please run 'pip install {pkg}' manually to diagnose.",
        "all_ok": "[OK] All dependencies are already satisfied.",
        "all_installed": "[OK] All dependencies successfully installed.",
        "reg_path": "[INFO] Registering path in your environment variables...",
        "path_added": "Successfully registered folder in PATH.",
        "path_exists": "Folder is already registered in PATH.",
        "ready_title": "TOOLBOX CLI IS READY TO BE USED",
        "instr_1": "1. Open a NEW terminal (CMD or PowerShell) to refresh PATH.",
        "instr_2": "2. Navigate to the directory containing your files.",
        "instr_3": "   Example: cd C:\\MyDocuments",
        "instr_4": "3. Type 'tb' and press Enter.",
        "note": "Toolbox CLI will automatically scan and process compatible files\n   in the folder where you execute the command.",
        "usage": "Usage instructions:",
        "note_label": "Note:",
    },
    "es": {
        "verifying": "Verificando dependencias del sistema...",
        "ok_installed": "ya instalado",
        "missing": "se instalará",
        "installing_n": "Instalando dependencias faltantes ({n})...",
        "installing_pkg": "  -> Instalando {pkg}... ",
        "done": "Listo.",
        "error": "ERROR.",
        "err_install": "[ERROR] No se pudo instalar el paquete '{pkg}' globalmente.",
        "err_manual": "Ejecuta 'pip install {pkg}' manualmente para diagnosticar.",
        "all_ok": "[OK] Todas las dependencias ya están satisfechas.",
        "all_installed": "[OK] Todas las dependencias fueron instaladas correctamente.",
        "reg_path": "[INFO] Registrando ruta en tus variables de entorno...",
        "path_added": "Ruta registrada en PATH exitosamente.",
        "path_exists": "La ruta ya está registrada en PATH.",
        "ready_title": "TOOLBOX CLI ESTÁ LISTO PARA USARSE",
        "instr_1": "1. Abre una NUEVA terminal (CMD o PowerShell) para refrescar el PATH.",
        "instr_2": "2. Navega al directorio que contiene tus archivos.",
        "instr_3": "   Ejemplo: cd C:\\MisDocumentos",
        "instr_4": "3. Escribe 'tb' y presiona Enter.",
        "note": "Toolbox CLI escaneará y procesará automáticamente los archivos\n   compatibles en la carpeta donde ejecutes el comando.",
        "usage": "Instrucciones de uso:",
        "note_label": "Nota:",
    }
}

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

def msg(key, lang, **kwargs):
    text = _MSGS.get(lang, _MSGS["en"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def register_path():
    """Register the install directory in the user's PATH (Windows only)."""
    if not sys.platform.startswith('win'):
        return
    target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             f"$p = [Environment]::GetEnvironmentVariable('PATH','User');"
             f"if(-not ($p -split ';' -contains '{target_dir}'))"
             f"{{ [Environment]::SetEnvironmentVariable('PATH',$p+';{target_dir}','User'); 'ADDED' }}"
             f"else{{ 'EXISTS' }}"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return "EXISTS"

def main():
    # ── Step 1: Language selection (FIRST, so all subsequent messages use it) ──
    print()
    print("----------------------------------------")
    print("Select interface language / Selecciona el idioma de la interfaz:")
    print("  1. English")
    print("  2. Español")
    print("----------------------------------------")

    cfg = load_config()
    current_lang = cfg.get("language", "en")
    lang_display = "English" if current_lang == "en" else "Español"

    try:
        choice = input(f"Enter choice / Ingresa tu opción (1-2) [Current: {lang_display}]: ").strip()
        if choice == "2":
            cfg["language"] = "es"
            lang = "es"
        elif choice == "1":
            cfg["language"] = "en"
            lang = "en"
        else:
            lang = current_lang
    except (KeyboardInterrupt, SystemExit):
        lang = current_lang

    cfg["language"] = lang
    save_config(cfg)
    lang_name = "ESPAÑOL" if lang == "es" else "ENGLISH"
    print(f"  -> {lang_name}")
    print("----------------------------------------")
    print()

    # ── Step 2: Dependency verification (in selected language) ──
    print(msg("verifying", lang))
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
            print(f"  [OK] {pip_name} ({msg('ok_installed', lang)})")
        else:
            print(f"  [--] {pip_name} ({msg('missing', lang)})")
            packages_to_install.append(pip_name)

    if packages_to_install:
        print("========================================")
        print(msg("installing_n", lang, n=len(packages_to_install)))

        # Silently upgrade pip first
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception:
            pass

        for pkg in packages_to_install:
            print(msg("installing_pkg", lang, pkg=pkg), end="", flush=True)
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                print(msg("done", lang))
            except subprocess.CalledProcessError:
                print(msg("error", lang))
                print(f"\n{msg('err_install', lang, pkg=pkg)}")
                print(msg("err_manual", lang, pkg=pkg))
                sys.exit(1)
        print("========================================")
        print(msg("all_installed", lang))
    else:
        print("========================================")
        print(msg("all_ok", lang))

    # ── Step 3: PATH registration (in selected language) ──
    print()
    print(msg("reg_path", lang))
    result = register_path()
    if result == "ADDED":
        print(msg("path_added", lang))
    else:
        print(msg("path_exists", lang))

    # ── Step 4: Success message (in selected language) ──
    print()
    print("+--------------------------------------------------------------------+")
    print(f"  * {msg('ready_title', lang)} *")
    print("+--------------------------------------------------------------------+")
    print()
    print(f"  {msg('usage', lang)}")
    print(f"    {msg('instr_1', lang)}")
    print(f"    {msg('instr_2', lang)}")
    print(f"    {msg('instr_3', lang)}")
    print(f"    {msg('instr_4', lang)}")
    print()
    print(f"  {msg('note_label', lang)}")
    print(f"    {msg('note', lang)}")
    print()
    print("======================================================================")

if __name__ == "__main__":
    main()
