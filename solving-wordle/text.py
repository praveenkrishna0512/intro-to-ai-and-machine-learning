import os
from time import sleep

dir_path = os.getcwd()
word_list = open(os.path.join(dir_path, 'words.txt'), 'r').read().splitlines()
print(f"original length: {len(word_list)}")

from turtle import pos


def filter_available_words(guess_word, colours, possible_words):
    '''
    Filters the list of possible words after making a guess.

    Parameters
    ----------
    guess_word:
        A string of the guess word.
    colours:
        A string representation of the colours of the result of the guess word.
    possible_words:
        A list of strings of all possible remaining words in the word list before this guess.
    
    Returns
    -------
        A list of possible words after making this guess.
    '''
    guess_word = guess_word.lower()

    green = "G"
    yellow = "Y"
    black = "B"
    if black not in colours and yellow not in colours:
        # Guess is the correct word
        return [guess_word]
    
    # Key: letter
    # Value: Array containing the index where the letter occured, and the number of non-black occurences
    occurence_dict = {}
    for index in range(len(guess_word)):
        letter = guess_word[index]
        if letter not in occurence_dict.keys():
            occurence_dict[letter] = [[], 0]
        occurence_dict[letter][0].append(index)
        if colours[index] != black:
            occurence_dict[letter][1] += 1
    # print(occurence_dict)

    for index in range(len(guess_word)):
        current_colour = colours[index]
        current_letter = guess_word[index]

        if current_colour == green:
            green_filter = lambda word : word[index] == current_letter
            possible_words = list(filter(green_filter, possible_words))
            # print(f"current length: {len(possible_words)}")
            # print(possible_words)

        elif current_colour == yellow:
            def yellow_filter(word):
                # Check if current letter is either not in word OR in the same index as guess word
                if current_letter not in word or word[index] == current_letter:
                    return False
                letter_occurence = occurence_dict[current_letter]
                min_num_of_letters = letter_occurence[1]
                if min_num_of_letters == 1:
                    return True
                # Reaching here means that the curr letter IS in word, NOT in curr index, and its repeated
                if word.count(current_letter) < min_num_of_letters:
                    return False
                return True
            possible_words = list(filter(yellow_filter, possible_words))
            # print(f"current length: {len(possible_words)}")
            # print(possible_words)

        elif current_colour == black:
            def black_filter(word):
                # Check if current letter is not in word
                if current_letter not in word:
                    return True
                if current_letter == word[index]:
                    return False
                # Curr letter is in this word
                letter_occurence = occurence_dict[current_letter]
                max_num_of_letters = letter_occurence[1]
                if max_num_of_letters == 0:
                    # Letter is not repeated or it is repeated but does not belong in word
                    return False
                # Reaching here means that the curr letter is repeated and IS in CORRECT word and should not be filtered out
                if word.count(current_letter) > max_num_of_letters:
                    return False
                return True
            possible_words = list(filter(black_filter, possible_words))
            # print(f"current length: {len(possible_words)}")
            # print(possible_words)
    
    return possible_words

# print(filter_available_words("CECRY", "YGGBB", word_list))
# print(filter_available_words("CECRC", "GGYYB", word_list))
# test_case = filter_available_words("tests", "BGYBB", word_list)
# print(test_case)

list_test = ['cease', 'dense', 'geese', 'lease', 'leash', 'reuse', 'sedan', 'seedy', 'segue', 'seize', 'semen', 'sepia', 'serif', 'serum', 'serve', 'seven', 'sever', 'sewer', 'verse', 'verso', 'welsh', 'cense', 'deash', 'deism', 'eensy', 'fease', 'feese', 'herse', 'leese', 'leish', 'lense', 'mease', 'mensa', 'mense', 'mensh', 'merse', 'meuse', 'neese', 'newsy', 'pease', 'peise', 'pepsi', 'perse', 'peyse', 'seame', 'seamy', 'seare', 'seaze', 'sebum', 'secco', 'seder', 'sedge', 'sedgy', 'sedum', 'seeld', 'seely', 'seepy', 'sefer', 'segar', 'segni', 'segno', 'segol', 'sehri', 'seine', 'seiza', 'selah', 'sella', 'selle', 'selva', 'semee', 'semie', 'sengi', 'senna', 'senor', 'senvy', 'senza', 'sepad', 'sepal', 'sepic', 'sepoy', 'serac', 'serai', 'seral', 'sered', 'serer', 'serge', 'seric', 'serin', 'seron', 'serow', 'serra', 'serre', 'serry', 'servo', 'sewan', 'sewar', 'sewed', 'sewel', 'sewen', 'sewin', 'sexed', 'sexer', 'seyen', 'weise', 'wersh', 'yeesh']

