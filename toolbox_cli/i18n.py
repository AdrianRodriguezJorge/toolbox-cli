from .config import load_config

_TRANSLATIONS = {
    "en": {
        # General UI
        "menu_title": "⚙️ TOOLBOX CLI - FILE CONVERSION AND COMPRESSION ⚙️",
        "menu_subtitle": "Execution directory",
        "sys_diag": "System Diagnostics",
        "option": "Option",
        "tool_name": "Conversion Tool",
        "input_format": "Input Format",
        "output_format": "Output Format",
        "files_detected": "Files Detected",
        "exit_opt": "Exit",
        "invalid_opt": "Invalid option. Please try again.",
        "press_enter": "Presione Enter to return to main menu...",
        "success_title": "Success",
        "error_title": "Error",
        
        # Diagnostics
        "diag_ffmpeg": "🎬 FFmpeg",
        "diag_office": "💼 MS Word COM",
        "diag_libre": "💼 LibreOffice",
        "diag_python": "🐍 Python Libraries",
        "diag_ok": "OK",
        "diag_missing": "NOT DETECTED",
        "diag_missing_libs": "Missing packages",
        
        # Prompts and Lists
        "select_all": "[Convert ALL matching files]",
        "select_file_prompt": "Select an item to convert",
        "select_menu_prompt": "Select a menu option",
        "found_files": "Found {count} files matching {exts} for '{tool}'.",
        "converting_single": "Converting single file...",
        "converting_all": "Converting all matched files...",
        "summary_msg": "Successfully converted {success} files. Failed: {fail}.",
        
        # Tools Titles and Details
        "t_img_to_ico": "Image to ICO",
        "t_pdf_to_img": "PDF to PNG",
        "t_pdf_to_md": "PDF to Markdown",
        "t_ppt_to_md": "PowerPoint to Markdown",
        "t_docx_to_md": "Word to Markdown",
        "t_xls_to_csv": "Excel to CSV",
        "t_csv_to_xls": "CSV to Excel",
        "t_md_to_html": "Markdown to HTML",
        "t_img_conv": "Image Converter",
        "t_img_comp": "Compress Image",
        "t_vid_comp": "Compress Video (FFmpeg)",
        "t_docx_to_pdf": "Word to PDF",
        "t_pdf_to_docx": "PDF to Word",
        
        # Error & status messages
        "err_no_files": "No matching files found for this tool in the current directory.",
        "err_no_pywin32": "Error: 'pywin32' library is required for Microsoft Office COM conversions.",
        "err_com_init": "Failed to initialize Microsoft Office COM server: {e}",
        "err_general": "Error processing {file}: {e}",
        "status_converting": "Converting: {input} -> {output}...",
        "status_converted": "Converted successfully: {output}",
        "status_com_start": "Starting Microsoft Office COM application in background...",
        
        # Image specific
        "img_conv_prompt": "Select target output format (png/jpg/webp/bmp)",
        "img_comp_prompt": "Select compression mode (1: Lossless, 2: High compression, 3: Custom)",
        "img_quality_prompt": "Enter custom quality level (1-100)",
        
        # Video specific
        "vid_codec_prompt": "Select video codec (1: H.265 (Recommended, slower), 2: H.264 (Faster, compatible))",
        "vid_crf_prompt": "Select compression strength (1: Low (High quality), 2: Medium (Balanced), 3: High (Low quality))",
        "vid_err_ffmpeg": "Error: FFmpeg was not found in your system's PATH. Video compression requires FFmpeg."
    },
    "es": {
        # Interfaz General
        "menu_title": "⚙️ CAJA DE HERRAMIENTAS TOOLBOX CLI ⚙️",
        "menu_subtitle": "Directorio de ejecución",
        "sys_diag": "Diagnóstico del Sistema",
        "option": "Opción",
        "tool_name": "Herramienta de Conversión",
        "input_format": "Formato Entrada",
        "output_format": "Formato Salida",
        "files_detected": "Archivos Detectados",
        "exit_opt": "Salir",
        "invalid_opt": "Opción inválida. Intente de nuevo.",
        "press_enter": "Presione Enter para regresar al menú principal...",
        "success_title": "Éxito",
        "error_title": "Error",
        
        # Diagnósticos
        "diag_ffmpeg": "🎬 FFmpeg",
        "diag_office": "💼 MS Word COM",
        "diag_libre": "💼 LibreOffice",
        "diag_python": "🐍 Librerías Python",
        "diag_ok": "OK",
        "diag_missing": "NO DETECTADO",
        "diag_missing_libs": "Faltan paquetes",
        
        # Prompts y Listas
        "select_all": "[Convertir TODOS los archivos coincidentes]",
        "select_file_prompt": "Selecciona un elemento para convertir",
        "select_menu_prompt": "Selecciona una opción del menú",
        "found_files": "Encontrados {count} archivos que coinciden con {exts} para '{tool}'.",
        "converting_single": "Convirtiendo archivo individual...",
        "converting_all": "Convirtiendo todos los archivos coincidentes...",
        "summary_msg": "Convertidos con éxito {success} archivos. Fallidos: {fail}.",
        
        # Títulos y Detalles de Herramientas
        "t_img_to_ico": "Imagen a ICO",
        "t_pdf_to_img": "PDF a PNG",
        "t_pdf_to_md": "PDF a Markdown",
        "t_ppt_to_md": "PowerPoint a Markdown",
        "t_docx_to_md": "Word a Markdown",
        "t_xls_to_csv": "Excel a CSV",
        "t_csv_to_xls": "CSV a Excel",
        "t_md_to_html": "Markdown a HTML",
        "t_img_conv": "Conversor de Imagen",
        "t_img_comp": "Comprimir Imagen",
        "t_vid_comp": "Comprimir Video (FFmpeg)",
        "t_docx_to_pdf": "Word a PDF",
        "t_pdf_to_docx": "PDF a Word",
        
        # Mensajes de error y estado
        "err_no_files": "No se encontraron archivos compatibles para esta herramienta en el directorio actual.",
        "err_no_pywin32": "Error: Se requiere la librería 'pywin32' para realizar conversiones mediante Office COM.",
        "err_com_init": "No se pudo iniciar el servidor Microsoft Office COM: {e}",
        "err_general": "Error al procesar {file}: {e}",
        "status_converting": "Convirtiendo: {input} -> {output}...",
        "status_converted": "Convertido exitosamente: {output}",
        "status_com_start": "Iniciando aplicación Microsoft Office COM en segundo plano...",
        
        # Específico de Imágenes
        "img_conv_prompt": "Selecciona el formato de salida objetivo (png/jpg/webp/bmp)",
        "img_comp_prompt": "Selecciona el modo de compresión (1: Sin pérdida, 2: Alta compresión, 3: Personalizado)",
        "img_quality_prompt": "Ingresa el nivel de calidad personalizado (1-100)",
        
        # Específico de Videos
        "vid_codec_prompt": "Selecciona el códec de video (1: H.265 (Recomendado, lento), 2: H.264 (Rápido, compatible))",
        "vid_crf_prompt": "Selecciona la fuerza de compresión (1: Baja (Alta calidad), 2: Media (Equilibrado), 3: Alta (Baja calidad))",
        "vid_err_ffmpeg": "Error: FFmpeg no fue encontrado en el PATH de tu sistema. La compresión de video requiere FFmpeg."
    }
}

def get_text(key, **kwargs):
    """Retrieve translated string with optional interpolation."""
    cfg = load_config()
    lang = cfg.get("language", "en")
    if lang not in _TRANSLATIONS:
        lang = "en"
    text = _TRANSLATIONS[lang].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            pass
    return text
