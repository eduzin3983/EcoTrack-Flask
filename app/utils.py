import numpy as np

def mod_inverse(a, m):
    #Calcula o inverso modular de 'a' em relação a 'm'.
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Inverso modular não encontrado.")

def hill_encrypt(password, key_matrix):
    #Criptografa a senha usando a Cifra de Hill.
    password = password.upper()
    while len(password) % len(key_matrix) != 0:
        password += 'X'  # Preenche com 'X' para ajustar o tamanho

    # Converte a senha em números (A=0, B=1, ..., Z=25)
    password_vector = [ord(char) - ord('A') for char in password]
    password_matrix = np.array(password_vector).reshape(-1, len(key_matrix))

    # Multiplica pela matriz de chave e aplica módulo 26
    encrypted_matrix = (np.dot(password_matrix, key_matrix) % 26).flatten()

    # Converte de volta para caracteres
    encrypted_password = ''.join(chr(num + ord('A')) for num in encrypted_matrix)
    return encrypted_password

def hill_decrypt(encrypted_password, key_matrix):
    #Descriptografa a senha usando a Cifra de Hill.
    encrypted_password = encrypted_password.upper()

    # Converte a senha criptografada em números
    encrypted_vector = [ord(char) - ord('A') for char in encrypted_password]
    encrypted_matrix = np.array(encrypted_vector).reshape(-1, len(key_matrix))

    # Calcula a matriz inversa da chave no módulo 26
    determinant = int(round(np.linalg.det(key_matrix)))
    determinant_mod_inverse = mod_inverse(determinant % 26, 26)
    adjugate_matrix = np.round(determinant * np.linalg.inv(key_matrix)).astype(int) % 26
    inverse_key_matrix = (determinant_mod_inverse * adjugate_matrix) % 26

    # Multiplica pela matriz inversa e aplica módulo 26
    decrypted_matrix = (np.dot(encrypted_matrix, inverse_key_matrix) % 26).flatten()

    # Converte de volta para caracteres
    decrypted_password = ''.join(chr(num + ord('A')) for num in decrypted_matrix)
    return decrypted_password

# Matriz chave
key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])

def custom_encrypt(password):
    return hill_encrypt(password, key_matrix)

def custom_decrypt(encrypted_password):
    return hill_decrypt(encrypted_password, key_matrix)