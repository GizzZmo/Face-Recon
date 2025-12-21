"""
Quantum-safe encryption module using Kyber KEM.

This module demonstrates post-quantum cryptography for securing
sensitive data in the Face-Recon system.

Note: Requires pqcrypto package: pip install pqcrypto
"""

try:
    from pqcrypto.kem.kyber import decrypt, encrypt, generate_keypair

    # Generate quantum-safe key pair
    public_key, private_key = generate_keypair()

    # Encrypt: generates ciphertext and shared secret
    ciphertext, shared_secret = encrypt(public_key)

    # Decrypt: recovers the shared secret
    decrypted_secret = decrypt(ciphertext, private_key)

    # Verify encryption works
    assert shared_secret == decrypted_secret, "Encryption/decryption failed!"

    print(f"Secure key established: {len(decrypted_secret)} bytes")
    print("Quantum-safe encryption ready!")

except ImportError:
    print("Warning: pqcrypto not installed. Install with: pip install pqcrypto")
    print("Quantum-safe encryption unavailable.")
