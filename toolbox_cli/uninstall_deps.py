import os
import sys
import json
import shutil
import subprocess

# Config path
CONFIG_FILE = os.path.expanduser("~/.toolbox_cli.json")

# Separator and formatting constants
SEPARATOR_MAIN = "=" * 70
SEPARATOR_SUB = "=" * 66

# Localized messages (re-using installer style)
_MSGS = {
    "en": {
        "title": "TOOLBOX CLI - UNINSTALLATION",
        "intro_msg": "This script will remove Toolbox CLI from your system.",
        "install_dir": "Installation directory:",
        "confirm": "Are you sure you want to uninstall Toolbox CLI? (Y/N): ",
        "cancelled": "Uninstallation cancelled.",
        "step_removing_path": "Step 1: Removing from system PATH",
        "removing_path": "  Removing Toolbox CLI from PATH...",
        "path_updated": "  ✓ PATH variable updated successfully.",
        "path_not_found": "  ✗ Installation folder not found in PATH.",
        "step_cleaning": "Step 2: Cleaning up configuration files",
        "cleaning": "  Cleaning up configuration files...",
        "config_removed": "  ✓ Configuration removed:",
        "config_not_found": "  ✗ No configuration files found.",
        "complete_title": "UNINSTALLATION COMPLETE!",
        "complete": "✓ Toolbox CLI has been removed from your system.",
        "post_steps": "To finish the process:",
        "step1": "  1. Close all terminal windows",
        "step2": "  2. Open a NEW terminal window",
        "step3": "  3. Verify with: tb (should show 'command not recognized')",
        "error": "An error occurred during uninstallation.",
    },
    "es": {
        "title": "TOOLBOX CLI - DESINSTALACIÓN",
        "intro_msg": "Este script eliminará Toolbox CLI de tu sistema.",
        "install_dir": "Directorio de instalación:",
        "confirm": "¿Estás seguro de que deseas desinstalar Toolbox CLI? (S/N): ",
        "cancelled": "Desinstalacion cancelada.",
        "step_removing_path": "Paso 1: Eliminando del PATH del sistema",
        "removing_path": "  Eliminando Toolbox CLI del PATH...",
        "path_updated": "  ✓ Variable PATH actualizada correctamente.",
        "path_not_found": "  ✗ Carpeta de instalacion no encontrada en PATH.",
        "step_cleaning": "Paso 2: Limpiando archivos de configuración",
        "cleaning": "  Limpiando archivos de configuracion...",
        "config_removed": "  ✓ Configuracion eliminada:",
        "config_not_found": "  ✗ No se encontraron archivos de configuracion.",
        "complete_title": "¡DESINSTALACIÓN COMPLETADA!",
        "complete": "✓ Toolbox CLI ha sido eliminado de tu sistema.",
        "post_steps": "Para finalizar el proceso:",
        "step1": "  1. Cierra todas las ventanas de terminal",
        "step2": "  2. Abre una NUEVA ventana de terminal",
        "step3": "  3. Verifica con: tb (debería mostrar 'comando no reconocido')",
        "error": "Ocurrio un error durante la desinstalacion.",
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


def msg(key, lang):
    return _MSGS.get(lang, _MSGS["en"]).get(key, key)


def remove_path(target_dir, lang):
    # Use PowerShell like the batch script to update the user PATH safely
    try:
        safe_target = target_dir.replace("'", "'" )
        ps_cmd = (
            f"$path = [Environment]::GetEnvironmentVariable('PATH','User');"
            f"if ($path -like '*{target_dir}*') {{ $newPath = $path -replace [regex]::Escape('{target_dir}') + ';?', ''; [Environment]::SetEnvironmentVariable('PATH',$newPath,'User'); Write-Host('UPDATED') }} else {{ Write-Host('NOTFOUND') }}"
        )
        result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
        out = (result.stdout or "").strip()
        if "UPDATED" in out:
            print(msg("path_updated", lang))
            return True
        else:
            print(msg("path_not_found", lang))
            return False
    except Exception:
        print(msg("error", lang))
        return False


def remove_configs(lang):
    removed_any = False
    appdata_dir = os.environ.get("APPDATA")
    if appdata_dir:
        cfg_folder = os.path.join(appdata_dir, "toolbox-cli")
        if os.path.exists(cfg_folder):
            try:
                shutil.rmtree(cfg_folder)
                print(msg("config_removed", lang), cfg_folder)
                removed_any = True
            except Exception:
                pass

    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
            print(msg("config_removed", lang), CONFIG_FILE)
            removed_any = True
        except Exception:
            pass

    if not removed_any:
        print(msg("config_not_found", lang))


def main():
    cfg = load_config()
    lang = cfg.get("language", "en")

    # Determine install directory (parent of the package folder)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DISPLAY HEADER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print()
    print(SEPARATOR_MAIN)
    center_text = msg("title", lang)
    padding = (len(SEPARATOR_MAIN) - len(center_text)) // 2
    print(" " * padding + center_text)
    print(SEPARATOR_MAIN)
    print()

    # Display introduction and installation directory
    print(msg("intro_msg", lang))
    print()
    print(f"{msg('install_dir', lang)}")
    print(f"  {script_dir}")
    print()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CONFIRMATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    try:
        choice = input(msg("confirm", lang)).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        print(msg("cancelled", lang))
        sys.exit(0)

    if lang == "es":
        if choice.upper() != "S":
            print()
            print(msg("cancelled", lang))
            sys.exit(0)
    else:
        if choice.upper() != "Y":
            print()
            print(msg("cancelled", lang))
            sys.exit(0)

    print()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 1: REMOVE FROM PATH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(msg("step_removing_path", lang))
    print("-" * 66)
    print(msg("removing_path", lang))
    remove_path(script_dir, lang)
    print()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 2: CLEAN UP CONFIGURATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(msg("step_cleaning", lang))
    print("-" * 66)
    print(msg("cleaning", lang))
    remove_configs(lang)
    print()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # COMPLETION MESSAGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(SEPARATOR_MAIN)
    center_text = msg("complete_title", lang)
    padding = (len(SEPARATOR_MAIN) - len(center_text)) // 2
    print(" " * padding + center_text)
    print(SEPARATOR_MAIN)
    print()
    print(msg("complete", lang))
    print()
    print(msg("post_steps", lang))
    print(msg("step1", lang))
    print(msg("step2", lang))
    print(msg("step3", lang))
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
