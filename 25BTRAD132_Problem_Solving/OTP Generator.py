import random 

# Function to generate a random OTP of a given length
def generate_otp(length=6):
    digits = "0123456789"
    otp = ""

    # Pick a random character from 'digits' length times
    for i in range(length):
        otp += random.choice(digits)

    return otp

# Test the function
my_otp = generate_otp(6)
print("Your OTP is:", my_otp)