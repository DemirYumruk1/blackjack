import random
from time import sleep

#-------initialise playerand dealer hands---------
class Player:
    def __init__(self):
        self.hand = []
        self.split_hand = []
        self.score = 0
        self.split_score = 0
        self.money = 100

    def getHand(self):
        return self.hand

    def getScore(self):
        self.__calcScore()
        return self.score
    
    def getSplitScore(self):
        self.__calcScore(True)
        return self.split_score

    def getMoney(self):
        return self.money

    def addMoney(self, add):
        self.money += add

    def loseMoney(self, bet):
        self.money -= bet

    def draw(self, *args):
        card = deck.pop()
        if card == 11:
            card = "J"
        if card == 12:
            card = "K"
        if card == 13:
            card = "Q"
        if card == 14:
            card = "A"

        if len(args) == 0:
            self.hand.append(card)
        else:
            self.split_hand.append(card)

    def __calcScore(self, *args):
        total = 0
        if len(args) == 0:
            self.hand.sort(key = lambda i: i == "A")
            for card in self.hand:
                if card == "J" or card == "K" or card == "Q":
                    total += 10
                elif card == "A":
                    if total >= 11:
                        total += 1
                    if total < 11:
                        total += 11
                else:
                    total += card
        
            self.score = total

        else:
            self.split_hand.sort(key = lambda i: i == "A")
            for card in self.split_hand:
                if card == "J" or card == "K" or card == "Q":
                    total += 10
                elif card == "A":
                    if total >= 11:
                        total += 1
                    if total < 11:
                        total += 11
                else:
                    total += card
            self.split_score = total

    def reset(self):
        self.hand = []
        self.split_hand = []
        self.score = 0

    def split(self):
        card = self.hand.pop(1)
        self.split_hand.append(card)

    def getSplitHand(self):
        return self.split_hand

class Dealer(Player):
    def __init__(self):
        self.money = random.randint(1000000,1500000)

    def showCard(self):
        return self.hand[0]
#globals
moneyToWin= 0

def playerTurn(player: Player, bet: int):
    global bust, split_game
    moneyToWin = 0
    def playerLoop(split):
        global bust, moneyToWin
        turn = True
        bust = False
        while turn:

            if not split:
                player_hand = player.getHand()
            else:
                player_hand = player.getSplitHand()
            
            print(f"Your hand:{player_hand}")
            
            choice=input("\nType 'hit' to draw, anything else to stand.")
            if choice == 'hit':
                if not split:
                    player.draw()
                else:
                    player.draw(split)
            else:
                turn = False
                
            if not split:
                player_score = player.getScore()
                if player_score > 21:
                    moneyToWin= 0
                    bust = True
                    print(f"Your hand:{player_hand}")
                    print("Bust!")
                    break
                elif player_score == 21:
                    moneyToWin = bet*4
                    bust = True
                    print(f"Your hand:{player_hand}")
                    print(f"Blackjack! You won ${moneyToWin - bet}!")
                    player.addMoney(moneyToWin)
                    break

            else:
                player_score = player.getSplitScore()
                if player_score > 21:
                    moneyToWin= 0
                    bust = True
                    print(f"Your hand:{player_hand}")
                    print("Bust!")
                    break
                elif player_score == 21:
                    moneyToWin = bet*4
                    bust = True
                    print(f"Your hand:{player_hand}")
                    print(f"Blackjack! You won ${moneyToWin}!")
                    player.addMoney(moneyToWin)
                    break

        return moneyToWin
    
    bust = False
    split_game = False
    player_hand = player.getHand()

    if player_hand[0] == player_hand[1]:
    #if True:
        choice = input(f"\nYour hand is {player_hand}. \nDo you wish to split? Enter 'y' if yes: ")
        if choice == 'y': player.split(); split_game = True
        
    moneyToWin = playerLoop(False)

    if split_game:
        moneyToWin += playerLoop(True)
    else:
        return moneyToWin
    
