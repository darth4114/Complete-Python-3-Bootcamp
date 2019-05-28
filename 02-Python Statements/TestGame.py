from random import randint

user_num = int(input('Input a number!'))

#user_num = 13

if user_num == randint(0,3):
    print('You have guessed the right number!')
else:
    print('Sorry you did not guess correctly :(')
