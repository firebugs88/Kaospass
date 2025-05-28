"""
generate_password_and_save genera una contraseña aleatoria de la longitud dada
que contiene una mezcla de minúsculas, mayúsculas, dígitos y signos de puntuación. Guarda
la contraseña generada en la ruta de archivo dada.

Parámetros:
- length (int): La longitud de la contraseña a generar. Por defecto 12.
- file_name (str): La ruta del archivo para guardar la contraseña generada.

Devuelve:
La cadena de contraseña generada.
"""
import secrets
import string
import os

def generate_password_and_save(length=10, file_name= os.path.expanduser("~/Desktop/new_pass/pass.txt")):
    alphabet = string.ascii_letters + string.digits 
    
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    try:
        with open(file_name, "a") as file:
            file.write(password + "\n")
    except Exception as e:
        print("Error al guardar la contraseña en el archivo:", e)
            
    return password

# Generar una contraseña y guardarla en un archivo
password = generate_password_and_save()
print("Contraseña generada:", password)