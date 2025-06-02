import tkinter as tk
from tkinter import messagebox
import secrets
import string
import os
from typing import List
from colors import *


class FileSavingError(Exception):
    """Excepción personalizada para errores durante el guardado de archivos."""
    pass

# Función auxiliar para mezclar una lista de forma segura
def _secure_shuffle(lst: List[str]) -> None:
    """Mezcla una lista en su lugar utilizando secrets.randbelow para aleatoriedad criptográfica."""
    n = len(lst)
    for i in range(n - 1, 0, -1):
        # secrets.randbelow(k) genera un entero aleatorio en [0, k-1]
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]
DEFAULT_PASSWORD_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "kaospass_passwords.txt")

def generate_password_and_save(length: int = 12,
                               file_name: str = DEFAULT_PASSWORD_FILE,
                               min_lower: int = 1,
                               min_upper: int = 1,
                               min_digits: int = 3,
                               min_punctuation: int = 1) -> str:
    """
    Genera una contraseña aleatoria de la longitud dada que cumple con los requisitos
    de caracteres especificados (minúsculas, mayúsculas, dígitos, puntuación).
    Guarda la contraseña generada en la ruta de archivo dada, creando el directorio
    si no existe.

    Parámetros:
    - length (int): La longitud de la contraseña a generar. Por defecto 12.
    - file_name (str): La ruta del archivo para guardar la contraseña generada.
                       Por defecto "~/Desktop/kaospass_passwords.txt".
    - min_lower (int): Número mínimo de caracteres en minúscula. Por defecto 1.
    - min_upper (int): Número mínimo de caracteres en mayúscula. Por defecto 1.
    - min_digits (int): Número mínimo de dígitos. Por defecto 3.
    - min_punctuation (int): Número mínimo de signos de puntuación. Por defecto 1.

    Devuelve:
    str: La cadena de contraseña generada.

    Lanza:
    - ValueError: Si la longitud especificada es demasiado corta para cumplir
                  con los requisitos mínimos de caracteres.
    """
    lower_chars = string.ascii_lowercase
    upper_chars = string.ascii_uppercase
    digit_chars = string.digits
    punctuation_chars = string.punctuation  # Se añaden signos de puntuación
    
    # Alfabeto completo para rellenar los caracteres restantes
    all_chars = lower_chars + upper_chars + digit_chars + punctuation_chars

    # Verificar si la longitud es suficiente
    required_char_count = min_lower + min_upper + min_digits + min_punctuation
    if length < required_char_count:
        raise ValueError(
            f"La longitud de la contraseña ({length}) es demasiado corta. "
            f"Se requiere una longitud mínima de {required_char_count} para incluir "
            f"todos los tipos de caracteres especificados (minúsculas: {min_lower}, "
            f"mayúsculas: {min_upper}, dígitos: {min_digits}, puntuación: {min_punctuation})."
        )

    password_chars = []

    # 1. Asegurar el número mínimo de cada tipo de carácter
    for _ in range(min_lower):
        password_chars.append(secrets.choice(lower_chars))
    for _ in range(min_upper):
        password_chars.append(secrets.choice(upper_chars))
    for _ in range(min_digits):
        password_chars.append(secrets.choice(digit_chars))
    for _ in range(min_punctuation):
        password_chars.append(secrets.choice(punctuation_chars))

    # 2. Rellenar el resto de la contraseña con caracteres aleatorios del conjunto completo
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(all_chars))

    # 3. Mezclar la lista de caracteres de forma segura para evitar patrones predecibles
    _secure_shuffle(password_chars)
    password = "".join(password_chars)

    # 4. Guardar la contraseña en el archivo
    try:
        # Asegurar que el directorio de destino exista
        dir_path = os.path.dirname(file_name)
        if dir_path:  # Solo crear si hay una ruta de directorio (evita problemas con nombres de archivo sin ruta)
            os.makedirs(dir_path, exist_ok=True)
        
        with open(file_name, "a") as file:  # Se mantiene el modo 'append' (añadir)
            file.write(password + "\n")
        # La retroalimentación de éxito ahora la maneja la GUI
    except OSError as e:
        error_message = (
            f"Error al intentar guardar la contraseña en '{file_name}'.\n"
            f"Causa: {e.__class__.__name__} - {e}.\n"
            "Verifique que la ruta es válida y que tiene permisos de escritura."
        )
        raise FileSavingError(error_message) from e
    except Exception as e: # Captura genérica para otros errores inesperados durante el guardado
        raise FileSavingError(f"Un error inesperado ocurrió al guardar la contraseña: {e}") from e
            
    return password

def copy_to_clipboard(root_window: tk.Tk, text_to_copy: str, status_label: tk.Label):
    """Copia el texto dado al portapapeles y actualiza la etiqueta de estado."""
    try:
        text_to_copy = text_to_copy.strip()
        if not text_to_copy or text_to_copy == "Error al generar." or text_to_copy == "Error al guardar.":
            status_label.config(text="Nada válido para copiar.", fg=STATUS_WARNING_FG)
            return

        root_window.clipboard_clear()
        root_window.clipboard_append(text_to_copy)
        status_label.config(text="¡Contraseña copiada al portapapeles!", fg=STATUS_INFO_FG)
    except tk.TclError:
        status_label.config(text="Error al copiar (portapapeles no accesible).", fg=STATUS_ERROR_FG)
        messagebox.showerror("Error al Copiar", "No se pudo acceder al portapapeles.", parent=root_window)

