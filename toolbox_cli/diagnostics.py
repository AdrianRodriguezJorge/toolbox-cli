import sys
import subprocess
import importlib.util
from .base import HAS_RICH

def check_system_dependencies():
    """
    Check availability of external tools and python libraries in real time.
    """
    ffmpeg_ok = False
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith('win') else 0
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=creationflags)
        ffmpeg_ok = True
    except Exception:
        pass
        
    office_ok = False
    if sys.platform.startswith('win'):
        try:
            import win32com.client
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Word.Application")
            winreg.CloseKey(key)
            office_ok = True
        except Exception:
            pass
    else:
        try:
            subprocess.run(["libreoffice", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            office_ok = True
        except Exception:
            pass
            
    # Check required python packages
    python_deps = {
        "Pillow": False,
        "PyMuPDF": False,
        "python-docx": False,
        "python-pptx": False,
        "pandas": False,
        "openpyxl": False,
        "markdown": False
    }
    
    try:
        import PIL
        python_deps["Pillow"] = True
    except ImportError: pass
    
    try:
        import fitz
        python_deps["PyMuPDF"] = True
    except ImportError: pass
    
    try:
        import docx
        python_deps["python-docx"] = True
    except ImportError: pass
    
    try:
        import pptx
        python_deps["python-pptx"] = True
    except ImportError: pass
    
    try:
        import pandas
        python_deps["pandas"] = True
    except ImportError: pass
    
    try:
        import openpyxl
        python_deps["openpyxl"] = True
    except ImportError: pass
    
    try:
        import markdown
        python_deps["markdown"] = True
    except ImportError: pass
    
    return ffmpeg_ok, office_ok, python_deps
