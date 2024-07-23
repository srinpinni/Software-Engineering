def decode(password):
    decoded_password = ''.join(str(int(char) - 3) for char in password)
    return decoded_password

