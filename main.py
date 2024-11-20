"""class to hold cards"""
    #deck
    #card scores

"""game logic"""
    #choose number of players 

    #hand out 2 cards to each player.
        #go to the deck pick random and pop
        #do not show dealers second card 

    #ask player to hit or stand:
        #total >21 bust and go to next player
        #if total < 21 ask again

    #game ends when dealer plays.

import random

class Cardholder:
    # Method to create a deck of cards
    @staticmethod
    def deck():
        full_deck = []
        for suit in ["H", "D", "S", "C"]:
            for value in range(2, 10):
                full_deck.append(f'{value}:{suit}')
            for value in ["A", "J", "K", "Q"]:
                full_deck.append(f'{value}:{suit}')
        return full_deck

    # Initialize and shuffle the deck
    newdeck = deck()
    random.shuffle(newdeck)

    def deck_reset():
        Cardholder.newdeck = Cardholder.deck()
        random.shuffle(Cardholder.newdeck)

        

    # Dictionary to store card values
    scores = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'J': 10, 'K': 10, 'Q': 10, 'A': 11
    }

    # Method to check if the score is a blackjack
    @staticmethod
    def isblackjack(score):
        return score == 21

    # Method to calculate the total score of a list of cards
    @staticmethod
    def totalcardscore(listcards):
        total = 0
        for card in listcards:
            total += Cardholder.scores[card[0]]
        return total

class Players:
    # Method for a player to take a card from the deck
    @staticmethod
    def player_takecard():
        try:
            card = Cardholder.newdeck[0]
            Cardholder.newdeck.pop(0)
            return card
        except IndexError:
            Cardholder.deck_reset()
            card = Cardholder.newdeck[0]
            Cardholder.newdeck.pop(0)
            return card

    # List to hold the cards of each player
    player_stackholder = [[], [], [], []]

    # Method to add a card to a player's stack
    @staticmethod
    def playeradd_tostack(playerposition):
        Players.player_stackholder[playerposition].append(Players.player_takecard())

    # Method to decide whether to hit or stand
    @staticmethod
    def hitorstand(score):
        if Cardholder.isblackjack(score):
            return "blackjack"
        else:
            hitostand = input("Hit or Stand? ")
            return hitostand

class Dealer:
    # List to hold the dealer's cards
    dealer_stackholder = []

    # Method to add a card to the dealer's stack
    @staticmethod
    def dealeradd_tostack():
        Dealer.dealer_stackholder.append(Players.player_takecard())

def game_play():
    print("****WELCOME TO BLACKJACK****")

    # Get the number of players
    while True:
        try:
            numplayers = int(input("How Many Player Hands Do You Want To Play? "))
            if numplayers in range(1, 5):
                break
        except ValueError:
            print("Please enter a valid number between 1 and 4.")

    # Deal the first 2 cards to each player and the dealer
    for rounds in range(1, 3):
        for playerposition in range(numplayers):
            Players.playeradd_tostack(playerposition)
        Dealer.dealeradd_tostack()

    # Print the initial cards and scores of each player
    for playerposition in range(numplayers):
        playerscards = Players.player_stackholder[playerposition]
        score = Cardholder.totalcardscore(playerscards)
        if score == 21:
            score = "BlackJack!!"
        print(f'Player {playerposition + 1} cards: {playerscards} scores == {score}')

    # Print the dealer's first card
    dealercard = Dealer.dealer_stackholder[0]
    print(f'Dealer card: [{dealercard}] score == {Cardholder.scores[dealercard[0]]}')

    playersscores = []

    # Players decide to hit or stand
    for playerposition in range(numplayers):
        playerscards = Players.player_stackholder[playerposition]
        playerscore = Cardholder.totalcardscore(playerscards)
        while playerscore <= 21:
            if playerscore <21:
                print(f'Player {playerposition + 1}', end=" ")
                response = Players.hitorstand(playerscore)
            if  playerscore==21:
                playersscores.append(21)
                break
            elif response.lower() in ["hit", "h"]:
                Players.playeradd_tostack(playerposition)
                playerscore = Cardholder.totalcardscore(playerscards)
                if playerscore > 21:
                    print(f'Player {playerposition + 1} cards: {playerscards} score == {playerscore} BUST!')
                    playersscores.append(playerscore)
                else:
                    print(f'Player {playerposition + 1} cards: {playerscards} score == {playerscore}')
            elif response.lower() in ["stand", "s"]:
                playersscores.append(playerscore)
                break

    dealertotal = []
    dealerscore = Cardholder.totalcardscore(Dealer.dealer_stackholder)
    # Dealer's turn to draw cards
    while dealerscore <= 21:
        if Cardholder.isblackjack(dealerscore):
            if len(Dealer.dealer_stackholder) ==2:
                print(f'Dealer card: {Dealer.dealer_stackholder} score == {dealerscore} BlackJack')
            else:
                print(f'Dealer card: {Dealer.dealer_stackholder} score == {dealerscore}')
                dealertotal.append(dealerscore)
            break
        elif dealerscore >= 17:
            print(f'Dealer card: {Dealer.dealer_stackholder} score == {dealerscore}')
            dealertotal.append(dealerscore)
            break
        else:
            Dealer.dealeradd_tostack()
            dealerscore = Cardholder.totalcardscore(Dealer.dealer_stackholder)
            if dealerscore > 21:
                print(f'Dealer card: {Dealer.dealer_stackholder} score == {dealerscore} Bust!!')
                dealertotal.append(dealerscore)
    

    # Determine the outcome for each player
    # Constants for readability
    BUST_THRESHOLD = 21

    for i, player_score in enumerate(playersscores):
        player_number = i + 1
        dealer_score = dealertotal[0]

        if (dealer_score > BUST_THRESHOLD and player_score <= BUST_THRESHOLD) or (player_score <= BUST_THRESHOLD and player_score > dealer_score):
            print(f'Player {player_number} WON!!')
        elif (player_score< 21 and dealer_score <21) and (player_score == dealer_score):
            print(f'Player {player_number} PUSHED!!')
        elif (dealer_score <= BUST_THRESHOLD and (player_score < dealer_score or player_score > 21)) or (player_score> 21 and dealer_score >21):
            print(f'Dealer WON AGAINST Player {player_number}')
        print(playersscores)

    playersscores.clear()
    dealertotal.clear()

def main():
    inp = True
    while inp:
        game_play()
        endgame = input("Press 'E' to exit game or 'C' to continue to new game: ")

        if endgame.lower() == 'e':
            print("Goodbye")
            inp = False
        elif endgame.lower() == 'c':
            for i in Players.player_stackholder:
                i.clear()
            Dealer.dealer_stackholder.clear()
        

if __name__ == "__main__":
    main()
