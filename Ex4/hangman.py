############################################################
# FILE : hangman.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex4 2020
# DESCRIPTION: Plays a round of hangman
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################
import hangman_helper


def main():
    word_list = hangman_helper.load_words("words.txt")

    games_played = 0
    score = hangman_helper.POINTS_INITIAL

    while score > 0:
        score = run_single_game(word_list, score)
        games_played += 1
        end_of_round_message = "Games played: " + str(games_played) + ". " +\
                               "Current score: " + str(score) + ". " +\
                               "Play Again?"
        if hangman_helper.play_again(end_of_round_message):
            if score == 0:
                games_played = 0
                score = hangman_helper.POINTS_INITIAL
        else:
            break


def run_single_game(words_list, score):
    # Choose a word
    word = hangman_helper.get_random_word(words_list)
    # Initialize pattern, score, and list of wrong guesses
    wrong_guesses = []
    pattern = "_" * len(word)
    message = ""
    # Run round
    while score > 0 and pattern != word:
        pattern, score, prev_guesses, message = \
            run_single_round(words_list, word, pattern, wrong_guesses, score, message)

    if pattern == word:
        hangman_helper.display_state(pattern, wrong_guesses,
                                     score, "You won the game!")
    else:
        hangman_helper.display_state(pattern, wrong_guesses,
                                     score, "You lost. The word was " + word)

    return score


def run_single_round(words_list, word, pattern, wrong_guesses, score, message):
    hangman_helper.display_state(pattern, wrong_guesses, score, message)
    message = ""
    guess_type, guess = hangman_helper.get_input()
    score -= 1

    if guess_type == hangman_helper.LETTER:
        pattern, score, wrong_guesses, message = \
            guessed_a_letter(word, pattern, guess, score,
                             wrong_guesses, message)
    elif guess_type == hangman_helper.WORD:
        pattern, score = guessed_a_word(word, pattern, guess, score)
    elif guess_type == hangman_helper.HINT:
        hangman_helper.show_suggestions(filter_words_list(words_list, pattern,
                                                          wrong_guesses))

    return pattern, score, wrong_guesses, message


def guessed_a_word(word, pattern, guess, score):
    if word == guess:
        score += add_to_score(pattern, word)
        pattern = word
    return pattern, score


def guessed_a_letter(word, pattern, letter, score, wrong_guesses, message):
    if valid_guess(letter):
        if letter in word:
            new_pattern = update_word_pattern(word, pattern, letter)
            if new_pattern != pattern:
                score += add_to_score(pattern, new_pattern)
                pattern = new_pattern
            else:
                message = "This letter was already chosen"
                score += 1
        else:
            if letter in wrong_guesses:
                message = "This letter was already chosen"
                score += 1
            else:
                wrong_guesses.append(letter)

    return pattern, score, wrong_guesses, message


def update_word_pattern(word, pattern, letter):
    """Update the pattern according to guessed letter"""
    # iterate over the characters in word
    for i in range(len(word)):
        # if a character matches the letter, update pattern
        if word[i] == letter:
            pattern = pattern[0:i] + letter + pattern[i+1:]
    return pattern


def valid_guess(guess):
    if len(guess) == 1:
        if 'a' <= guess <= 'z':
            return True
    return False


def letters_revealed(old_pattern, new_pattern):
    changes = 0
    for i in range(len(old_pattern)):
        if old_pattern[i] != new_pattern[i]:
            changes += 1
    return changes


def add_to_score(old_pattern, new_pattern):
    changes = letters_revealed(old_pattern, new_pattern)
    return changes * (changes + 1) // 2


def filter_words_list(words, pattern, wrong_guess_lst):
    hint_lst = []
    for word in words:
        if len(word) == len(pattern):
            add_word = True
            for i in range(len(word)):
                if pattern[i] != "_":
                    if pattern[i] != word[i]:
                        add_word = False
                        break
                if word[i] in wrong_guess_lst:
                    add_word = False
                    break
            if add_word:
                hint_lst.append(word)

    if len(hint_lst) > hangman_helper.HINT_LENGTH:
        new_hint_list = []
        n = len(hint_lst)
        hint_length = hangman_helper.HINT_LENGTH
        for i in range(hint_length):
            new_hint_list.append(hint_lst[i * n // hint_length])
        hint_lst = new_hint_list

    return hint_lst


if __name__ == "__main__" :
    main()