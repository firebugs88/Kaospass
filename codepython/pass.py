# -*- coding: utf-8 -*-
import tkinter as tk
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

def generate_password_and_save(length: int = 10,
                               file_name: str = DEFAULT_PASSWORD_FILE,
                               min_lower: int = 4,
                               min_upper: int = 1,
                               min_digits: int = 3,
                               min_punctuation: int = 1) -> str:
    
    char_types = {
        string.ascii_lowercase: min_lower,
        string.ascii_uppercase: min_upper,
        string.digits: min_digits,
        string.punctuation: min_punctuation
    }
    # Verificar si la longitud es suficiente
    required_char_count = sum(char_types.values())
    if length < required_char_count:
        raise ValueError(f"La longitud de la contraseña ({length}) es demasiado corta.")

    password_chars = [secrets.choice(chars) for chars, count in char_types.items() for _ in range(count)]
    remaining_length = length - len(password_chars)
    all_chars = ''.join(char_types.keys())
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    _secure_shuffle(password_chars)
    password = ''.join(password_chars)

    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "a") as file:
            file.write(password + "\n")
    except OSError as e:
        raise FileSavingError(f"Error al guardar la contraseña: {e}") from e

    return password

def update_display_widget(widget: tk.Text, text: str, state: str = tk.DISABLED):
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, text)
    widget.config(state=state)

def update_status_label(label: tk.Label, text: str, color: str):
    label.config(text=text, fg=color)

class NotificationBanner:
    def __init__(self, parent):
        self.parent = parent
        self.notification_frame = None
        self.notification_label = None
        self.hide_timer = None
    
    def show_notification(self, message: str, notification_type: str = "info", duration: int = 3000):
        if self.notification_frame:
            self.hide_notification()
        
        color_map = {
            "success": STATUS_SUCCESS_FG,
            "error": STATUS_ERROR_FG,
            "warning": STATUS_WARNING_FG,
            "info": STATUS_INFO_FG
        }
        
        bg_color_map = {
            "success": "#1e3a1e",
            "error": "#3a1e1e",
            "warning": "#3a2e1e",
            "info": "#1e2e3a"
        }
        
        text_color = color_map.get(notification_type, STATUS_INFO_FG)
        bg_color = bg_color_map.get(notification_type, "#1e2e3a")
        
        self.notification_frame = tk.Frame(self.parent, bg=bg_color, relief=tk.SOLID, borderwidth=1)
        self.notification_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.notification_label = tk.Label(
            self.notification_frame,
            text=message,
            fg=text_color,
            bg=bg_color,
            font=("Arial", 9),
            wraplength=350
        )
        self.notification_label.pack(pady=5, padx=10)
        
        close_button = tk.Button(
            self.notification_frame,
            text="×",
            command=self.hide_notification,
            bg=bg_color,
            fg=text_color,
            relief=tk.FLAT,
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)
        
        if duration > 0:
            self.hide_timer = self.parent.after(duration, self.hide_notification)
    
    def hide_notification(self):
        if self.hide_timer:
            self.parent.after_cancel(self.hide_timer)
            self.hide_timer = None
        
        if self.notification_frame:
            self.notification_frame.destroy()
            self.notification_frame = None
            self.notification_label = None

def copy_to_clipboard(root_window: tk.Tk, text_to_copy: str, status_label: tk.Label):
    """Copia el texto dado al portapapeles y actualiza la etiqueta de estado."""
    try:
        text_to_copy = text_to_copy.strip()
        if not text_to_copy or text_to_copy == "Error al generar." or text_to_copy == "Error al guardar.":
            update_status_label(status_label, "Nada válido para copiar.", STATUS_WARNING_FG)
            return

        root_window.clipboard_clear()
        root_window.clipboard_append(text_to_copy)
        update_status_label(status_label, "¡Contraseña copiada al portapapeles!", STATUS_INFO_FG)
    except tk.TclError:
        update_status_label(status_label, "Error al copiar (portapapeles no accesible).", STATUS_ERROR_FG)

def gui_handle_generate_password(root_window: tk.Tk, display_widget: tk.Text, status_label: tk.Label, notification_banner=None):
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
        if notification_banner:
            notification_banner.show_notification(f"Error de Configuración: {str(ve)}", "error")
        status_label.config(text="Error de configuración al generar.", fg=STATUS_ERROR_FG)
        display_widget.config(state=tk.NORMAL)
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, "Error al generar.")
        display_widget.config(state=tk.DISABLED)
    except FileSavingError as fse:
        if notification_banner:
            notification_banner.show_notification(f"Error al Guardar: {str(fse)}", "error")
        status_label.config(text="Error al guardar el archivo.", fg=STATUS_ERROR_FG)
        display_widget.config(state=tk.NORMAL)
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, "Error al guardar.")
        display_widget.config(state=tk.DISABLED)
    except Exception as e:
        if notification_banner:
            notification_banner.show_notification(f"Error Inesperado: {str(e)}", "error")
        status_label.config(text="Error inesperado.", fg=STATUS_ERROR_FG)

