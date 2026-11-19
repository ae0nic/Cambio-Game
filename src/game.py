"""Command-line entry point for starting a Cambio game."""

if __package__:
    from .cambio import Cambio, GameState
    from .display import PygameDisplay
    from .instructions import display_rules
else:
    from cambio import Cambio, GameState
    from display import PygameDisplay
    from instructions import display_rules



def _run_game(display):
    """Run a console-driven Cambio game with a live Pygame display."""
    while True:
        answer = display.console_input("Number of players (2-6): ").strip()
        try:
            player_count = int(answer)
        except ValueError:
            print("Enter a number.")
            continue
        if 2 <= player_count <= 6:
            break
        print("A Cambio game needs between 2 and 6 players.")

    player_names = []
    while len(player_names) < player_count:
        name = display.console_input(
            f"Enter a name for player {len(player_names) + 1}: "
        ).strip()
        if not name:
            print("Names cannot be empty.")
        elif name in player_names:
            print("Each player needs a unique name.")
        else:
            player_names.append(name)

    game = Cambio(player_count, input_fn=display.console_input)
    game.initialize_players(player_names)

    while True:
        starting_name = display.console_input(
            f"Who starts? ({', '.join(player_names)}): "
        ).strip()
        try:
            game.set_starting_player(starting_name)
            break
        except ValueError:
            print("Enter one of the player names shown.")

    display.bind(game)
    game.deal_starting_hands()
    display.refresh()
    print("\nStarting hands have been dealt. Each player may look at their two bottom cards.")
    for player_index, name in enumerate(player_names):
        display.console_input(f"{name}, press Enter when you are ready to view your cards.")
        display.show_initial_cards(player_index)
        print(f"{name}, remember these cards: {game.show_bottom_cards(player_index)}")
        display.console_input("Press Enter to pass the screen to the next player.")
        display.hide_initial_cards()

    print(f"\nThe starting discard is {game.get_discard_top_card()}.")
    while game.get_game_state() != GameState.ENDED:
        current_player_index = game.get_current_player_index()
        game.turn_logic(current_player_index, display.refresh)
        if game.get_game_state() != GameState.ENDED:
            game.advance_turn()
            display.refresh()

    players = game.get_players()
    lowest_score = min(game.count_points(index) for index in range(len(players)))
    winners = [
        player.get_name()
        for index, player in enumerate(players)
        if game.count_points(index) == lowest_score
    ]
    print("\nFinal scores:")
    for index, player in enumerate(players):
        print(
            f"{player.get_name()}: {game.count_points(index)} points "
            f"({player.get_cards()})"
        )
    print(f"Winner{'s' if len(winners) != 1 else ''}: {', '.join(winners)}")


def main():
    """Start the console-driven game and its Pygame display."""
    display = PygameDisplay()
    try:
        _run_game(display)
    finally:
        display.close()


if __name__ == "__main__":
    display_rules()
    main()