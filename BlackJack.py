# Blackjack

import simplegui
import random
import math

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize global variables
in_play = False
outcome = ""
play_again = ""
bet = ""
game_over = ""
score = 50
total_money = 10000
broke = False
win = False
double = False

spin_count = 90
spin_speed = 2
draw_position = CARD_SIZE
has_spun = False

display = False
rules1 = ""
rules2 = ""
rules3 = ""
rules4 = ""
rules5 = ""
rules6 = ""
rules7 = ""
rules8 = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# card class
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
        global spin_count, has_spun

        spin_count = (spin_count % 360) + spin_speed
        draw_width = CARD_SIZE[0] * math.sin(math.radians(spin_count))
        if has_spun:    
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], 
                        pos[1] + CARD_CENTER[1]], CARD_SIZE)
        elif spin_count < 180 and not(has_spun):  
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], 
                        pos[1] + CARD_CENTER[1]], (draw_width, CARD_SIZE[1]))   
        else:
            draw_width = math.fabs(draw_width)
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], 
                        pos[1] + CARD_CENTER[1]], (draw_width, CARD_SIZE[1]))
            if spin_count == 270:
                has_spun = True
                
# hand class
class Hand:
    def __init__(self):
        self.card = []
        
    def __str__(self):
        return "Hand contains " + ' '.join(map(str, self.card))	
    
    def add_card(self, card):
        self.card.append(card)
        
    def get_value(self):
        self.hand_value = []
        for i in self.card:
            self.hand_value.append(VALUES[i.get_rank()])
        if 1 not in self.hand_value:
            return sum(self.hand_value)
        else:
            if sum(self.hand_value) + 10 <= 21:
                return sum(self.hand_value) + 10
            else:
                return sum(self.hand_value)
            
    def draw(self, canvas, pos):
        for i in self.card:
            i.draw(canvas, (pos[0], pos[1]))
            pos[0] += 100
            
# deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(i, j) for i in SUITS for j in RANKS] 

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(random.randint(0,len(self.cards)-1))
    
    def __str__(self):
        return "Deck contains " + ' '.join(map(str, self.cards))	

# event handlers for gameplay
def bankrupt_check():
    global game_over, bet, total_money, broke
    
    if int(total_money) <= 0:
        broke = True
        game_over = "Game Over, Please Restart"
        bet = ""
            
def win_check():
    global total_money, my_hand, dealer_hand, score, win, double
      
    bankrupt_check()
    if my_hand.get_value() <= 21 and (my_hand.get_value() > dealer_hand.get_value() or dealer_hand.get_value() > 21):
        if double:
            total_money += (2 * int(score))  
        else:
            total_money += int(score)
        win = True
    else:
        if double:
            total_money -= int(score)
        win = False
    
def print_details():
    global play_again, bet, outcome, broke, my_hand, in_play
    
    in_play = False
    bet = "To change bet amount, enter new amount and press Enter"                
    if not(broke) and my_hand.get_value() <= 21:
        play_again = "Play again?"
        if win:
            outcome = "Player wins"
        else:
            outcome = "Dealer wins"
    else:
            outcome ="You went bust"
        
def blackjack_check():
    global my_hand, win, total_money, score
    
    if my_hand.get_value() == 21:
        win = True
        total_money += int(score)
        print_details()
        
# event handlers for buttons
def display_rules():
    global display, rules1, rules2, rules3, rules4
    global rules5, rules6, rules7, rules8
    
    if not(display):
        display = True
        rules1 = "Your goal is to beat the dealer at cards."
        rules2 = "To win you must have a higher card value"
        rules3 = "or for the dealer to bust. busting is any"
        rules4 = "card value over 21. The dealer must hit"
        rules5 = "below 16 and must stand above 16."
        rules6 = "Hit = get a new card"
        rules7 = "Stand = keep current cards"
        rules8 = "Double Down = get only one card, and double bet"
    else:
        display = False
        rules1 = ""
        rules2 = ""
        rules3 = ""
        rules4 = ""
        rules5 = ""
        rules6 = ""
        rules7 = ""
        rules8 = ""
        
def reset():
    global in_play, outcome, play_again, bet, game_over, score, total_money
    global broke, win, double
    
    in_play = False
    outcome = ""
    play_again = ""
    bet = ""
    game_over = ""
    score = 50
    total_money = 10000
    broke = False
    win = False
    double = False
    deal()
    
