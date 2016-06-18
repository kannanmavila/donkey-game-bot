# encoding=utf8

import sys
from enum import Enum
from functools import total_ordering

# Constants
SUIT_SYMBOLS = (u'♠',u'♥', u'♦',u'♣')


"""
The four suits
"""
class Suit(Enum):
    Spades = 1
    Hearts = 2
    Diamonds = 3
    Clubs = 4
    
    def __unicode__(self):
        return SUIT_SYMBOLS[self.value-1]


"""
The 13 numbers
"""
class Number(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14


"""
A playing card
"""
@total_ordering
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    
    def __hash__(self):
        return hash(self.suit.value*100 + self.number.value)
        
    def __eq__(self, other):
        return (self.suit == other.suit and self.number == other.number)
        
    def __lt__(self, other):
        return (self.suit.value*100 + self.number.value <
                other.suit.value*100 + other.number.value)
    
    def repr_number(self):
        str_repr = ''
        str_repr += str(self.number.value if self.number.value <= 10 \
                        else ['J', 'Q', 'K', 'A'][self.number.value-11])
        return str_repr
    
    def __repr__(self):
        str_repr = self.suit.name[0]
        str_repr += str(self.number.value if self.number.value <= 10 \
                        else ['J', 'Q', 'K', 'A'][self.number.value-11])
        return str_repr
        
    @classmethod
    def deck_US(self, start=2, end=14):
        deck = []
        for i in range(1, 5):
            for j in range(start, end+1):
                deck.append(Card(Suit(i), Number(j)))
        return deck


