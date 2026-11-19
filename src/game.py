from cambio import Cambio

def main():
    amount_players = int(input("How many players are playing the game? (2-6): "))

    game = Cambio(amount_players)
    game.start_game()
    # running = True
    # final = None
    # input("Press enter when you are ready to start the game")
    # for i in range(amount_players):
    #     first_turn_logic(players, turn)
    #     turn += 1
    #     input("Press enter when the next player is ready")
    #     if turn == amount_players:
    #         turn = 0
    # turn = start_turn
    # while running == True:
        
    #     # store turn as previous_turn so that it can be used later
    #     previous_turn = turn
        
    #     # chekc if the player called cambio on their previous turn
    #     if final == turn:
    #         break
        
    #     # do the players turn
    #     turn = turn_logic(players, turn)
        
    #     # handle if the player called cambio
    #     if turn == "cambio":
    #         final = previous_turn
    #         turn = previous_turn + 1
    #     else:
    #         turn += 1
        
    #     # loop back to player 1's turn
    #     if turn == amount_players:
    #         turn = 0
    #     input("Press enter when the next player is ready")
    # # After game ends count points
    # for i in range(amount_players):
    #     players[i].change_points(count_points(players, i))
    #     print(players[i])

if __name__ == "__main__":
    main()