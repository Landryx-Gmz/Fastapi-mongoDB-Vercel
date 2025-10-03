from passlib.context import CryptContext

# Usamos bcrypt, como quieres
crypt = CryptContext(schemes=["bcrypt"]) 

# Genera el hash de la contraseña '123456'
hash_password = crypt.hash("123456")

print(hash_password)