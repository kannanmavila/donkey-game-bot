import logging

# Logger setup
logger = logging.getLogger('donkey-log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gameplay.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - ' + \
                              '%(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

"""
Lets you log multiple variables easily
"""
def log(**var_tuple):
    logger.debug("----")
    for key, value in var_tuple.iteritems():
        logger.debug("%s = %s" % (key, value))
    logger.debug("----")

"""
Pretty prints (logs) a hand
"""
def log_hand(hand):
    suits = set([c.suit for c in hand])
    for s in sorted(suits, key = lambda x: x.value):
        full_suit = [c for c in hand if c.suit == s]
        if full_suit:
            suit_str = ''
            for c in sorted(full_suit):
                suit_str += unicode(c.suit) + str(c.number.value) + " "
            logger.debug(suit_str)

