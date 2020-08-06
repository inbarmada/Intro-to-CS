############################################################
# FILE : hangman.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse Ex4 2020
# DESCRIPTION: Plays a game of hangman until player stops
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES:
############################################################
import hangman_helper

# Define all messages as constants
REPEAT_LETTER_MESSAGE = "This letter was already chosen"
INVALID_LETTER_MESSAGE = "This is not a valid letter"
PLAY_AGAIN_MESSAGE = "Play Again?"
NEW_SERIES_MESSAGE = "Start a new series of games?"
GAME_WON_MESSAGE = "You won the game!"
GAME_LOST_MESSAGE = "You lost. The word was "
GAMES_PLAYED_MESSAGE = "Games played: "
CURRENT_SCORE_MESSAGE = ". Current score: "


def main():
    """ Run games and keep score until player decides to stop """
    # Load list of words from file and initialize games stats
    word_list = hangman_helper.load_words("words.txt")
    games_played = 0
    score = hangman_helper.POINTS_INITIAL

    # Keep playing until player stops
    while score > 0:
        # Run a single round
        score = run_single_game(word_list, score)
        games_played += 1

        # Write end-of-round message
        end_of_round_message = GAMES_PLAYED_MESSAGE + str(games_played) + \
            CURRENT_SCORE_MESSAGE + str(score) + ". "
        end_of_round_message += PLAY_AGAIN_MESSAGE if score > 0 \
            else NEW_SERIES_MESSAGE

        # Ask player whether to continue
        if hangman_helper.play_again(end_of_round_message):
            # If player lost but wants to continue reset game stats
            if score == 0:
                games_played = 0
                score = hangman_helper.POINTS_INITIAL
        else:
            break


def run_single_game(words_list, score):
    """ Run a single game until player guesses the word or loses"""
    # Choose a word
    word = hangman_helper.get_random_word(words_list)
    # Initialize pattern, score, and list of wrong guesses
    wrong_guesses = []
    pattern = "_" * len(word)
    message = ""

    # Run rounds until player guesses word or loses
    while score > 0 and pattern != word:
        # Run a round
        round_stats = run_single_round(words_list, word, pattern,
                                       wrong_guesses, score, message)
        # Update game variables
        pattern, score, prev_guesses, message = round_stats

    # Game outcome: game won
    if pattern == word:
        hangman_helper.display_state(pattern, wrong_guesses,
                                     score, GAME_WON_MESSAGE)
    # Game outcome: game lost
    else:
        hangman_helper.display_state(pattern, wrong_guesses,
                                     score, GAME_LOST_MESSAGE + word)
    return score


def run_single_round(words_list, word, pattern, wrong_guesses, score, message):
    """ Run a single round - one guess and its outcome """
    # Display games stats and message and reset message
    hangman_helper.display_state(pattern, wrong_guesses, score, message)
    message = ""

    # Get player input
    guess_type, guess = hangman_helper.get_input()
    score -= 1

    # Input is a letter
    if guess_type == hangman_helper.LETTER:
        round_stats = guessed_a_letter(word, pattern, guess, score,
                                       wrong_guesses, message)
        pattern, score, wrong_guesses, message = round_stats

    # Input is a word
    elif guess_type == hangman_helper.WORD:
        pattern, score = guessed_a_word(word, pattern, guess, score)

    # Input is a hint
    elif guess_type == hangman_helper.HINT:
        hangman_helper.show_suggestions(filter_words_list(words_list, pattern,
                                                          wrong_guesses))

    return pattern, score, wrong_guesses, message


def guessed_a_word(word, pattern, guess, score):
    """ Check if word guess was right and update score """
    if word == guess:
        score += add_to_score(pattern, word)
        pattern = word
    return pattern, score


def guessed_a_letter(word, pattern, letter, score, wrong_guesses, message):
    """ Check if a letter is correct and update score"""
    # Check if guess is a lower case letter
    if valid_guess(letter):
        # Letter was already guessed
        if letter in pattern or letter in wrong_guesses:
            message = REPEAT_LETTER_MESSAGE
            score += 1

        # Check if guess appears in word
        elif letter in word:
            new_pattern = update_word_pattern(word, pattern, letter)
            score += add_to_score(pattern, new_pattern)
            pattern = new_pattern

        # Guess is not in word
        else:
            wrong_guesses.append(letter)

    # Invalid guess
    else:
        score += 1
        message = INVALID_LETTER_MESSAGE

    return pattern, score, wrong_guesses, message


def update_word_pattern(word, pattern, letter):
    """Update the pattern according to guessed letter"""
    # iterate over the characters in word
    for i in range(len(word)):
        # if a character matches the letter, update pattern
        if word[i] == letter:
            pattern = pattern[0:i] + letter + pattern[i + 1:]
    return pattern


def valid_guess(guess):
    """ Check if guess is a lower case letter """
    if len(guess) == 1:
        if 'a' <= guess <= 'z':
            return True
    return False


def letters_revealed(old_pattern, new_pattern):
    """ Find how many new letters were revealed """
    changes = 0
    for i in range(len(old_pattern)):
        if old_pattern[i] != new_pattern[i]:
            changes += 1
    return changes


def add_to_score(old_pattern, new_pattern):
    """ Add to score based on the number of letters revealed """
    changes = letters_revealed(old_pattern, new_pattern)
    return changes * (changes + 1) // 2


def filter_words_list(words, pattern, wrong_guess_lst):
    """ Find hints - words that can match pattern """
    hint_lst = []
    # Iterate through every word in list
    for word in words:
        # Length of word matches pattern
        if len(word) == len(pattern):
            if check_hint_word(word, pattern, wrong_guess_lst):
                hint_lst.append(word)

    # If hint list is too long, cut it to hint_length
    if len(hint_lst) > hangman_helper.HINT_LENGTH:
        hint_lst = cut_hint_list(hint_lst)

    return hint_lst


def check_hint_word(word, pattern, wrong_guess_lst):
    """ Check if word can work as a hint """
    # Check every letter in word
    for i in range(len(word)):
        # If letter doesn't match pattern, break
        if pattern[i] != "_" and pattern[i] != word[i]:
            return False
        # Word contains letters from wrong guess list
        elif word[i] in wrong_guess_lst:
            return False
        # Letter is in word more times than in pattern
        elif word[i] in pattern and word[i] != pattern[i]:
            return False
    # Hint works
    else:
        return True


def cut_hint_list(hint_lst):
    """ If hint list is too long, cut it down """
    new_hint_list = []
    n = len(hint_lst)
    hint_length = hangman_helper.HINT_LENGTH
    for i in range(hint_length):
        new_hint_list.append(hint_lst[i * n // hint_length])
    hint_lst = new_hint_list
    return hint_lst


if __name__ == "__main__":
    main()
