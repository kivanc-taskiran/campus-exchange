# ============================================================
# ACM 474 - Term Homework | Part 1: Caesar (Shift) Cipher
# Student : Kivanc Mete Taskiran
# Plaintext: MYNAMEISKIVANCMETETASKIRAN
# Shift    : 18  (total chars in KIVANC + METE + TASKIRAN)
# ============================================================

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


# Driver code
text = "MYNAMEISKIVANCMETETASKIRAN"
s = 18  # len("KIVANC") + len("METE") + len("TASKIRAN") = 6 + 4 + 8 = 18

print("Plaintext:  " + text)
print("Shift:      " + str(s))
print("Ciphertext: " + encrypt(text, s))
print("Decrypted:  " + decrypt(encrypt(text, s), s))
