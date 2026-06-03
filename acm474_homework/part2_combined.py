# ============================================================
# ACM 474 - Term Homework | Part 2: Combined Caesar + Vigenere
# Student : Kivanc Mete Taskiran
# Plaintext   : MYNAMEISKIVANCMETETASKIRAN
# Caesar Shift: 18  (len("KIVANC")+len("METE")+len("TASKIRAN"))
# Vigenere Key: SECURITY
# ============================================================


# ── Caesar Cipher Functions ────────────────────────────────

def encrypt(text, s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


def decrypt(text, s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        # Decrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) - s - 65) % 26 + 65)
        # Decrypt lowercase characters
        else:
            result += chr((ord(char) - s - 97) % 26 + 97)
    return result


# ── Vigenere Cipher Functions ──────────────────────────────

# This function generates the key in a cyclic manner until
# its length isn't equal to the length of original text
def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))

# This function returns the encrypted text generated
# with the help of the key
def cipherText(string, key):
    cipher_text = []
    for i in range(len(string)):
        x = (ord(string[i]) +
             ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))

# This function decrypts the encrypted text and returns
# the original text
def originalText(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return("" . join(orig_text))


# ── Driver Code ────────────────────────────────────────────

if __name__ == "__main__":
    plaintext = "MYNAMEISKIVANCMETETASKIRAN"
    s         = 18          # Caesar shift key
    keyword   = "SECURITY"  # Vigenere key

    print("Plaintext: " + plaintext)

    # STEP 1: Apply Caesar encryption on the plaintext
    ciphertext1 = encrypt(plaintext, s)
    print("After Caesar Encryption (ciphertext1):   " + ciphertext1)

    # STEP 2: Apply Vigenere encryption on the Caesar ciphertext
    key = generateKey(ciphertext1, keyword)
    ciphertext2 = cipherText(ciphertext1, key)
    print("After Vigenere Encryption (ciphertext2): " + ciphertext2)

    # STEP 3: Decrypt - Vigenere first, then Caesar
    vigenere_key      = generateKey(ciphertext2, keyword)
    vigenere_decrypted = originalText(ciphertext2, vigenere_key)
    decrypted_plaintext = decrypt(vigenere_decrypted, s)
    print("Original/Decrypted Text: " + decrypted_plaintext)
