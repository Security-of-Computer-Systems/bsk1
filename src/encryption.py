import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as aspadding

# pseudolosowy ciąg przy złym haśle
# pseudolosowy ciąg przy złym kluczu
# zachowanie rozszerzenia -> to chyba i tak u patryka
# inne szyfrowanie klucza prywatnego? opinia patryka?


# inicjalizacja folderów
def directories_initialization():

    # folder na własne klucze publiczne
    if os.path.exists("user_pub_keys") and os.path.isdir("user_pub_keys"):
        pass
    else:
        os.mkdir("user_pub_keys")

    # folder na własne klucze prywatne
    if os.path.exists("user_prv_keys") and os.path.isdir("user_prv_keys"):
        pass
    else:
        os.mkdir("user_prv_keys")

    # folder na klucze publiczne innych
    if os.path.exists("other_keys") and os.path.isdir("other_keys"):
        pass
    else:
        os.mkdir("other_keys")


def create_RSA_keys():

    #tworzenie folderów
    directories_initialization()

    # tworzenie klucza prywatnego
    private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048)

    # serializacja klucza prywatnego
    pem_prv = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.BestAvailableEncryption(b'mypassword')) #problem? nie wiem czym ten klucz jest szyforwany

    # tworzenie klucza publicznego
    public_key = private_key.public_key()

    # serializacja klucza publicznego
    pem_pub = public_key.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo)

    # zapisanie klucza prywatnego do folderu
    privkey_file = open("user_prv_keys/klucz.txt", "wb") #problem? rozszerzenie nic nie zmienia ale może "wyglądać lepiej"
    privkey_file.write(pem_prv)
    privkey_file.close()

    # zapisanie klucza publicznego do folderu
    pubkey_file = open("user_pub_keys/klucz_pub.txt", "wb")
    pubkey_file.write(pem_pub)
    pubkey_file.close()


def encrypt_session_key(session_key, public_key_path):
    #wczytanie klucza publicznego
    pubkey = open(public_key_path, "rb")
    public_key = serialization.load_pem_public_key(
        pubkey.read())
    pubkey.close()

    #zaszyfrowanie klucza sesyjnego
    ciphered_skey = public_key.encrypt(
    session_key,
    aspadding.OAEP(
        mgf = aspadding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None))

    return ciphered_skey

# przyjmuje klucz sesyjne, ścieżkę doi klucza prywatnego i hasło klucza prywatnego
def decrypt_session_key(session_key, private_key_path, password):
    # wczytanie klucza prywatnego
    privkey_file = open(private_key_path, "rb")
    private_key = serialization.load_pem_private_key(
        privkey_file.read(),
        password=b'mypassword')
    privkey_file.close()

    # odszyfrowanie klucza sesyjnego
    decrypted_skey = private_key.decrypt(
    session_key,
    aspadding.OAEP(
        mgf = aspadding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None))
    return decrypted_skey


# data_path = ścieżka do pliku, encryption_mode = tryb blokowy w formie stringa np. "ECB" lub "OFB"
# zwraca 0 jak podano zły tryb
def encrypt(data_path, encryption_mode):

    # wczytanie pliku do zaszyfrowania ze ścieżki
    file = open(data_path, 'rb')
    data = file.read()
    file.close()

    # dodawania paddingu - uzupełnienie do wielkości bloku
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data)
    padded_data += padder.finalize()

    # generowanie klucza sesyjnego
    key = os.urandom(32)

    # generowanie wektora inicjalizującego
    iv = os.urandom(16)

    # wybór trybu
    if encryption_mode == "cbc":
        mode = modes.CBC(iv)
    elif encryption_mode == "ecb":
        mode = modes.ECB()
    elif encryption_mode == "ofb":
        mode = modes.OFB(iv)
    elif encryption_mode == "cfb":
        mode = modes.CFB(iv)
    else:
        return 0

    # szyfrowanie
    cipher = Cipher(algorithms.AES(key), mode)
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    # zwracanie szyfrogramu, klucza sesyjnego i wektora inicjalizującego
    return ct, key, iv


# data_path = ścieżka do pliku, encryption_mode = tryb blokowy w formie stringa np. "ECB" lub "OFB"
# session_key = klucz sesyjny, iv = wektor inicjalizacyjny
# zwraca 0 jak podano zły tryb
def decrypt(data_path, encryption_mode, session_key, iv):
    # wczytanie pliku do odszyfrowania ze ścieżki
    file = open(data_path, 'rb')
    data = file.read()
    file.close()

    # wybór trybu
    if encryption_mode == "cbc":
        mode = modes.CBC(iv)
    elif encryption_mode == "ecb":
        mode = modes.ECB()
    elif encryption_mode == "ofb":
        mode = modes.OFB(iv)
    elif encryption_mode == "cfb":
        mode = modes.CFB(iv)
    else:
        return 0

    # deszyfrowanie
    cipher = Cipher(algorithms.AES(session_key), mode)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()

    # usuwanie paddingu
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted)
    unpadded_data += unpadder.finalize()

    return unpadded_data


