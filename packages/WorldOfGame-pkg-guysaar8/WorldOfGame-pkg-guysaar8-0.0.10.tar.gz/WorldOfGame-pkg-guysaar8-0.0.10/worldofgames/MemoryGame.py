#####################
# import modules
#####################
from ManegeGame import GameManager
import random
import time
import os


#####################
# Define functions
#####################

def memory_game(difficulty):
    game_id = "Memory Game"
    user_chosen_nums = []
    generate_list = []

    # generate the guess list
    for i in range(difficulty):
        generate = random.randint(1, 101)
        generate_list.append(generate)
    print(generate_list)
    time.sleep(0.7)
    os.system('clear')

    # getting number from user
    print("choose number between 1 to 101")
    print("your choices so far", user_chosen_nums)
    checking_list = GameManager.check_if_number()
    choose_num = checking_list[0]
    if_digit = checking_list[1]

    # check range
    for i in range(1, difficulty):
        if type(choose_num) == int and 101 >= choose_num >= 1:  # check if int and if in range
            if choose_num in user_chosen_nums:  # check if number is already in the list
                os.system('clear')
                generate_random = random.randint(1, 101)
                user_chosen_nums.append(generate_random)
                GameManager.in_list()
                print('Try again')
                print("choose number between 1 to 101")
                print("your choices so far", user_chosen_nums)
                checking_list = GameManager.check_if_number()
                choose_num = checking_list[0]
                if_digit = checking_list[1]
            else:  # is int and in range
                os.system('clear')
                user_chosen_nums.append(choose_num)
                print("choose number between 1 to 101")
                print("your choices so far", user_chosen_nums)
                checking_list = GameManager.check_if_number()
                choose_num = checking_list[0]
                if_digit = checking_list[1]

        elif not if_digit:  # number is not int
            generate_random = random.randint(1, 101)
            user_chosen_nums.append(generate_random)
            GameManager.invalid_character()
            print('Try again')
            print("your choices so far", user_chosen_nums)
            checking_list = GameManager.check_if_number()
            choose_num = checking_list[0]
            if_digit = checking_list[1]
            os.system('clear')
        else:  # number was out of range
            generate_random = random.randint(1, 101)
            user_chosen_nums.append(generate_random)
            GameManager.out_of_range()
            print('Try again')
            print("your choices so far", user_chosen_nums)
            print("enter a number")
            checking_list = GameManager.check_if_number()
            choose_num = checking_list[0]
            if_digit = checking_list[1]

            os.system('clear')

    # check last append
    if if_digit is True and 101 >= choose_num >= 1:  # check if int and if in range
        if choose_num in user_chosen_nums:  # check if number is already in the list
            os.system('clear')
            generate_random = random.randint(1, 101)
            user_chosen_nums.append(generate_random)
            GameManager.in_list()
        else:  # is int and in range
            user_chosen_nums.append(choose_num)
    elif not if_digit:  # number is not int
        generate_random = random.randint(1, 101)
        user_chosen_nums.append(generate_random)
        GameManager.invalid_character()
    else:  # number was out of range
        generate_random = random.randint(1, 101)
        user_chosen_nums.append(generate_random)
        GameManager.out_of_range()

    # sorting lists
    generate_list = sorted(generate_list)
    user_chosen_nums = sorted(user_chosen_nums)

    if generate_list == user_chosen_nums:  # user won
        os.system('clear')
        print("YOU WON")
        print(generate_list, "Numbers generated by GAME MASTER")
        print(user_chosen_nums, "Your numbers")
        time.sleep(5)
        print("*" * 70)
        GameManager.again(game_id, difficulty)
    else:  # user lost
        os.system('clear')
        print("YOU LOST")
        print(generate_list, "Numbers generated by GAME MASTER")
        print(user_chosen_nums, "Your numbers")
        time.sleep(5)
        print("*" * 70)
        GameManager.again(game_id, difficulty)
