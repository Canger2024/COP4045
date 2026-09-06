import string

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            alphabet = string.ascii_uppercase if char.isupper() else string.ascii_lowercase
            idx = alphabet.index(char)
            shifted_idx = (idx + shift) % 26
            result += alphabet[shifted_idx]
        else:
            result += char
    return result


def caesar_decipher(ciphertext, shift):
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    freq = {letter: 0 for letter in string.ascii_lowercase}
    for char in text.lower():
        if char in freq:
            freq[char] += 1
    return freq


def main():
    print("=== Interactive Caesar Cipher Tool ===")

    while True:
        print("\nMenu:")
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Analyze letter frequency")
        print("4. Quit")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            text = input("Enter text to encrypt: ")
            shift = int(input("Enter shift value: "))
            encrypted = caesar_cipher(text, shift)
            print("\nEncrypted text:", encrypted)
            print("\nLetter frequency:")
            for letter, count in letter_frequency(encrypted).items():
                print(f"{letter}: {count}")
            print("\nDeciphered back:", caesar_decipher(encrypted, shift))

        elif choice == "2":
            text = input("Enter text to decrypt: ")
            shift = int(input("Enter shift value: "))
            decrypted = caesar_decipher(text, shift)
            print("\nDecrypted text:", decrypted)

        elif choice == "3":
            text = input("Enter text to analyze: ")
            freq = letter_frequency(text)
            print("\nLetter frequency:")
            for letter, count in freq.items():
                print(f"{letter}: {count}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            

if __name__ == "__main__":
    main()
