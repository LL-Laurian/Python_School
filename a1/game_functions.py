"""CSCA08: Fall 2022 -- Assignment 1: What's that Phrase?

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020-2022 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.

"""

from constants import (POINTS_PER_GUESS, COST_OF_VOWEL, BONUS_POINTS,
                       PLAYER_ONE, PLAYER_TWO, GUESS, BUY, SOLVE,
                       QUIT, SINGLE_PLAYER, PVP, PVE, EASY, HARD,
                       ALL_CONSONANTS, ALL_VOWELS,
                       PRIORITY_CONSONANTS, MYSTERY_CHAR)


# This function is provided as an example.
def winning(mystery_phrase: str, view: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination. That is, if and only if mystery_phrase and view are
    the same.

    >>> winning('banana', 'banana')
    True
    >>> winning('apple', 'a^^le')
    False
    >>> winning('apple', 'app')
    False
    """

    return mystery_phrase == view


# This function is partially provided as an example of calling another
# function as helper.
def game_over(mystery_phrase: str, view: str, move: str) -> bool:
    """Return True if and only if mystery_phrase and view are a winning
    combination or move is QUIT.

    Precondition: current view view is valid for the mystery phrase. move is
    GUESS, SOLVE, BUY or QUIT.

    >>> game_over('apple','a^^le','GUESS')
    False
    >>> game_over('banana','banana','BUY')
    True
    >>> game_over('apple','app','QUIT')
    True
    >>> game_over('apple','apple','QUIT')
    True
    """

    return winning(mystery_phrase, view) or move == 'QUIT'


def one_player(game_type: str) -> bool:
    """Return True if and only if game type game_type is a one-player game.

    Precondition: game_type is SINGLE_PLAYER, PVP, or PVE.

    >>> one_player('SP')
    True
    >>> one_player('PVP')
    False
    >>> one_player('PVE')
    False
    """

    return game_type == SINGLE_PLAYER


# This function is partially provided as an example of using constants
# in the docstring description and specific values in docstring
# examples.
def is_player(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human player
    in a game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is SINGLE_PLAYER, PVP, or PVE.

    In a SINGLE_PLAYER game or a PVP game, a player is always a human
    player. In a PVE game, PLAYER_ONE is a human player and PLAYER_TWO
    is the environment.

    Precondition: current_player is valid and game_type is valid.

    >>> is_player('Player One', 'SP')
    True
    >>> is_player('Player Two', 'PVE')
    False
    >>> is_player('Player Two','PVP')
    True
    """

    if game_type == PVE:
        return current_player == PLAYER_ONE
    return True


def current_player_score(player_one_score: int, player_two_score: int,
                         current_player: str) -> int:
    """Return the score of current player current_player corresponding to
    player_one_score for player one and player_two_score for player two.

    Precondition: current_player is PLAYER_ONE or PLAYER_TWO.

    >>> current_player_score(1,2,PLAYER_ONE)
    1
    >>> current_player_score(1,2,PLAYER_TWO)
    2
    """

    if current_player == PLAYER_ONE:
        return player_one_score
    return player_two_score


def adds_points(letter: str, mystery_phrase: str, view: str) -> bool:
    """Return True if and only if the letter letter is in mystery phrase
    mystery_phrase but not in current view view and the letter letter is a
    consonant.

    Precondition: view is valid for mystery_phrase.
    letter is a one-character-long string.

    >>> adds_points('p', 'apple', 'a^^^^')
    True
    >>> adds_points('z', 'better', 'b^tt^r')
    False
    >>> adds_points('p', 'apple', 'app^^')
    False
    >>> adds_points('e', 'better', 'b^^^^^')
    False
    """

    if letter in mystery_phrase and letter in ALL_CONSONANTS:
        return letter not in view
    return False


def update_view(mystery_phrase: str, view: str, index: int, guess: str) -> str:
    """Return guess if guessed letter guess is in mystery phrase
    mystery_phrase. Otherwise, return character at index index of current view
    view.

    Precondition: view and index are valid for mystery_phrase.
    guess is a one-character-long string.

    >>> update_view('apple', '^^^^^', 0, 'a')
    'a'
    >>> update_view('better','b^^^^^',2, 'z')
    '^'
    >>> update_view('better','b^^^^^',0, 'b')
    'b'
    >>> update_view('better','b^^^^^',0, 'z')
    'b'
    >>> update_view('better', 'b^^^^^',2, 't' )
    't'
    """

    if mystery_phrase[index] == guess:
        return guess
    return view[index]


def compute_score(current_score: int, num_occurrence: int, move: str) -> int:
    """Return the final score by adding current score current_score to the
    number of revealed occurrences num_occurrence or decreasing current score
    current_score, depending on player's current move move.

    Precondition: move is GUESS or BUY.
    current_score >= 0
    current_score >= 1 if move is BUY
    num_occurrence is valid for mystery_phrase.
    num_occurrence >= 0

    >>> compute_score(0, 1, GUESS)
    1
    >>> compute_score(3, 2, GUESS)
    5
    >>> compute_score(3, 0, GUESS)
    3
    >>> compute_score(2, 2, BUY)
    1
    """

    if move == BUY:
        return current_score - COST_OF_VOWEL
    return current_score + POINTS_PER_GUESS * num_occurrence


def next_turn(current_player: str, num_occurrence: int, game_type: str) -> str:
    """Return current player current_player if game type is a single player
    game or the number of occurrences revealed num_occurrence is not zero;
    otherwise, return the other player other than the current player
    current_player.

    Precondition: current_player is PLAYER_ONE or PLAYER_TWO.
    num_occurrence >= 0
    game_type is SINGLE_PLAYER, PVP, or PVE.

    >>> next_turn(PLAYER_ONE, 0, SINGLE_PLAYER)
    'Player One'
    >>> next_turn(PLAYER_ONE, 1, SINGLE_PLAYER)
    'Player One'
    >>> next_turn(PLAYER_ONE, 0, PVP)
    'Player Two'
    >>> next_turn(PLAYER_TWO, 1, PVP)
    'Player Two'
    >>> next_turn(PLAYER_ONE, 1, PVE)
    'Player One'
    >>> next_turn(PLAYER_ONE, 0, PVE)
    'Player Two'
    """

    if game_type == SINGLE_PLAYER or num_occurrence > 0:
        return current_player
    if current_player == PLAYER_ONE:
        return PLAYER_TWO
    return PLAYER_ONE


def is_mystery_char(index: int, mystery_phrase: str, view: str) -> bool:
    """Return True if and only if the character at index of mystery_phrase
    is currently displayed as a mystery character in view.

    Precondition: index is valid for mystery_phrase.
    index >= 0

    >>> is_mystery_char(4, 'apple', '^^^^e')
    False
    >>> is_mystery_char(0, 'apple', '^^^^^')
    True
    """

    return mystery_phrase[index] != view[index] and view[index] == MYSTERY_CHAR


def half_solved(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_solved('')
    True
    >>> half_solved('x')
    True
    >>> half_solved('^')
    False
    >>> half_solved('a^,^c!')
    True
    >>> half_solved('a^b^^e ^c^d^^d')
    False
    """

    num_mystery_chars = view.count(MYSTERY_CHAR)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_mystery_chars


def environment_solves(view: str, dif: str, unguess_consonant: str) -> bool:
    """Return True if and only if unguessed consonants unguess_consonant of
    view is empty or when dif is HARD, at least half view is revealed.

    Precondition: dif is EASY or HARD. unguess_consonant is in ALL_CONSONANTS.
    unguess_consonant is valid for mystery_phrase.

    >>> environment_solves('a^^^^', EASY, 'pl')
    False
    >>> environment_solves('appl^', EASY, '')
    True
    >>> environment_solves('appl^', HARD, '')
    True
    >>> environment_solves('app^^^^', HARD, '')
    True
    >>> environment_solves('giant ^^^^^', HARD, 'ct')
    True
    >>> environment_solves('g^^^t ^ct^^^', HARD, 'n')
    False
    """

    if dif == EASY:
        return unguess_consonant == ''
    return unguess_consonant == '' or half_solved(view)


def delete(letters: str, index: int) -> str:
    """Return the string of letters letters with character at given index index
    deleted, if index index is valid. Otherwise, return the original string of
    letters letters.
    Precondition: index >= 0

    >>> delete('abcdef', 2)
    'abdef'
    >>> delete('abcdef', 7)
    'abcdef'
    >>> delete('abcdef',0)
    'bcdef'
    >>> delete('abcdef',5)
    'abcde'
    """

    if 0 < index < len(letters) - 1:
        return letters[0:index] + letters[index + 1:]
    if index == 0:
        return letters[1:]
    if index == len(letters) - 1:
        return letters[:-1]
    return letters


if __name__ == '__main__':
    import doctest

    doctest.testmod()
