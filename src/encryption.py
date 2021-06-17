import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as aspadding

# pseudolosowy ciąg przy złym haśle
# pseudolosowy ciąg przy złym kluczu

# własne szyfrowanie i odszyfrowanie tego klucza prywatnego
# tamta losowość
# duże pliki?

# funkcja generująca hash przy użyciu SHA256
def hash(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data.encode())
    hashed = digest.finalize()
    return hashed


# funkcja szyfrująca klucz prywatny przy użyciu AESa w trybie CBC z encryption key = hash hasła użytkownika
def encrypt_RSA_key(private_key,password):
    # generowanie wektora inicjalizującego
    iv = os.urandom(16)

    # generowania hasha hasła użytkownika
    hashed_password = hash(password)

    # dodawanie paddingu do klucza prywatnego
    padder = padding.PKCS7(128).padder()
    padded_key = padder.update(private_key)
    padded_key += padder.finalize()

    # szyfrowanie klucza prywatnego
    cipher = Cipher(algorithms.AES(hashed_password), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_private_key = encryptor.update(padded_key) + encryptor.finalize()

    return encrypted_private_key, iv


# funkcja odszyfrowująca klucz prywatny
def decrypt_RSA_key(file_path, password):
    # otwarcie pliku z kluczem prywatnym
    privkey_file = open(file_path, "rb")

    # wczytanie wektora inicjalizującego
    iv = privkey_file.read(16)

    # wczytanie zaszyfrowanego klucza prywatnego
    private_key_encrypted = privkey_file.read()

    # zamknięcie pliku z kluczem prywatnym
    privkey_file.close()

    # generowanie hasha z podanego przez użytkownika hasła do klucza
    hashed_password = hash(password)

    # deszyfrowanie
    cipher = Cipher(algorithms.AES(hashed_password), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(private_key_encrypted) + decryptor.finalize()

    # usuwanie paddingu
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted)
    unpadded_data += unpadder.finalize()

    # wczytanie klucza do formy obsługiwanej przez bibliotekę
    private_key = serialization.load_pem_private_key(
        unpadded_data,
        password=None)

    return private_key

# inicjalizacja folderów do przechowywania kluczy
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


# funkcja tworząca pare kluczy RSA
def create_RSA_keys(password):

    #tworzenie folderów
    directories_initialization()

    # tworzenie klucza prywatnego
    private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048)

    # serializacja klucza prywatnego
    pem_prv = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm = serialization.NoEncryption())

    #szyfrowanie klucza prywatnego
    private_key_ciphered, iv = encrypt_RSA_key(pem_prv,password)
    pem_prv = iv + private_key_ciphered

    # tworzenie klucza publicznego
    public_key = private_key.public_key()

    # serializacja klucza publicznego
    pem_pub = public_key.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo)

    # zapisanie klucza prywatnego do folderu
    privkey_file = open("user_prv_keys/klucz.pem", "wb")
    privkey_file.write(pem_prv)
    privkey_file.close()

    # zapisanie klucza publicznego do folderu
    pubkey_file = open("user_pub_keys/klucz.pub", "wb")
    pubkey_file.write(pem_pub)
    pubkey_file.close()


# funkcja szyfrująca klucz sesyjny
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


# funkcja odszyfrowująca klucz sesyjny
def decrypt_session_key(session_key, private_key_path, password):
    # wczytanie klucza prywatnego
    private_key = decrypt_RSA_key(private_key_path,password)
    a = len(session_key)
    # odszyfrowanie klucza sesyjnego
    decrypted_skey = private_key.decrypt(
    session_key,
    aspadding.OAEP(
        mgf = aspadding.MGF1(algorithm=hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None))

    return decrypted_skey


# data_path = ścieżka do pliku, encryption_mode = tryb blokowy w formie stringa np. "ecb" lub "ofb"
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


# data_path = ścieżka do pliku, encryption_mode = tryb blokowy w formie stringa np. "ecb" lub "ofb"
# session_key = klucz sesyjny, iv = wektor inicjalizacyjny
# zwraca 0 jak podano zły tryb
def decrypt(data_path, encryption_mode, private_key_path, private_key_password,  encrypted_session_key, iv):
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

    # deszyfrowanie klucza sesyjnego
    session_key = decrypt_session_key(encrypted_session_key,private_key_path,private_key_password)

    # deszyfrowanie
    cipher = Cipher(algorithms.AES(session_key), mode)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()

    # usuwanie paddingu
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted)
    unpadded_data += unpadder.finalize()

    return unpadded_data