def deal():
    global broke, game_over, bet, outcome, in_play, my_deck, my_hand
    global dealer_hand, score, total_money, has_spun, spin_count, play_again, double

    if broke == False and int(total_money) >= int(score):
        has_spun = False
        double = False
        spin_count = 90
        outcome = "Hit, Stand, or Double Down?"
        bet = ""
        my_deck = Deck()
        my_deck.shuffle()
        my_hand = Hand()
        dealer_hand = Hand()
        my_hand.add_card(my_deck.deal_card())
        my_hand.add_card(my_deck.deal_card())
        dealer_hand.add_card(my_deck.deal_card())
        dealer_hand.add_card(my_deck.deal_card())
        in_play = True
        blackjack_check()
        if in_play:
            total_money -= int(score)
            if int(total_money) <= 0:
                broke = True
                game_over = "Game Over, Please Restart"
                outcome = "Game Over"
                play_again = "Play again?"
            else:
                outcome = "Hit or Stand?"
    elif int(score) > int(total_money):
        outcome = "Not enough money. Enter a valid bet amount"
  
def hit():
    global in_play, outcome, broke, my_deck, my_hand
    
    if in_play and not(broke):
        outcome = "Hit or Stand?"
        if my_hand.get_value() <= 21:
            my_hand.add_card(my_deck.deal_card())
            if my_hand.get_value() > 21:
                win_check()
                print_details()
                    
def stand():
    global in_play, broke, my_deck, dealer_hand
    
    if in_play and not(broke):
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
        win_check()
        print_details()
        
def double_down():
    global game_over, bet, score, total_money, in_play, outcome, play_again, broke, my_deck, my_hand, dealer_hand, double
    
    if my_hand.get_value() <= 21:
        double = True
        if total_money >= score:
            my_hand.add_card(my_deck.deal_card())
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(my_deck.deal_card())
            win_check()
            print_details()
        else:
           outcome = "Hit or Stand? Not enough money to Double Down" 
        
# bet handler           
def input_handler(x):
    global score, outcome, total_money, play_again
    
    if in_play:
        outcome = "You must wait to bet. You can only Hit, Double Down, or Stand?"
    elif x.isdigit():
        if int(x) > 0 and int(x) <= total_money:
            score = x
            outcome = "Press Deal"
            play_again = ""
        else:
            outcome = "That is not a valid bet"
    else:
        outcome = "That is not a valid bet"
            
# draw handler    
def draw(canvas):
    my_hand, dealer_hand, in_play, card_back, has_spun, broke
    
    if broke or not(in_play):
        canvas.draw_text(play_again, (140, 370), 20, 'Yellow')
        canvas.draw_text(str(dealer_hand.get_value()), (100, 193), 20, 'Yellow')
        canvas.draw_text(str(my_hand.get_value()), (100, 395), 20, 'Yellow')
    canvas.draw_text(str(outcome), (140, 350), 20, 'Blue')
    canvas.draw_text("Blackjack", (300, 90), 50, 'Black')
    canvas.draw_text(str(game_over), (25, 150), 50, 'Red')
    canvas.draw_text("You", (10, 400), 30, 'Black')
    canvas.draw_text("Dealer", (10, 200), 30, 'Black')
    canvas.draw_text("Bet Amount = " + str(score), (10, 40), 20, 'Blue')
    canvas.draw_text("Total Money = " + str(total_money), 
                     (10, 20), 20, 'Blue')
    canvas.draw_text(bet, (300, 20), 20, 'Yellow')
    canvas.draw_text(rules1, (350, 180), 20, 'Black')
    canvas.draw_text(rules2, (350, 210), 20, 'Black')
    canvas.draw_text(rules3, (350, 240), 20, 'Black')
    canvas.draw_text(rules4, (350, 270), 20, 'Black')
    canvas.draw_text(rules5, (350, 300), 20, 'Black')
    canvas.draw_text(rules6, (350, 330), 20, 'Black')
    canvas.draw_text(rules7, (350, 360), 20, 'Black')
    canvas.draw_text(rules8, (350, 390), 20, 'Black')
    my_card = my_hand
    dealer_card = dealer_hand
    my_card.draw(canvas, [100, 400])
    dealer_card.draw(canvas, [100, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (135, 248), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

# buttons and canvas callback
frame.add_button("Rules on/off", display_rules, 200)
frame.add_button("Reset", reset, 200)
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Double Down", double_down, 200)
frame.add_input('Bet Amount', input_handler, 200)
frame.set_draw_handler(draw)

# start
deal()
frame.start()