def compScores(dealer_score, player_score, bet):
    prize = 0
    if dealer_score > 21:
            print("Dealer bust!\n")
            prize=bet*2
    elif dealer_score > player_score:
            print("Dealer win.\n")
            prize=0
    elif player_score > dealer_score:
            print("You win!\n")
            prize = bet*2
    elif player_score == dealer_score:
            print("Draw.\n")
            prize = bet
    return prize

def dealerTurn(dealer: Dealer, bet: int, player: Player, split_game: bool):
    dealer_score = dealer.getScore()
    player_score = player.getScore()
    player_split_score = player.getSplitScore()
    while dealer_score < 11:
        dealer.draw()
        sleep(2)
        print(f"Dealer hand:{dealer.getHand()}")
        dealer_score = dealer.getScore()

    if not split_game and player_score < 21:
        moneyToWin = compScores(dealer_score, player_score, bet)

    if split_game:
        bet = bet//2
        if player_score < 21:
            moneyToWin = compScores(dealer_score, player_split_score, bet)
        
        elif player_split_score < 21:
            moneyToWin = compScores(dealer_score, player_score, bet)

        else:
            moneyToWin = compScores(dealer_score, player_split_score, bet)
            moneyToWin += compScores(dealer_score, player_score, bet)
    return moneyToWin

def validateBet(player: Player, hasHouse: bool):
    validBet = False
    player_bal = player.getMoney()
    while validBet == False:
        try:
            if hasHouse:
                bet = int(input(f"You have ${player_bal}. Enter your bet: "))
            else:
                bet = int(input(f"You have ${player_bal} and no house. Enter your bet: "))
            validBet = True
        except:
            print("Invalid bet.")
            validBet = False
    while bet > player_bal:
        bet = int(input(f"Bet too high.\nYou have ${player_bal}. Enter your bet: "))
    return bet

def Main():
    global deck
    win = False
    hasHouse = True
    player = Player()
    dealer = Dealer()
    deck = []

    while True:
        skip = False
        player.reset()
        dealer.reset()
        player_bal = player.getMoney()
        dealer_bal = dealer.getMoney()
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        random.shuffle(deck)

        moneyToWin = 0

        print(f"You estimate the dealer has ${dealer_bal} left.\n")

        #check for game overs
        if player_bal <= 0 and not hasHouse:
            print("You are now in crippling debt. You may no longer play.")
            break

        if player_bal <= 0 and hasHouse:
            money = random.randint(100,100000)
            print(f"You have sold your house to gamble more.\nOn the way back you got distracted by the slot machine and now only have ${money} left.\n")
            hasHouse = False
            player.addMoney(money)
        
        if dealer_bal <= 0:
            print("You have gotten the dealer fired and the casino is in debt to you. You may no longer play.")
            win= True
            break

        bet = validateBet(player, hasHouse)

        #start the game
        player.loseMoney(bet)
        dealer.addMoney(bet)
        dealer.draw()
        dealer.draw()
        print(f"The dealer's first card is: {dealer.showCard()}")
        
        if dealer.showCard() == 'A':
            insurance = input("Take insurance? Type 'y' if yes.")
            if insurance == "y":
                if dealer.getScore() == 21:
                    print("Dealer had a natural blackjack.\n")
                    skip = True
                    player.addMoney(bet // 2)
                    dealer.loseMoney(bet // 2)
                else:
                    print("Dealer does not have a blackjack.\n")
                    bet //= 1.5

        if not skip:
            player.draw()
            player.draw()
            moneyToWin = playerTurn(player, bet) 
            
            
            print(f"Dealer hand:{dealer.getHand()}")
            
            if not bust:
                moneyToWin = dealerTurn(dealer, bet, player, split_game)
            
                if not moneyToWin is None:
                    player.addMoney(moneyToWin)
                    dealer.loseMoney(moneyToWin)
    if win:
        if hasHouse:
            print("You are now a millionaire!")
        else:
            print("You have bought a house but due to inflation it cost all of the money you earned. \nOne more round and maybe you could win it all again!")
        print(f"Final score: {player_bal}")
            
                
if __name__ == "__main__":
	Main()