# DO NOT MODIFY:
def make_evaluate_guess(word, word_list):
    def evaluate_guess(guess_word):
        if guess_word not in word_list:
            raise Exception("Guess word not in word list")
        word_length = len(word)
        if len(guess_word) != word_length:
            raise Exception("Guess word not of correct length")

        result = ['B']*word_length
        word_l = list(word)
        ignore_index = []
        for i in range(word_length):
            if i in ignore_index:
                continue
            if guess_word[i] == word_l[i]:
                result[i] = 'G'
                word_l[i] = '-'
                ignore_index.append(i)
        for i in range(word_length):
            if i in ignore_index:
                continue
            for j in range(word_length):
                if guess_word[i] == word_l[j]:
                    result[i] = 'Y'
                    word_l[j] = '-'
                    break
        return ''.join(result)
    return evaluate_guess

# def generate_smart_guess(word_list, possible_words, nth_guess):
#     '''
#     Generates a good guess word from the list of possible words.

#     Parameters
#     ----------
#     word_list:
#         A list of strings of all words in the word list.
#     possible_words:
#         A list of strings of all possible remaining words in the word list.
#     nth_guess:
#         A number indicating how many guesses have been made so far inclusive of this one.
    
#     Returns
#     -------
#         A string of a good guess.
#     '''
#     def heuristic(guess_word, potential_answer):
#         print(guess_word)
#         colours = make_evaluate_guess(potential_answer, word_list)(guess_word)
#         # result = filter_available_words(guess_word, colours, possible_words)
#         # G = 10, Y = 5, B = 1
#         points = 0
#         for colour in colours:
#             if colour == "G":
#                 points += 10
#             if colour == "Y":
#                 points += 5
#             if colour == "B":
#                 points += 1
#         return points
  
#     if nth_guess == 1:
#         return "salet"
    
#     guess_points_dict = {}
#     for possible_guess in possible_words:
#         total_points = 0
#         for potential_answer in possible_words:
#             total_points += heuristic(possible_guess, potential_answer)
#         guess_points_dict[possible_guess] = total_points
      
#     v = list(guess_points_dict.values())
#     k = list(guess_points_dict.keys())
#     return k[v.index(max(v))]



# def generate_smart_guess(word_list, possible_words, nth_guess):
#     '''
#     Generates a good guess word from the list of possible words.

#     Parameters
#     ----------
#     word_list:
#         A list of strings of all words in the word list.
#     possible_words:
#         A list of strings of all possible remaining words in the word list.
#     nth_guess:
#         A number indicating how many guesses have been made so far inclusive of this one.
    
#     Returns
#     -------
#         A string of a good guess.
#     '''
#     colour_letters = ["B", "Y", "G"]
#     colours_arr = ["B", "Y", "G"]
#     for i in range(4):
#         temp_array = []
#         for word in colours_arr:
#             for letter in colour_letters:
#                 new_word = word + letter
#                 temp_array.append(new_word)
#         colours_arr = temp_array

#     letter_distribution = {}
#     for word in possible_words:
#         letter_set = set()
#         for letter in word:
#             if letter in letter_set:
#                 continue
#             if letter not in letter_distribution.keys():
#                 letter_distribution[letter] = 0
#             letter_distribution[letter] += 1
#             letter_set.add(letter)
#     print(letter_distribution)

#     def heuristic(guess_word, colours):
#         # print(guess_word)
#         points = 0
#         letter_set = set()
#         # BASED ON THIS COLOUR AND WORD, how can i divie up the search space to a fine degree
#         for letter in guess_word:
#             if letter in letter_set:
#                 continue
#             points += letter_distribution[letter]
#             letter_set.add(letter)
#         return points / len(letter_set)
  
#     # if nth_guess == 1:
#     #     return "salet"