def gui_handle_generate_password_compact(root_window: tk.Tk, display_widget: tk.Entry, status_label: tk.Label, notification_banner=None):
    """Versión compacta para manejar la generación de contraseña con Entry widget."""
    try:
        password = generate_password_and_save()
        
        display_widget.config(state=tk.NORMAL)
        display_widget.delete(0, tk.END)
        display_widget.insert(0, password)
        display_widget.config(state="readonly")
        
        status_label.config(text="¡Generada!", fg=STATUS_SUCCESS_FG)
        
    except ValueError as ve:
        if notification_banner:
            notification_banner.show_notification(f"Error: {str(ve)}", "error")
        status_label.config(text="Error al generar", fg=STATUS_ERROR_FG)
        display_widget.config(state=tk.NORMAL)
        display_widget.delete(0, tk.END)
        display_widget.insert(0, "Error")
        display_widget.config(state="readonly")
    except FileSavingError as fse:
        if notification_banner:
            notification_banner.show_notification(f"Error al guardar: {str(fse)}", "error")
        status_label.config(text="Error al guardar", fg=STATUS_ERROR_FG)
        display_widget.config(state=tk.NORMAL)
        display_widget.delete(0, tk.END)
        display_widget.insert(0, "Error al guardar")
        display_widget.config(state="readonly")
    except Exception as e:
        if notification_banner:
            notification_banner.show_notification(f"Error: {str(e)}", "error")
        status_label.config(text="Error inesperado", fg=STATUS_ERROR_FG)

def copy_to_clipboard_compact(root_window: tk.Tk, text_to_copy: str, status_label: tk.Label):
    """Versión compacta para copiar contraseña al portapapeles."""
    try:
        text_to_copy = text_to_copy.strip()
        if not text_to_copy or text_to_copy in ["Error", "Error al guardar"]:
            update_status_label(status_label, "Nada que copiar", STATUS_WARNING_FG)
            return

        root_window.clipboard_clear()
        root_window.clipboard_append(text_to_copy)
        update_status_label(status_label, "¡Copiada!", STATUS_INFO_FG)
    except tk.TclError:
        update_status_label(status_label, "Error al copiar", STATUS_ERROR_FG)

if __name__ == "__main__":
    # Configuración minimalista de la ventana
    root = tk.Tk()
    root.title("Kaospass")
    root.geometry("250x160")
    root.configure(bg=COLOR_PRIMARY_BG)
    root.resizable(False, False)
    
    # Frame principal compacto
    main_frame = tk.Frame(root, bg=COLOR_PRIMARY_BG)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    # Banner de notificaciones (oculto por defecto)
    notification_banner = NotificationBanner(main_frame)
    
    # Título minimalista
    title_label = tk.Label(
        main_frame, 
        text="Generador de Contraseñas",
        font=("Arial", 11, "bold"),
        fg=COLOR_TEXT_FG, 
        bg=COLOR_PRIMARY_BG
    )
    title_label.pack(pady=(0, 15))
    
    # Campo de contraseña compacto
    password_frame = tk.Frame(main_frame, bg=COLOR_PRIMARY_BG)
    password_frame.pack(fill=tk.X, pady=(0, 14))
    
    
    # Campo de contraseña ajustado exactamente para 10 caracteres
    password_display = tk.Entry(
        password_frame,
        width=12,
        font=("Consolas", 12, "bold"),
        bg=COLOR_TEXT_WIDGET_BG,
        fg=COLOR_TEXT_FG,
        relief=tk.SOLID,
        borderwidth=1,
        highlightbackground=COLOR_TEXT_WIDGET_BORDER,
        highlightcolor=COLOR_ACCENT,
        highlightthickness=1,
        justify="center",
        state="readonly"
    )
    password_display.pack(anchor="center", ipady=4)
    
    # Botones compactos
    button_frame = tk.Frame(main_frame, bg=COLOR_PRIMARY_BG)
    button_frame.pack(pady=(0, 10))
    
    generate_button = tk.Button(
        button_frame, 
        text="🔄",
        command=lambda: gui_handle_generate_password_compact(root, password_display, status_label, notification_banner),
        bg=COLOR_ACCENT, 
        fg=COLOR_BUTTON_FG,
        font=("Arial", 9, "bold"),
        relief=tk.FLAT, 
        activebackground="#005C99", 
        activeforeground=COLOR_BUTTON_FG,
        borderwidth=0, 
        highlightthickness=0,
        padx=10, 
        pady=6,
        cursor="hand2"
    )
    generate_button.pack(side=tk.LEFT, padx=(0, 10))
    
    copy_button = tk.Button(
        button_frame, 
        text="📋",
        command=lambda: copy_to_clipboard_compact(root, password_display.get(), status_label),
        bg=COLOR_SECONDARY_BG, 
        fg=COLOR_TEXT_FG,
        font=("Arial", 9),
        relief=tk.FLAT, 
        activebackground="#4A5A6D", 
        activeforeground=COLOR_TEXT_FG,
        borderwidth=1,
        highlightthickness=0,
        padx=15, 
        pady=6,
        cursor="hand2"
    )
    copy_button.pack(side=tk.LEFT)
    
    # Estado minimalista
    status_label = tk.Label(
        main_frame, 
        text="Listo", 
        font=("Arial", 8), 
        fg=STATUS_READY_FG, 
        bg=COLOR_PRIMARY_BG
    )
    status_label.pack()
    
    # Generar una contraseña inicial
    gui_handle_generate_password_compact(root, password_display, status_label, notification_banner)
    
    root.mainloop()
