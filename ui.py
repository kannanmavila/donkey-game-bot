import os
import sys
import time
from model import *
from gameplay import *

# Constants
UNICODE_TAB = u' '*7
LEFT_INDENT = 8
BOTTOM_INDENT = 1
SUIT_LETTERS =   {'s': Suit.Spades,   'h': Suit.Hearts,
                  'd': Suit.Diamonds, 'c': Suit.Clubs}
NUMBER_LETTERS = {'j': Number.Jack,   'q': Number.Queen,
                  'k': Number.King,   'a': Number.Ace}

"""
Clears the screen
"""
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

"""
Prints the current state of the game
"""
def print_hands(human_hand, comp_hand):
    for i in range(0, 15):
        sys.stdout.write(' '*LEFT_INDENT)
        for hand, mask in [(human_hand, False), (comp_hand, False)]:
            for j in range(1, 5):
                if i == 0:
                    sys.stdout.write("%s" % unicode(Suit(j)))
                    sys.stdout.write(UNICODE_TAB)
                    continue
                if i == 1:
                    sys.stdout.write('-')
                    sys.stdout.write('-'*7 if j !=4 else ' '*7)
                    continue
                card = Card(Suit(j), Number(i))
                if mask:
                    sys.stdout.write('#')
                elif card in hand:
                    sys.stdout.write(card.repr_number())
                else:
                    sys.stdout.write('-')
                sys.stdout.write('\t')
                sys.stdout.flush()
            sys.stdout.write('\t\t')
        print ''
    print '\n'*BOTTOM_INDENT

"""
Accepts and parses user input and returns the card
"""
def get_user_input(human_hand, suit=None):
    while True:
        # Parse input
        inp = raw_input("\nYou:  ")
        log(context="get_user_input()", inp=inp)
        try:
            if len(inp) == 0:
                raise KeyError
            inp_suit = SUIT_LETTERS[inp[0].lower()]
        except KeyError as ke:
            error_message = "Valid suites are: S, H, D, and C"
            print error_message
            logger.error(error_message)
            continue
        
        inp_number = inp[1:]
        if inp_number.lower() in NUMBER_LETTERS:
            inp_number = NUMBER_LETTERS[inp_number.lower()]
        else:
            try:
                inp_number = int(inp_number)
                if not 2 <= inp_number <= 10:
                    raise ValueError
                inp_number = Number(inp_number)
            except ValueError as ve:
                error_message = "Valid values are: J, Q, K, A and 2-10"
                print error_message
                logger.error(error_message)
                continue
        
        card = Card(inp_suit, inp_number)
        
        # Check if card belongs to the human
        if card not in human_hand:
            error_message = "You do not possess that card"
            print error_message
            logger.error(error_message)
            continue
        
        # Check if card belongs to the same suit
        if suit is not None:
            if card.suit != suit \
                    and suit in [c.suit for c in human_hand]:
                error_message = "You must choose a card of %s" % suit.name
                print error_message
                logger.error(error_message)
                continue
        
        break
    return card

"""
Prints the computer's choice
"""
def play_card(card):
    [suit, ] = [key for key in SUIT_LETTERS
                if SUIT_LETTERS[key] == card.suit]
    if 2 <= card.number.value <= 10:
        number = card.number.value
    else:
        [number, ] = [key for key in NUMBER_LETTERS
                      if NUMBER_LETTERS[key] == card.number]
    sys.stdout.write("Comp: %s%s" % (unicode(card.suit), number))
    sys.stdout.flush()

"""
"Press enter to continue"
"""
def press_enter():
    raw_input("\n\nPress ENTER to continue")

