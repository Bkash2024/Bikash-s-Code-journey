import random

def num_guess(start: int,finish: int):

    

    # Generate a random number between start and finish
    secret_number = random.randint(start, finish)
    attempts = 0
    # Set up the game loop
    guess = None
    while guess != secret_number:
        try:
            guess = int(input(f"Guess a number between {start} and {finish}: "))
            if start<= guess <= finish: 
                attempts += 1
                if guess < secret_number:
                    print(f"Too low! Try again.")
                elif guess > secret_number:
                    print(f"Too high! Try again.")
                else:
                    print(f"Congratulation success in {attempts} attempts")
            else:
                print(f'out of the range please give a number between{start} and {finish}')        
        except ValueError:
            print("That is not a valid number! Please type digits only.")





num_guess(5,50)