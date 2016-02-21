# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message = ''

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand 'Hand contains '
        sHand = 'Hand contains'
        if len(self.hand) > 0:
            for i in range(len(self.hand)):
                sHand += ' ' + self.hand[i].get_suit() + self.hand[i].get_rank()
        return sHand

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        ace = 0
        for i in range(len(self.hand)):
            total += VALUES[self.hand[i].get_rank()]
            if self.hand[i].get_rank() == 'A':
                ace += 1
        if ace >= 1 and total <= 11:
            total += 10
        return total
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            self.hand[i].draw(canvas, [pos[0] + i * (CARD_SIZE[0] + 9), pos[1]]) 

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []       
        for s in SUITS:
            for r in RANKS:
                card = Card(s, r)
                self.deck.append(card)
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        t = self.deck[-1]
        self.deck.pop()
        return t
    
    def __str__(self):
        # return a string representing the deck
        sDeck = 'Deck contains'
        if len(self.deck) > 0:
            for i in range(len(self.deck)):
                sDeck += ' ' + self.deck[i].get_suit() + self.deck[i].get_rank()
        return sDeck

#define event handlers for buttons
def deal():
    global outcome, score, message, in_play, d_in_play, player_hand, dealer_hand
    if in_play:
        message = 'You lose. Press the Deal again.'
        outcome = 'New deal?'
        score -= 1
        in_play = False
        print message
        print outcome
        print score
    else:
        in_play = True
        d_in_play = Deck()
        d_in_play.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        outcome = ''
        message = ''

        print d_in_play    

        for i in range(2):
            player_hand.add_card(d_in_play.deal_card())
            dealer_hand.add_card(d_in_play.deal_card())           
        outcome  = 'Hit or Stand?'

#        print d_in_play
        print 'Player', player_hand
        print 'Dealer', dealer_hand
        print 'Player value', player_hand.get_value()
        print outcome

def hit():
    global in_play, outcome
    # if the hand is in play, hit the player
    if player_hand.get_value() < 21 and in_play:
        player_hand.add_card(d_in_play.deal_card())   
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = 'You have busted'
    
#    print d_in_play
    print 'Player', player_hand
    print 'Player value', player_hand.get_value()
    print outcome
        
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, message, score, in_play
    
#    print d_in_play
    print 'Dealer', dealer_hand
    print 'Dealer', dealer_hand.get_value()
    
    if in_play and outcome != 'You have busted':
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(d_in_play.deal_card())
            
            print d_in_play
            print 'Dealer', dealer_hand
            print 'Dealer', dealer_hand.get_value()
    
    # assign a message to outcome, update in_play and score
    
    if outcome == 'You have busted' or (dealer_hand.get_value() >= player_hand.get_value() 
                    and dealer_hand.get_value() <= 21) and in_play:
        message = 'You lose.'
        if outcome == 'You have busted':
            message = outcome + '. ' + message
        outcome = 'New deal?'
        score -= 1
    elif in_play:
        message = 'You win.'
        if dealer_hand.get_value() > 21:
            message = 'I have busted. ' + message
        outcome = 'New deal?'
        score += 1
    in_play = False
    
    print message
    print outcome
    print score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BlackJack', (100, 100), 48, 'Blue')
    canvas.draw_text('Score ' + str(score), (450, 100), 32, 'Maroon')
    
    canvas.draw_text('Player' + '               ' + outcome, (100, 380), 18, 'Black')
    player_hand.draw(canvas, [100, 400])
        
    canvas.draw_text('Dealer' + '               ' + message, (100, 180), 18, 'Black')
    dealer_hand.draw(canvas, [100, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
# Grading rubric - 18 pts total (scaled to 100)

# 1 pt - The program opens a frame with the title "Blackjack" appearing on the canvas.
# 3 pts - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area. (1 pt per button)
# 2 pts - The program graphically displays the player's hand using card sprites. 
#		(1 pt if text is displayed in the console instead) 
# 2 pts - The program graphically displays the dealer's hand using card sprites. 
#		Displaying both of the dealer's cards face up is allowable when evaluating this bullet. 
#		(1 pt if text displayed in the console instead)
# 1 pt - Hitting the "Deal" button deals out new hands to the player and dealer.
# 1 pt - Hitting the "Hit" button deals another card to the player. 
# 1 pt - Hitting the "Stand" button deals cards to the dealer as necessary.
# 1 pt - The program correctly recognizes the player busting. 
# 1 pt - The program correctly recognizes the dealer busting. 
# 1 pt - The program correctly computes hand values and declares a winner. 
#		Evalute based on player/dealer winner messages. 
# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with the messages 
#        "Hit or stand?" and "New deal?". (1 pt per message)
# 1 pt - The program keeps score correctly.