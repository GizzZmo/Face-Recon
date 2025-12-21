"""
Quantum-safe encryption utilities using the Kyber algorithm (from pqcrypto).

Provides high-level functions for key generation, encryption, and decryption
using post-quantum cryptography.
"""

try:
    from pqcrypto.kem.kyber import decrypt, encrypt, generate_keypair

    KYBER_AVAILABLE = True
except ImportError:
    KYBER_AVAILABLE = False
    print("Warning: pqcrypto not installed. Encryption unavailable.")


def generate_keys():
    """
    Generate a quantum-safe key pair.

    Returns:
        Tuple of (public_key, private_key)

    Raises:
        ImportError: If pqcrypto is not installed
    """
    if not KYBER_AVAILABLE:
        raise ImportError("pqcrypto package required. Install: pip install pqcrypto")
    public_key, private_key = generate_keypair()
    return public_key, private_key


def encrypt_message(public_key, message=None):
    """
    Encrypt using public key and generate shared secret.

    Args:
        public_key: Public key from generate_keys()
        message: Optional message (currently unused, for API compatibility)

    Returns:
        Tuple of (ciphertext, shared_secret)
        In practice, use shared_secret for symmetric encryption of message

    Raises:
        ImportError: If pqcrypto is not installed
    """
    if not KYBER_AVAILABLE:
        raise ImportError("pqcrypto package required. Install: pip install pqcrypto")
    ciphertext, shared_secret = encrypt(public_key)
    return ciphertext, shared_secret


def decrypt_message(ciphertext, private_key):
    """
    Decrypt ciphertext using private key.

    Args:
        ciphertext: Ciphertext from encrypt_message()
        private_key: Private key from generate_keys()

    Returns:
        Decrypted shared secret (bytes)

    Raises:
        ImportError: If pqcrypto is not installed
    """
    if not KYBER_AVAILABLE:
        raise ImportError("pqcrypto package required. Install: pip install pqcrypto")
    decrypted_secret = decrypt(ciphertext, private_key)
    return decrypted_secret


if __name__ == "__main__":
    if KYBER_AVAILABLE:
        pub, priv = generate_keys()
        ciphertext, secret = encrypt_message(pub, b"secret")
        decrypted = decrypt_message(ciphertext, priv)
        print(f"Decrypted secret: {len(decrypted)} bytes")
        print("Encryption test successful!")
    else:
        print("Kyber encryption not available. Install pqcrypto to use.")
