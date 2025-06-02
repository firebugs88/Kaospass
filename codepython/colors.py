# --- Definición de Colores para la UI ---
COLOR_PRIMARY_BG = "#2E3B4E"       # Gris oscuro azulado para el fondo principal
COLOR_SECONDARY_BG = "#3A4759"     # Gris un poco más claro para frames
COLOR_TEXT_FG = "#F0F0F0"          # Blanco/Gris muy claro para texto general
COLOR_ACCENT = "#007ACC"           # Azul para botones y acentos
COLOR_BUTTON_FG = "#FFFFFF"        # Blanco para texto de botones
COLOR_TEXT_WIDGET_BG = "#252526"   # Fondo para el campo de texto (similar a VSCode)
COLOR_TEXT_WIDGET_BORDER = COLOR_ACCENT # Borde del campo de texto

STATUS_READY_FG = "#B0B0B0"
STATUS_SUCCESS_FG = "#77DD77"      # Verde pastel
STATUS_INFO_FG = "#89CFF0"         # Azul bebé
STATUS_WARNING_FG = "#FFBF00"      # Ámbar
STATUS_ERROR_FG = "#FF6961"        # Rojo pastel
# --- Fin Definición de Colores ---

# Puedes dejar el bloque if __name__ == "__main__": si quieres
# ejecutar alguna prueba específica de este archivo, pero las
# definiciones de las variables deben estar fuera para que se puedan importar.
if __name__ == "__main__":
    # Por ejemplo, podrías imprimir los colores para verificar
    print(f"COLOR_PRIMARY_BG: {COLOR_PRIMARY_BG}")
    print("El archivo colors.py se ejecutó directamente.")
