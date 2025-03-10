def encrypt(key, plaintext, mod=256):
    ciphertext = ['' for _ in range(len(plaintext))]

    for i in range(len(plaintext)):
        ciphertext[i] = chr((ord(plaintext[i]) + ord(key[i % len(key)])) % mod)

    return ''.join(ciphertext)

def decrypt(key, cihpertext, mod=256):
    plaintext = ['' for _ in range(len(cihpertext))]

    for i in range(len(cihpertext)):
        plaintext[i] = chr((ord(cihpertext[i]) - ord(key[i % len(key)])) % mod)

    return ''.join(plaintext)


if __name__ == "__main__":
    key = "sony"
    plaintext = "thisplaintext"
    encrypted = encrypt(key, plaintext)
    decrypted = decrypt(key, encrypted)

    print(plaintext)
    print(encrypted)
    print(decrypted)
