import random


def num_guess(start: int, finish: int) -> None:
    """
    Run a number guessing game where the user tries to guess a random number.

    Args:
        start: The lower bound of the random number range (inclusive).
        finish: The upper bound of the random number range (inclusive).

    The function generates a random number between start and finish, then
    prompts the user to guess until they find the correct number, providing
    hints whether each guess is too high or too low.
    """
    secret_number = random.randint(start, finish)
    attempts = 0
    guess = None
    while guess != secret_number:
        try:
            guess = int(input(f"Guess a number between {start} and {finish}: "))
            if start <= guess <= finish:
                attempts += 1
                if guess < secret_number:
                    print("Too low! Try again.")
                elif guess > secret_number:
                    print("Too high! Try again.")
                else:
                    print(f"Congratulations success in {attempts} attempts")
            else:
                print(f"out of the range please give a number between {start} and {finish}")
        except ValueError:
            print("That is not a valid number! Please type digits only.")


if __name__ == "__main__":
    num_guess(5, 50)
