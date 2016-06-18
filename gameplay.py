import types
from model import *
from util import *

"""
Makes a first move
"""
def make_move(human_hand, comp_hand):
    human_suits = set([c.suit for c in human_hand])
    comp_suits = set([c.suit for c in comp_hand])
    human_comp_suits = human_suits & comp_suits
    bad_suits = [s for s in human_comp_suits
                 if min(_get_suit(comp_hand, s)) > \
                    min(_get_suit(human_hand, s))]
    bad_suits_adv = [s for s in bad_suits
                     if max(_get_suit(comp_hand, s)) > \
                        max(_get_suit(human_hand, s))]
    human_clashworthy_suits = _get_clashworthy_suits(human_hand, comp_hand,
            lambda x,y: x>=y)
    log(context="make_move(): variables", human_suits=human_suits,
            comp_suits=comp_suits, human_comp_suits=human_comp_suits,
            bad_suits=bad_suits, bad_suits_adv=bad_suits_adv,
            human_clashworthy_suits=human_clashworthy_suits)
    
    if not human_comp_suits:
        log(move="1.1", state="Negative: Definite loss")
        return max(comp_hand)
    else:
        if bad_suits:
            if bad_suits_adv:
                log(move="1.2.1.1", state="Positive")
                return max(_get_suit(comp_hand, bad_suits_adv))
            elif not human_clashworthy_suits and (comp_suits - human_suits):
                log(move="1.2.1.2", state="Positive/Neutral")
                return max(_get_suit(comp_hand, comp_suits - human_suits))
            else:
                log(move="1.2.1.3", state="Neutral")
                return _get_second_min(comp_hand, bad_suits)
        else:
            if len(_get_suit(human_hand, human_comp_suits)) == 1:
                log(move="1.2.2.1", state="Positive: Definite win")
                return min(_get_suit(comp_hand, human_comp_suits))
            else:
                log(move="1.2.2.2", state="Positive: Definite win")
                return max(_get_suit(comp_hand, human_comp_suits))
    logger.error("No card selected by make_move()")

"""
Counters a move made by the human
"""
def make_counter_move(human_hand, comp_hand, human_choice):
    human_suits = set([c.suit for c in human_hand])
    comp_suits = set([c.suit for c in comp_hand])
    human_comp_suits = human_suits & comp_suits
    comp_clashworthy_suits = _get_clashworthy_suits(comp_hand, human_hand,
            lambda x,y: x>y)
    comp_clashable_suits = _get_clashworthy_suits(comp_hand, human_hand,
            lambda x,y: x==y)
    full_suit = _get_suit(comp_hand, human_choice.suit)
    log(context="make_counter_move(): variables", human_suits=human_suits,
            comp_suits=comp_suits, human_comp_suits=human_comp_suits,
            comp_clashworthy_suits=comp_clashworthy_suits,
            comp_clashable_suits=comp_clashable_suits
            )
    
    if full_suit:
        if len(_get_suit(human_hand, human_comp_suits)) == 1:
            log(move="2.1.1", state="Positive: Definite win")
            return min(_get_suit(comp_hand, human_comp_suits))
        if max(full_suit) > human_choice:
            log(move="2.1.2", state="Positive")
            return min([c for c in full_suit if c > human_choice])
        else:
            log(move="2.1.3", state="Neutral")
            return _get_second_min(comp_hand, human_choice.suit)
    else:
        if not human_comp_suits:
            log(move="2.2.1", state="Positive: Definite win")
            return max(comp_hand)
        elif comp_clashworthy_suits:
            log(move="2.2.2", state="Positive")
            return _get_second_min(comp_hand, comp_clashworthy_suits)
        elif comp_clashable_suits:
            log(move="2.2.3", state="Neutral")
            return _get_second_min(comp_hand, comp_clashable_suits)
        else:
            log(move="2.2.4", state="Negative")
            return _get_second_min(comp_hand, comp_suits)
    logger.error("No card selected by make_counter_move()")

"""
Adjusts the hands after each round, and decides the turns
"""
def adjust_hands(turn, human_hand, comp_hand, human_choice, comp_choice):
    human_hand.remove(human_choice)
    comp_hand.remove(comp_choice)
    
    if human_choice.suit != comp_choice.suit:
        this_round = set([human_choice, comp_choice])
        log(context="adjust_hands(): clash!")
        if turn:
            human_hand.update(this_round)
        else:
            comp_hand.update(this_round)
    else:
        turn = human_choice.number.value > comp_choice.number.value
    
    return turn, human_hand, comp_hand

"""
Decides the winner, once the game ends
"""
def who_won(human_hand, comp_hand):
    if len(human_hand) == 0:
        return "You"
    elif len(comp_hand) == 0:
        return "The computer"
    else:
        error_message = "Cannot decide the winner until the game ends"
        logger.error(error_message)
        raise Exception(error_message)

"""
Returns suits that `first` would prefer to clash `second` with.
`comparator` decides how the card counts of first and second
should compare to make the clash "worthwhile"
"""
def _get_clashworthy_suits(first, second, comparator):
    return [s for s in list(Suit)
            if _get_suit(first, s) and _get_suit(second, s)
            and
            (
                (min(_get_suit(first, s)) > min(_get_suit(second, s))
                        and comparator(len(_get_suit(second, s)) -
                        len(_get_suit(first, s)), 1))
                or
                (min(_get_suit(first, s)) < min(_get_suit(second, s))
                        and comparator(len(_get_suit(first, s)) -
                        len(_get_suit(second, s)), 1))
            )]

"""
Gets all cards in a hand, belonging to a particular suit/set of suits
"""
def _get_suit(hand, suit):
    cards = set()
    if type(suit) is list or type(suit) is set:
        for s in suit:
            cards |= _get_suit(hand, s)
    else:
        cards = set([card for card in hand
                     if card.suit == suit])
    return cards

"""
Returns the second smallest card in a deck,
or the smallest card if there is only one"""
def _get_second_min(hand, suit):
    cards = set()
    if type(suit) is list or type(suit) is set:
        for s in suit:
            min_set = [c for c in _get_suit(hand, s)
                       if c > min(_get_suit(hand, s))]
            if len(min_set) != 0:
                cards |= set([min(min_set)])
        if len(cards) == 0:
            for s in suit:
                cards |= set([min(_get_suit(hand, s))])
    else:
        min_set = [c for c in _get_suit(hand, suit)
                   if c > min(_get_suit(hand, suit))]
        if len(min_set) != 0:
            cards = set([min(min_set)])
        if len(cards) == 0:
            cards = set([min(_get_suit(hand, suit))])
    card = cards.pop()
    return card