#     guess_points_dict = {}
#     for possible_guess in possible_words:
#         # total_points = 0
#         # for colour in colours_arr:
#         #     total_points += heuristic(possible_guess, colour)
#         total_points = heuristic(possible_guess, "BBBBB")
#         guess_points_dict[possible_guess] = total_points
    
#     if nth_guess <= 2:
#         sorted_dict = sorted(guess_points_dict.items(), key=lambda kv: kv[1])
#         length = len(sorted_dict)
#         return sorted_dict[length // 2][0]
    
#     v = list(guess_points_dict.values())
#     k = list(guess_points_dict.keys())
#     return k[v.index(max(v))]







def generate_smart_guess(word_list, possible_words, nth_guess):
    '''
    Generates a good guess word from the list of possible words.

    Parameters
    ----------
    word_list:
        A list of strings of all words in the word list.
    possible_words:
        A list of strings of all possible remaining words in the word list.
    nth_guess:
        A number indicating how many guesses have been made so far inclusive of this one.
    
    Returns
    -------
        A string of a good guess.
    '''
    # colour_letters = ["B", "Y", "G"]
    # colours_arr = ["B", "Y", "G"]
    # for i in range(4):
    #     temp_array = []
    #     for word in colours_arr:
    #         for letter in colour_letters:
    #             new_word = word + letter
    #             temp_array.append(new_word)
    #     colours_arr = temp_array

    letter_distribution = {}
    for word in possible_words:
        letter_set = set()
        for letter in word:
            if letter in letter_set:
                continue
            if letter not in letter_distribution.keys():
                letter_distribution[letter] = 0
            letter_distribution[letter] += 1
            letter_set.add(letter)
    # print(letter_distribution)

    def heuristic_low(guess_word):
        # print(guess_word)
        points = 0
        letter_set = set()
        # BASED ON THIS COLOUR AND WORD, how can i divie up the search space to a fine degree
        for letter in guess_word:
            if letter in letter_set:
                continue
            points += letter_distribution[letter]
            letter_set.add(letter)
        return points / len(letter_set)

    def heuristic_high(guess_word, potential_answer):
        colours = make_evaluate_guess(potential_answer, word_list)(guess_word)
        # result = filter_available_words(guess_word, colours, possible_words)
        # G = 10, Y = 5, B = 1
        points = 0
        for colour in colours:
            if colour == "G":
                points += 10
            if colour == "Y":
                points += 5
            if colour == "B":
                points += 1
        return points
  
    # if nth_guess == 1:
    #     return "salet"

    guess_points_dict = {}
    if nth_guess <= 2:
        for possible_guess in possible_words:
            # total_points = 0
            # for colour in colours_arr:
            #     total_points += heuristic(possible_guess, colour)
            total_points = heuristic_low(possible_guess)
            guess_points_dict[possible_guess] = total_points
        sorted_dict = sorted(guess_points_dict.items(), key=lambda kv: kv[1])
        length = len(sorted_dict)
        return sorted_dict[length // 2][0]
    
    for possible_guess in possible_words:
        total_points = 0
        for potential_answer in possible_words:
            total_points += heuristic_high(possible_guess, potential_answer)
        guess_points_dict[possible_guess] = total_points

    # if nth_guess <= 2:
    #     sorted_dict = sorted(guess_points_dict.items(), key=lambda kv: kv[1])
    #     length = len(sorted_dict)
    #     return sorted_dict[length // 2][0]
    
    v = list(guess_points_dict.values())
    k = list(guess_points_dict.keys())
    return k[v.index(max(v))]

print(generate_smart_guess(word_list, list_test, 4))

def smart_solver(word_list, evaluate_guess_func, max_guess):
    possible_words = word_list.copy()
    for num in range(max_guess):
        print(f"Try {num}")
        sleep(4)
        guess = generate_smart_guess(word_list, possible_words, num)
        colours = evaluate_guess_func(guess)
        possible_words = filter_available_words(guess, colours, possible_words)
    
    if len(word_list) == 0:
        return "NOT POSSIBLE"
    
    # if len(word_list) > 1:
    #     return "Whats going on"

    return word_list

# cases_game = make_evaluate_guess("cases", word_list)
# print(smart_solver(word_list, cases_game, 5))