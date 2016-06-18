import random
from model import *
from gameplay import *
from ui import *
from util import *

# Deck
deck = Card.deck_US(start=3, end=13) # Omit Twos and Aces
random.shuffle(deck)

# Hands
human_hand = set(deck[22:])
comp_hand  = set(deck[:22])

# Distribute Twos and Aces equally for fairness
aces = Card.deck_US(start=14, end=14)
twos = Card.deck_US(start=2, end=2)
random.shuffle(aces)
random.shuffle(twos)
human_hand.update(aces[2:])
human_hand.update(twos[2:])
comp_hand.update(aces[:2])
comp_hand.update(twos[:2])

# Decide first turn (True-Human, False-Computer)
turn = False if Card(Suit.Spades, Number.Ace) in comp_hand else True

# Begin game!
logger.info("Game begins")
round_num = 0
while len(human_hand) and len(comp_hand):
    cls()
    round_num += 1
    log(round_num=round_num, turn=turn)
    logger.debug("human_hand:")
    log_hand(human_hand)
    logger.debug("comp_hand:")
    log_hand(comp_hand)
    print_hands(human_hand, comp_hand)
    
    if turn:
        human_choice = get_user_input(human_hand)
        comp_choice = make_counter_move(human_hand, comp_hand, human_choice)
        play_card(comp_choice)
        press_enter()
    else:
        comp_choice = make_move(human_hand, comp_hand)
        play_card(comp_choice)
        human_choice = get_user_input(human_hand, comp_choice.suit)
    
    log(context="driver", human_choice=human_choice, comp_choice=comp_choice)
    turn, human_hand, comp_hand = \
            adjust_hands(turn, human_hand, comp_hand,
                    human_choice, comp_choice)
cls()
print_hands(human_hand, comp_hand)
print "\n%s won the game. Thanks for playing!" \
        % who_won(human_hand, comp_hand)
log(winner=who_won(human_hand, comp_hand))
logger.info("Game ends")

