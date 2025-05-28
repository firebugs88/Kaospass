import secrets
import string
import os

# Función auxiliar para mezclar una lista de forma segura
def _secure_shuffle(lst):
    """Mezcla una lista en su lugar utilizando secrets.randbelow para aleatoriedad criptográfica."""
    n = len(lst)
    for i in range(n - 1, 0, -1):
        # secrets.randbelow(k) genera un entero aleatorio en [0, k-1]
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]

def generate_password_and_save(length=8,
                               file_name=os.path.expanduser("~F:/gitpass/gitpass.txt"),
                               min_lower=1,
                               min_upper=1,
                               min_digits=3,
                               min_punctuation=1):
    """
    Genera una contraseña aleatoria de la longitud dada que cumple con los requisitos
    de caracteres especificados (minúsculas, mayúsculas, dígitos, puntuación).
    Guarda la contraseña generada en la ruta de archivo dada, creando el directorio
    si no existe.

    Parámetros:
    - length (int): La longitud de la contraseña a generar. Por defecto 12.
    - file_name (str): La ruta del archivo para guardar la contraseña generada.
                       Por defecto "~/Desktop/new_pass/pass.txt".
    - min_lower (int): Número mínimo de caracteres en minúscula. Por defecto 1.
    - min_upper (int): Número mínimo de caracteres en mayúscula. Por defecto 1.
    - min_digits (int): Número mínimo de dígitos. Por defecto 3.
    - min_punctuation (int): Número mínimo de signos de puntuación. Por defecto 1.

    Devuelve:
    La cadena de contraseña generada.

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

        with open(file_name, "a") as file: # Se mantiene el modo 'append' (añadir)
            file.write(password + "\n")
        print(f"Contraseña guardada exitosamente en: {file_name}")
    except IOError as e: # Excepción más específica para errores de E/S
        print(f"Error de E/S al guardar la contraseña en el archivo ({file_name}): {e}")
    except OSError as e: # Para errores como fallo al crear directorio
        print(f"Error del sistema operativo al crear el directorio o guardar el archivo ({file_name}): {e}")
    except Exception as e: # Captura genérica para otros errores inesperados
        print(f"Ocurrió un error inesperado al guardar la contraseña: {e}")
            
    return password

# Bloque para ejecutar como script
if __name__ == "__main__":
    try:
        # Generar una contraseña con los valores por defecto y guardarla
        password_generada = generate_password_and_save()
        print(f"Contraseña generada: {password_generada}")

        # Ejemplo de contraseña más larga y con más dígitos/puntuación
        # password_custom = generate_password_and_save(length=16, file_name="custom_pass.txt", min_digits=4, min_punctuation=2)
        # print(f"Contraseña personalizada generada: {password_custom}")
        
        # Ejemplo que podría lanzar ValueError si la longitud es muy corta
        # Intenta generar una contraseña de longitud 5 (requiere 1+1+3+1 = 6 por defecto)
        # password_corta = generate_password_and_save(length=5)
        # print(f"Contraseña corta generada: {password_corta}")

    except ValueError as ve:
        print(f"Error en la configuración para generar contraseña: {ve}")
    except Exception as e:
        print(f"Ha ocurrido un error general: {e}")
