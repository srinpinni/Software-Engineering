def decode(password):
    final = []
    for num in password:
        final.append(int(num)-3)
    string = ''
    for num in final:
        string += str(num)
    return string