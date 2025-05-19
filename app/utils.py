import numpy as np
from math import gcd
import string

# ——————————————
# 1) ALFABETO E PARÂMETROS BÁSICOS
#    • PAD_CHAR: caractere reservado para preencher os blocos (interno).
#    • ALPHABET: todos os caracteres válidos (inclui underscore, letras, dígitos e símbolos).
#    • MOD: tamanho do alfabeto, usado como módulo nas operações.
PAD_CHAR = '§'  # símbolo que nunca deve aparecer na entrada do usuário
ALPHABET = (
    PAD_CHAR           # índice 0, só para padding
    + string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    + string.digits         # '0123456789'
    + "!@#$%&*()-_=+[]{};:',.<>/?\\|`~ "  # símbolos diversos + espaço
)
MOD = len(ALPHABET)  # módulo = tamanho do alfabeto

# Mapeamentos para converter rapidamente
# caractere → índice  (0 .. MOD-1) e índice → caractere
CHAR_TO_INDEX = {c: i for i, c in enumerate(ALPHABET)}
INDEX_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}


# ——————————————
# 2) INVERSO MODULAR (via Algoritmo Estendido de Euclides)
def egcd(a, b):
    """
    Retorna (g, x, y) tais que:
      g = gcd(a, b)
      a*x + b*y = g
    Usado para encontrar coeficientes de Bézout.
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    # reconstrói x e y para a*x + b*y = g
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a, m):
    """
    Retorna o inverso de a em módulo m, i.e. x tal que (a*x) % m == 1.
    Usa egcd; lança erro se gcd(a, m) != 1 (sem inverso).
    """
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError(f"Sem inverso modular de {a} mod {m}")
    return x % m


# ——————————————
# 3) INVERSÃO DE MATRIZ NO MÓDULO (método da adjunta)
def matrix_mod_inv(matrix, modulus):
    """
    Dada uma matriz quadrada 'matrix' e um módulo 'modulus',
    devolve a matriz inversa em Z_modulus (i.e. K^{-1} tal que
      matrix.dot(K^{-1}) % modulus = I).
    Passos:
      1) calcula det mod modulus
      2) garante gcd(det, modulus)==1
      3) encontra det_inv = inverso modular de det
      4) constrói matriz de cofatores e obtém adjunta (cof.T)
      5) multiplica adjunta por det_inv mod modulus
    """
    # 1) determinante (float → int → mod)
    det = int(round(np.linalg.det(matrix))) % modulus
    # 2) checa se é invertível
    if gcd(det, modulus) != 1:
        raise ValueError(f"Determinante {det} não é invertível módulo {modulus}.")
    # 3) inverso do determinante
    det_inv = mod_inverse(det, modulus)

    # 4) monta matriz de cofatores
    n = matrix.shape[0]
    cof = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            # menor: remove linha i e coluna j
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            # cofactor (± det(minor))
            cof[i, j] = ((-1) ** (i + j)) * int(round(np.linalg.det(minor)))
    # adjunta = transposta da matriz de cofatores
    adj = cof.T

    # 5) inversa modular = det_inv * adjunta mod modulus
    return (det_inv * adj) % modulus


# ——————————————
# 4) ENCRIPTAÇÃO (Hill Cipher adaptado)
def hill_encrypt(plaintext: str, key_matrix: np.ndarray) -> str:
    """
    Cifra o texto em blocos de tamanho n = key_matrix.shape[0]:
      1) Filtra só os caracteres permitidos em ALPHABET[1:] (texto bruto).
      2) Calcula um único padding para que (1 + len(raw) + pad) % n == 0.
      3) Usa PAD_CHAR para preencher e um 'marker' inicial (ALPHABET[pad]).
      4) Converte cada char em índice, agrupa em matriz, multiplica mod MOD.
      5) Reconverte índices em caracteres e retorna a string cifrada.
    """
    # 1) mantém somente caracteres válidos (underscore, letras, dígitos, símbolos)
    raw = ''.join(c for c in plaintext if c in ALPHABET[1:])
    n = key_matrix.shape[0]

    # 2) quantos PAD_CHAR (internos) preciso para completar múltiplo de n
    pad = (n - (1 + len(raw)) % n) % n
    # marker informa esse número de pads na decriptação
    marker = ALPHABET[pad]

    # 3) constrói o texto a ser cifrado: marker + raw + PAD_CHAR*pad
    full = marker + raw + PAD_CHAR * pad

    # 4a) converte chars → índices
    nums = [CHAR_TO_INDEX[c] for c in full]
    # 4b) agrupa em blocos de n colunas
    mat = np.array(nums).reshape(-1, n)
    # 4c) aplica multiplicação de Hill em cada linha (vetor) e faz módulo
    enc_nums = (mat.dot(key_matrix) % MOD).flatten()

    # 5) índices → caracteres cifrados
    return ''.join(INDEX_TO_CHAR[i] for i in enc_nums)


# ——————————————
# 5) DECRIPTAÇÃO
def hill_decrypt(ciphertext: str, key_matrix: np.ndarray) -> str:
    """
    Reverte a encriptação:
      1) converte cada char cifrado em índice
      2) agrupa em matriz de blocos n
      3) multiplica pela matriz inversa mod MOD
      4) índices → chars decifrados
      5) lê o marker (primeiro char), remove padding do final
    """
    # 1) ciphertext → índices
    nums = [CHAR_TO_INDEX[c] for c in ciphertext]
    n = key_matrix.shape[0]
    mat = np.array(nums).reshape(-1, n)

    # 2) obtém K^{-1} em Z_MOD
    inv_key = matrix_mod_inv(key_matrix, MOD)
    # 3) decifra cada bloco e faz módulo
    dec_nums = (mat.dot(inv_key) % MOD).flatten()
    # 4) índices → texto completo (marker + raw + pads)
    dec_text = ''.join(INDEX_TO_CHAR[i] for i in dec_nums)

    # 5) extrai e usa o marker para remover os PAD_CHAR finais
    marker = dec_text[0]
    pad = CHAR_TO_INDEX[marker]  # número de chars a remover
    core = dec_text[1:]
    # se pad>0, corta os últimos pad caracteres; senão retorna tudo
    return core[:-pad] if pad > 0 else core


# ——————————————
# 6) MATRIZ-CHAVE (3×3)
#    Det deve ser coprimo com MOD para matriz ser invertível em Z_MOD.
key_matrix = np.array([
    [ 3, 10, 20],
    [20,  7, 21],
    [ 2,  4, 11]
], dtype=int)

# Funções gerais
def custom_encrypt(txt: str) -> str:
    return hill_encrypt(txt, key_matrix)

def custom_decrypt(ct: str) -> str:
    return hill_decrypt(ct, key_matrix)


# Teste
if __name__ == "__main__":
    msg = input("Digite a senha para criptografar: ")
    e = custom_encrypt(msg)
    d = custom_decrypt(e)

    print("\n=== Resultado ===")
    print("Original:   ", msg)
    print("Encrypted:  ", e)
    print("Decrypted:  ", d)
