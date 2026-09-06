import unittest
from p5_Anger_Colby import caesar_cipher, caesar_decipher, letter_frequency

class TestCaesarCipher(unittest.TestCase):

    def test_cipher_basic(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_cipher_preserves_case(self):
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_decipher(self):
        encrypted = caesar_cipher("Hello World", 5)
        decrypted = caesar_decipher(encrypted, 5)
        self.assertEqual(decrypted, "Hello World")

    def test_letter_frequency(self):
        freq = letter_frequency("AaBbCc!!")
        self.assertEqual(freq["a"], 2)
        self.assertEqual(freq["b"], 2)
        self.assertEqual(freq["c"], 2)
        self.assertEqual(freq["d"], 0)

if __name__ == "__main__":
    unittest.main()
