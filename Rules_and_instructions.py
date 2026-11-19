def display_rules():
    output = "Cambio is a fast paced memory game where the goal of each round is to have the least amount of points in your hand."
    output += "\n The basic rules to Cambio are as follows:\n"
    output += "1: Each player starts with 4 cards in a 2x2 grid and are shown the bottom two cards in that grid\n"
    output += "2: At the start of each player's turn, they will be able to call Cambio\n"
    output += "3: Calling Cambio means every player other than the player who called Cambio gets one more turn before the game ends\n"
    output += "4: If the player does not call Cambio then they will draw a card from the deck\n"
    output += "5: The drawn card can be swapped with a card from the player's hand, or it can be discarded\n"
    output += "6: Some cards have special abilities that can be activated when they are discarded directly after being drawn\n"
    output += "7: Cards with this ability include 7s, 8s, 9s, 10s, Jacks, Queens, and Kings of Spades or Clubs\n"
    output += "8: The special effects for 7s and 8s allow the player to look at one of their own cards\n"
    output += "9: The special effects for 9s and 10s allow the player to look at one of their opponent's face down cards\n"
    output += "10: The special effects for Queens and Jacks allow the player to switch a card with one of their opponent's cards\n"
    output += "11: The special effects for Kings of Spades or Clubs allow the player to look at one of their opponent's cards then decide if they want to swap one of the cards from their hand with that card\n "
    output += "12: When a card is discarded regardless of when it was discarded, all players can choose if they want to stick a card to the discarded card\n"
    output += "13: If the stuck card is the same rank as the top card in the discard pile, then the stuck card is discarded\n"
    output += "14: If the stuck card is not the same rank as the top card in the discard pile, then the player who attempted to stick a card gets a card added to their hand\n"
    output += "15: Only one player can successfully stick a card, multiple can if the stuck card is invalid\n"
    output += "16: Each card has an assigned point value. Number cards are their number, Jokers are 0, Queens, Jacks, and Kings of Spades and Clubs are 10, Kings of Hearts and Diamonds are -1\n"
    output += "17: When the game is over, the player with the least amount of points at the end of each round wins!\n"
    output += display_instructions()
    with open("Rules_and_Instructions.txt", "w") as out_file:
        out_file.write(output)
def display_instructions():
    output = "\nInstructions for playing Cambio will be displayed on the screen\n"
    output += "All inputs will prompt the user for a text based response\n"
    output += "Instructions will be obvious to player"
    return output
display_rules()