def gui_handle_generate_password(root_window: tk.Tk, display_widget: tk.Text, status_label: tk.Label):
    """Maneja la generación de contraseña y la actualización de la GUI."""
    try:
        # Podríamos obtener parámetros (length, file_name, etc.) de campos de entrada en la GUI en el futuro.
        # Por ahora, usa los valores por defecto de generate_password_and_save.
        password = generate_password_and_save()
        
        display_widget.config(state=tk.NORMAL) # Habilitar para modificar
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, password)
        display_widget.config(state=tk.DISABLED) # Deshabilitar, solo lectura
        
        status_label.config(text=f"¡Contraseña generada y guardada!", fg=STATUS_SUCCESS_FG)
        # Podríamos añadir el nombre del archivo si generate_password_and_save lo devolviera
        # o si lo pasáramos explícitamente.
        # Ejemplo: status_label.config(text=f"Contraseña guardada en {DEFAULT_PASSWORD_FILE}", fg="green")
        
    except ValueError as ve:
        messagebox.showerror("Error de Configuración", str(ve), parent=root_window)
        status_label.config(text="Error de configuración al generar.", fg=STATUS_ERROR_FG)
        display_widget.config(state=tk.NORMAL)
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, "Error al generar.")
        display_widget.config(state=tk.DISABLED)
    except FileSavingError as fse:
        messagebox.showerror("Error al Guardar Archivo", str(fse), parent=root_window)
        status_label.config(text="Error al guardar el archivo.", fg=STATUS_ERROR_FG)
        # La contraseña pudo haberse generado, así que la mostramos si está disponible
        # (aunque no se haya guardado). Si 'password' no está definido, es un problema.
        # Por simplicidad, si hay error de guardado, mostramos mensaje de error en el display.
        display_widget.config(state=tk.NORMAL)
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, "Error al guardar.") # O mostrar la contraseña generada con advertencia
        display_widget.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error general: {str(e)}", parent=root_window)
        status_label.config(text="Error inesperado.", fg=STATUS_ERROR_FG)

if __name__ == "__main__":


    root = tk.Tk()
    root.title("Generador de Contraseñas Kaospass")
    root.geometry("400x200") # Ajustado para más espacio
    root.configure(bg=COLOR_PRIMARY_BG)

    frame = tk.Frame(root, bg=COLOR_PRIMARY_BG)
    frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

    password_label = tk.Label(frame, text="Contraseña Generada:", fg=COLOR_TEXT_FG, bg=COLOR_PRIMARY_BG)
    password_label.pack(pady=(0,2))

    password_display = tk.Text(frame, width=30, height=1,
                                relief=tk.SOLID, borderwidth=1,
                                bg=COLOR_TEXT_WIDGET_BG, fg=COLOR_TEXT_FG,
                                highlightbackground=COLOR_TEXT_WIDGET_BORDER, # Color del borde cuando no está enfocado
                                highlightcolor=COLOR_TEXT_WIDGET_BORDER,    # Color del borde cuando está enfocado (menos relevante si está DISABLED)
                                highlightthickness=1,
                                insertbackground=COLOR_TEXT_FG) # Color del cursor (si fuera editable)
    password_display.pack(pady=(0,10))
    password_display.config(state=tk.DISABLED) # Inicia deshabilitado (solo lectura)

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=5)

    status_label = tk.Label(frame, text="Listo.", font=("Arial", 9), fg=STATUS_READY_FG, bg=COLOR_PRIMARY_BG)
    status_label.pack(pady=(5,0))

    generate_button = tk.Button(button_frame, text="Generar Nueva Contraseña",
                                command=lambda: gui_handle_generate_password(root, password_display, status_label),
                                bg=COLOR_ACCENT, fg=COLOR_BUTTON_FG,
                                relief=tk.FLAT, activebackground="#005C99", activeforeground=COLOR_BUTTON_FG,
                                borderwidth=0, highlightthickness=0,
                                padx=10, pady=5)
    generate_button.pack(side=tk.LEFT, padx=5)

    copy_button = tk.Button(button_frame, text="Copiar al Portapapeles",
                            command=lambda: copy_to_clipboard(root, password_display.get("1.0", tk.END), status_label),
                            bg=COLOR_ACCENT, fg=COLOR_BUTTON_FG,
                            relief=tk.FLAT, activebackground="#005C99", activeforeground=COLOR_BUTTON_FG,
                            borderwidth=0, highlightthickness=0,
                            padx=10, pady=5)
    copy_button.pack(side=tk.LEFT, padx=5)

    button_frame.configure(bg=COLOR_PRIMARY_BG) # Asegurar que el frame de botones tenga el fondo correcto

    # Generar una contraseña inicial al cargar la GUI
    gui_handle_generate_password(root, password_display, status_label)

    root.mainloop()
