import os
import sys
import json
import shutil
import subprocess

# Config path
CONFIG_FILE = os.path.expanduser("~/.toolbox_cli.json")

# Localized messages (re-using installer style)
_MSGS = {
    "en": {
        "confirm": "Are you sure you want to uninstall Toolbox CLI? (Y/N): ",
        "cancelled": "Uninstallation cancelled.",
        "removing_path": "Removing Toolbox CLI from PATH...",
        "path_updated": "PATH variable updated successfully.",
        "path_not_found": "Installation folder not found in PATH.",
        "cleaning": "Cleaning up configuration files...",
        "config_removed": "Configuration removed:",
        "config_not_found": "No configuration files found.",
        "complete": "Uninstallation complete.",
        "error": "An error occurred during uninstallation.",
    },
    "es": {
        "confirm": "¿Estás seguro de que deseas desinstalar Toolbox CLI? (S/N): ",
        "cancelled": "Desinstalacion cancelada.",
        "removing_path": "Eliminando Toolbox CLI del PATH...",
        "path_updated": "Variable PATH actualizada correctamente.",
        "path_not_found": "Carpeta de instalacion no encontrada en PATH.",
        "cleaning": "Limpiando archivos de configuracion...",
        "config_removed": "Configuracion eliminada:",
        "config_not_found": "No se encontraron archivos de configuracion.",
        "complete": "Desinstalacion completada.",
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

    try:
        choice = input(msg("confirm", lang)).strip()
    except (KeyboardInterrupt, EOFError):
        print(msg("cancelled", lang))
        sys.exit(0)

    if lang == "es":
        if choice.upper() != "S":
            print(msg("cancelled", lang))
            sys.exit(0)
    else:
        if choice.upper() != "Y":
            print(msg("cancelled", lang))
            sys.exit(0)

    print()
    print(msg("removing_path", lang))
    remove_path(script_dir, lang)
    print()
    print(msg("cleaning", lang))
    remove_configs(lang)
    print()
    print(msg("complete", lang))


if __name__ == "__main__":
    main()
