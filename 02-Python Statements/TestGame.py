from random import randint

print('Wecome to the Guessing Game!')
print('See how close you can get to the number!')

ans = randint(1,101)
guesses = [0]

while True:
    guess = int(input('PIck your number!\n'))

    #check for valid answer
    if guess < 1 or guess > 100:
        print('OUT OF BOUNDS! Please try again: ')
        break

    #check for correct answer
    if guess == ans:
        print(f'CONGRATULATIONS, YOU GUESSED IT IN {len(guesses)} GUESSES!')
        break

    #add to list
    guesses.append(guess)

    #check for difference
    if guesses[-2]:
        if abs(ans-guess) < abs(ans-guesses[-2]):
            print('WARMER!')
        else:
            print('COLDER!')
    else:
        if abs(ans-guess) <= 10:
            print('WARM!')
        else:
            print('COLD!')
