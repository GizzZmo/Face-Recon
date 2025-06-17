"""
Quantum-safe encryption utilities using the Kyber algorithm (from pqcrypto).
"""

from pqcrypto.kem.kyber import generate_keypair, encrypt, decrypt

def generate_keys():
    public_key, private_key = generate_keypair()
    return public_key, private_key

def encrypt_message(public_key, message):
    ciphertext, shared_secret = encrypt(public_key)
    # In practice, use shared_secret for symmetric encryption of `message`
    return ciphertext, shared_secret

def decrypt_message(ciphertext, private_key):
    decrypted_secret = decrypt(ciphertext, private_key)
    return decrypted_secret

if __name__ == "__main__":
    pub, priv = generate_keys()
    ciphertext, secret = encrypt_message(pub, b"secret")
    decrypted = decrypt_message(ciphertext, priv)
    print(f"Decrypted secret: {decrypted}")
