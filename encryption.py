from pqcrypto.kem.kyber import decrypt, encrypt, generate_keypair

public_key, private_key = generate_keypair()
ciphertext, shared_secret = encrypt(public_key)
decrypted_secret = decrypt(ciphertext, private_key)

print("Sikker nøkkel:", decrypted_secret)
