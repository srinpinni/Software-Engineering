def encode(password):
    encoded_password = ''.join(str(int(char) + 3) for char in password)
    return encoded_password



def main():
    encoded_password = None

    while True:
        print("\nMenu")
        print("-------------")
        print("1. Encode")
        print("2. Decode")
        print("3. Quit\n")

        try:
            option = int(input("Please enter an option: "))

            if option == 1:
                password = input("Please enter your password to encode: ")
                encoded_password = encode(password)
                print("Your password has been encoded and stored!")

            elif option == 2:
                if encoded_password:
                    original_password = decode(encoded_password)
                    print(f"The encoded password is {encoded_password}, and the original password is {original_password}.")
                else:
                    print("No password has been encoded yet.")

            elif option == 3:
                break

            else:
                print("Invalid option. Please enter 1, 2, or 3.")

        except ValueError:
            print("Invalid input. PLease enter a number.")

if __name__ == '__main__':
    main()