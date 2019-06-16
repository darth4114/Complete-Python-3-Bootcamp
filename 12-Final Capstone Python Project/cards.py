'''
This module contains the main classes for blackjack.py
'''

import random


suits = ('Diamonds', 'Clubs', 'Hearts', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    '''Defines each of the 52 cards in the deck'''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck:

    def __init__(self):
        '''Generates the Deck of 52 cards'''
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck = ''
        for card in self.deck:
            deck += '\n' + card.__str__()
        return deck

    def shuffle(self):
        '''Shuffle deck'''
        random.shuffle(self.deck)

    def deal_card(self):
        '''Pop card off of deck to deal'''
        return self.deck.pop(0)


class Hand:
    '''Generate player's hands'''

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bust = False
        self.blackjack = False
        self.skip = False

    def draw(self, card):
        '''Drawing card from Deck() and adding value to total'''
        self.cards.append(card)
        self.value += values[card.rank]
        # check for ace
        if card.rank == 'Ace':
            self.aces += 1
        # bust switch check
        if self.value > 21:
            self.bust = True
        # blackjack switch check
        while True:
            try:
                if values[self.cards[0].rank] + values[self.cards[1].rank] == 21:
                    self.blackjack = True
            except IndexError:
                break
            else:
                break
        # ace value adjust
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            self.bust = False

    def split(self):
        '''Split hand if cards are same value'''
        self.value -= values[self.cards[0].rank]
        return self.cards.pop()


class Chips:
    '''
    Defines the player's chip bank
    args = amoutn of chips
    '''

    def __init__(self, value):
        self.value = value
        self.bet = 0

    def lose_bet(self):
        self.value -= self.bet

    def win_bet(self):
        self.value += self.bet


def disp_hand(player):
    print(*player.cards, sep='\n')
    print(f"Hand Value = {player.value}")


def ask_chips(chips):
    '''Asks player how many chips they want to start with'''
    while True:
        try:
            chips.value = int(input("How many chips do you want to buy? - "))
        except ValueError:
            print("Sorry, I didn't understand you, please try again")
            continue
        else:
            if chips.value < 1:
                print(
                    "You haven't bought enough chips to play, you need to purchase more.\n")
                continue
            else:
                break

    print(f"Thank you!\nYou have bought {chips.value} chips!")


def ask_bet(chips):
    '''Asks player for a bet, cannot be more than their current chip count'''
    while True:
        try:
            chips.bet = int(input("How many chips do you want to bet? - "))
        except ValueError:
            print("Sorry, I didn't understand you, please try again")
            continue
        else:
            if chips.bet < 1:
                print(
                    "Sorry, you did not bet a valid amount of chips. Please try again.")
                continue
        break


def split_hand(hand, chips, deck, sp_hand, sp_chips):
    '''
    return a new hand of a popped card from the player's hand, and a card from the desk
    also returns a new bank with the player's bet as the value and bet values
    '''
    # split hand and draw full hand
    sp_hand.skip = False
    sp_hand.draw(hand.split())
    sp_hand.draw(deck.deal_card())

    # split bank and set value and bet = chip.bet
    sp_chips.value = chips.bet
    sp_chips.bet = chips.bet
    chips.value -= chips.bet

    # if split hand draws a blackjack, pay out winnings and close the split loop
    if sp_hand.blackjack == True:
        disp_hand(sp_hand)
        reward_blackjack(chips)
        sp_hand.skip = True
        split = False

    return sp_hand, sp_chips


def hit(hand, deck):
    '''Append card to hand'''
    hand.draw(deck.deal_card())


def hit_or_stand(hand, deck):
    '''Ask if hit or stand until stand, or bust'''

    while True:
        x = input("Would you like to Hit or Stand? - ")

        if x[0].lower() == 'h':
            hit(hand, deck)
        elif x[0].lower() == 's':
            print("Player stands\n Next turn:\n")
            hand.skip = True
            break
        else:
            print("Sorry please try again.\n")
            continue
        break


def ready_to_play():
    '''Ask player if they want to play'''
    x = input("Are you ready to play?(y/n) - ")

    if x[0].lower() == 'y':
        return True
    else:
        return False


def reward_blackjack(chips):
    '''Apply blackjack winnings'''
    print("Player gets Blackjack!")
    chips.value += chips.bet * 2


def check_split(hand, chips):
    '''Check if the player's deal and bank are eligible for a split hand'''
    if values[hand.cards[0].rank] == values[hand.cards[1].rank] and chips.bet * 2 < chips.value:
        x = input("Do you want to split? (y/n) - ")

        if x[0] == 'y':
            print("Splitting hand!")
            return True
        else:
            print("Hand will not be split")
            return False


def dealer_draw(hand, sp_hand, dealer_hand, chips, sp_chips, deck):
    '''dealer's turn if players have not busted'''
    print("\nDealer's Hand:")
    disp_hand(dealer_hand)

    if hand.bust == False or hand.blackjack == False or sp_hand.bust == False or sp_hand.blackjack == False:
        while dealer_hand.value < 17:
            hit(dealer_hand, deck)
            print("\nDealer's Hand:")
            disp_hand(dealer_hand)
    if dealer_hand.bust == True:
        dealer_bust(hand, chips, sp_hand, sp_chips)


def push():
    '''No winner'''
    print("No winner, this hand is a push!")


def player_win(player, chips):
    '''If player wins, add winnings to value'''
    print("Player wins!")
    chips.win_bet()


def player_bust(player, chips):
    '''If player busts, subtract bet from value'''
    print("Player busts!")
    chips.lose_bet()


def dealer_win(player, chips):
    '''If dealer wins, subtract bet from value'''
    print("Dealer wins!")
    chips.lose_bet()


def dealer_bust(player, chips, sp_hand, sp_chips):
    '''If dealer busts, add winnings to value'''
    print("Dealer busts!")
    if sp_chips.bet > 0 and sp_hand.blackjack == False:
        chips.win_bet()
        chips.value += sp_chips.bet * 2
    else:
        chips.win_bet()


def split_combine(chips, split, dealer):
    '''Combine winnings/losses from a split hand'''
    if split.bust == True or split.skip == True:
        pass
    elif dealer.value > split.value:
        print("Lose. Dealer beat's split")
    elif split.value > dealer.value:
        player_win(split, chips)
    elif split.value == dealer.value:
        push()


def calc_results(player, chips, sp_hand, sp_chips, dealer):
    '''Calculates the winning results'''
    split_combine(chips, sp_hand, dealer)

    if player.bust == False:
        if player.value > dealer.value:
            print("\nPlayer's Hand:")
            disp_hand(player)
            print("\nDealer's Hand:")
            disp_hand(dealer)
            player_win(player, chips)
        elif player.value < dealer.value and dealer.bust == False:
            # print("\nDealer's Hand:")
            # disp_hand(dealer)
            dealer_win(player, chips)
        elif player.value == dealer.value:
            push()


def reset_board(player, chips, sp_hand, sp_chips, dealer, deck):
    chips.bet = 0
    sp_chips.bet = 0
    del player
    del sp_hand
    del dealer
    del deck
