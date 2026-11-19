from pathlib import Path

#code =
#Cambio card game with a Tkinter interface.

#This version uses only Python's standard library. It does NOT require pygame
#or any other third-party package.

#Run in Spyder with:
 #   %runfile 'C:/path/to/cambio_tkinter.py' --wdir
#or open the file and click Run.

import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from enum import Enum


# ---------------------------------------------------------------------------
# CARD, PLAYER, DECK, AND DISCARD-PILE CLASSES
# ---------------------------------------------------------------------------

class Card:
    POINTS = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "Jack": 10, "Queen": 10, "King": 10,
        "Ace": 1, "Joker": 0
    }

    SUIT_SYMBOLS = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠",
        "Joker": "★"
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_points(self):
        # Red Kings are worth -1; black Kings are worth 10.
        if self.rank == "King" and self.suit in ("Hearts", "Diamonds"):
            return -1
        return self.POINTS[self.rank]

    def short_rank(self):
        return {"Jack": "J", "Queen": "Q", "King": "K",
                "Ace": "A", "Joker": "★"}.get(self.rank, self.rank)

    def color(self):
        return "#c62828" if self.suit in ("Hearts", "Diamonds") else "#172554"


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def get_name(self):
        return self.name

    def get_cards(self):
        return self.cards.copy()

    def set_cards(self, cards):
        self.cards = cards.copy()

    def add_card(self, card):
        self.cards.append(card)

    def remove_card_by_index(self, index):
        return self.cards.pop(index)

    def get_points(self):
        return sum(card.get_points() for card in self.cards)


class Deck:
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = [
            Card(suit, rank)
            for suit in self.SUITS
            for rank in self.RANKS
        ]
        self.cards.extend([Card("Joker", "Joker"), Card("Joker", "Joker")])
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            return None
        return self.cards.pop()


class DiscardPile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        if card is not None:
            self.cards.append(card)

    def look_top_card(self):
        return self.cards[-1] if self.cards else None

    def get_cards(self):
        return self.cards.copy()


class GameState(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    DRAWING = 3
    CAMBIO_CALLED = 4
    ENDED = 5


# ---------------------------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------------------------

class Cambio:
    STARTING_HAND_SIZE = 4

    def __init__(self, num_players):
        if not 2 <= num_players <= 6:
            raise ValueError("Cambio requires 2 to 6 players.")
        self.num_players = num_players
        self.players = []
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.current_player = 0
        self.state = GameState.NOT_STARTED
        self.drawn_card = None
        self.pending_ability_card = None
        self.cambio_caller = None
        self.final_turns_remaining = 0

    def initialize_players(self, names):
        if len(names) != self.num_players:
            raise ValueError("The number of names must match the player count.")
        self.players = [Player(name) for name in names]

    def start(self, starting_player_index=0):
        self.current_player = starting_player_index
        for player in self.players:
            for _ in range(self.STARTING_HAND_SIZE):
                player.add_card(self.deck.deal())
        self.state = GameState.IN_PROGRESS

    def current(self):
        return self.players[self.current_player]

    def draw_card(self):
        if self.state not in (GameState.IN_PROGRESS, GameState.CAMBIO_CALLED):
            raise RuntimeError("It is not currently possible to draw.")
        if self.drawn_card is not None:
            raise RuntimeError("A drawn card is already waiting for a decision.")
        if self.pending_ability_card is not None:
            raise RuntimeError("Resolve the pending card ability first.")
        self.drawn_card = self.deck.deal()
        if self.drawn_card is None:
            raise RuntimeError("The draw pile is empty.")
        self.state = GameState.DRAWING
        return self.drawn_card

    def keep_drawn_card(self, hand_index):
        if self.state != GameState.DRAWING or self.drawn_card is None:
            raise RuntimeError("There is no drawn card to keep.")
        hand = self.current().get_cards()
        if not 0 <= hand_index < len(hand):
            raise IndexError("Select a valid card in your hand.")
        replaced = hand[hand_index]
        hand[hand_index] = self.drawn_card
        self.current().set_cards(hand)
        self.discard_pile.add_card(replaced)
        self.drawn_card = None
        self.state = (GameState.CAMBIO_CALLED if self.cambio_caller is not None
                      else GameState.IN_PROGRESS)
        return replaced

    def discard_drawn_card(self):
        if self.state != GameState.DRAWING or self.drawn_card is None:
            raise RuntimeError("There is no drawn card to discard.")
        card = self.drawn_card
        self.discard_pile.add_card(card)
        self.drawn_card = None
        self.state = (GameState.CAMBIO_CALLED if self.cambio_caller is not None
                      else GameState.IN_PROGRESS)
        if has_card_ability(card):
            self.pending_ability_card = card
        return card

    def resolve_ability(self, own_index=None, target_player_index=None,
                        target_index=None, swap=False):
        card = self.pending_ability_card
        if card is None:
            return None
        own = self.current()
        target = (self.players[target_player_index]
                  if target_player_index is not None else None)

        if card.rank in ("7", "8"):
            if own_index is None:
                raise ValueError("Choose one of your own cards.")
            result = own.get_cards()[own_index]
        elif card.rank in ("9", "10"):
            if target is None or target is own:
                raise ValueError("Choose another player.")
            if target_index is None:
                raise ValueError("Choose a card from that player.")
            result = target.get_cards()[target_index]
        elif card.rank in ("Jack", "Queen") or (
                card.rank == "King" and card.suit in ("Clubs", "Spades")):
            if target is None or target is own:
                raise ValueError("Choose another player.")
            if own_index is None or target_index is None:
                raise ValueError("Choose one card from each player.")
            own_cards = own.get_cards()
            target_cards = target.get_cards()
            own_card = own_cards[own_index]
            target_card = target_cards[target_index]
            result = (own_card, target_card)
            if card.rank in ("Jack", "Queen") or swap:
                own_cards[own_index] = target_card
                target_cards[target_index] = own_card
                own.set_cards(own_cards)
                target.set_cards(target_cards)
        else:
            result = None

        self.pending_ability_card = None
        return result

    def call_cambio(self):
        if self.cambio_caller is not None:
            raise RuntimeError("Cambio has already been called.")
        self.cambio_caller = self.current_player
        self.final_turns_remaining = self.num_players - 1
        self.state = GameState.CAMBIO_CALLED

    def advance_turn(self):
        was_final_round = self.cambio_caller is not None
        self.current_player = (self.current_player + 1) % self.num_players
        if was_final_round:
            self.final_turns_remaining -= 1
            if self.final_turns_remaining <= 0:
                self.state = GameState.ENDED
                return
            # Skip the player who called Cambio if the turn order wraps.
            if self.current_player == self.cambio_caller:
                self.current_player = (self.current_player + 1) % self.num_players
        else:
            self.state = GameState.IN_PROGRESS

    def stick_card(self, own_index, target_player_index=None, target_index=None):
        return self.stick_card_for_player(
            self.current_player, own_index, target_player_index, target_index
        )

    def stick_card_for_player(self, player_index, own_index,
                              target_player_index=None, target_index=None):
        """Attempt a stick on behalf of any player in the table-wide stick round.

        A matching own card is placed on the discard pile. A matching opponent
        card is exchanged for the selected card belonging to the player making
        the attempt (so that player gives the opponent one of their cards).
        A failed attempt gives the attempting player a penalty card.
        """
        if not 0 <= player_index < self.num_players:
            raise IndexError("Select a valid player.")
        top = self.discard_pile.look_top_card()
        if top is None:
            raise RuntimeError("There is no card on the discard pile.")

        actor = self.players[player_index]
        actor_cards = actor.get_cards()
        if not 0 <= own_index < len(actor_cards):
            raise IndexError("Select a valid card from your hand.")

        if target_player_index is None:
            if actor_cards[own_index].rank == top.rank:
                stuck = actor.remove_card_by_index(own_index)
                self.discard_pile.add_card(stuck)
                return True
        else:
            if not 0 <= target_player_index < self.num_players:
                raise IndexError("Select a valid target player.")
            target = self.players[target_player_index]
            if target is actor:
                raise ValueError("You cannot target yourself.")
            target_cards = target.get_cards()
            if not 0 <= target_index < len(target_cards):
                raise IndexError("Select a valid target card.")
            if target_cards[target_index].rank == top.rank:
                actor_cards[own_index], target_cards[target_index] = (
                    target_cards[target_index], actor_cards[own_index]
                )
                actor.set_cards(actor_cards)
                target.set_cards(target_cards)
                return True

        penalty = self.deck.deal()
        if penalty is not None:
            actor.add_card(penalty)
        return False

    def scores(self):
        return [(p.get_name(), p.get_points()) for p in self.players]


def has_card_ability(card):
    return (
        card.rank in ("7", "8", "9", "10", "Jack", "Queen")
        or (card.rank == "King" and card.suit in ("Clubs", "Spades"))
    )


# ---------------------------------------------------------------------------
# TKINTER USER INTERFACE
# ---------------------------------------------------------------------------

class CambioApp:
    BG = "#176344"
    FELT = "#1d7954"
    CREAM = "#f7f0dc"
    RED = "#b4232e"
    DARK = "#172554"
    GOLD = "#f4c95d"

    def __init__(self, root):
        self.root = root
        self.root.title("Cambio")
        self.root.geometry("1120x820")
        self.root.minsize(900, 700)

        self.game = None
        self.selected_card = None
        self.drawn_card = None
        self.action_mode = None
        self.ability_selection = {}
        self.stick_window_open = False
        self.initial_peek_cards = {}
        self.initial_peek_active = set()
        self.stick_round_queue = []
        self.stick_round_message = ""

        self.canvas = tk.Canvas(root, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        controls = tk.Frame(root, bg="#123f30", padx=10, pady=9)
        controls.pack(fill="x")

        self.status = tk.Label(
            controls, text="Welcome to Cambio",
            bg="#123f30", fg="white", font=("Arial", 13, "bold")
        )
        self.status.pack(side="left", padx=8)

        self.draw_button = tk.Button(
            controls, text="Draw Card", command=self.draw_card,
            font=("Arial", 10, "bold"), width=12
        )
        self.draw_button.pack(side="right", padx=4)

        self.discard_button = tk.Button(
            controls, text="Discard Draw", command=self.discard_draw,
            font=("Arial", 10, "bold"), width=12, state="disabled"
        )
        self.discard_button.pack(side="right", padx=4)

        self.swap_button = tk.Button(
            controls, text="Swap Selected", command=self.swap_draw,
            font=("Arial", 10, "bold"), width=12, state="disabled"
        )
        self.swap_button.pack(side="right", padx=4)

        self.stick_button = tk.Button(
            controls, text="Stick Card", command=self.start_stick,
            font=("Arial", 10, "bold"), width=10, state="disabled"
        )
        self.stick_button.pack(side="right", padx=4)

        self.end_turn_button = tk.Button(
            controls, text="End Turn", command=self.end_turn,
            font=("Arial", 10, "bold"), width=10
        )
        self.end_turn_button.pack(side="right", padx=4)

        self.cambio_button = tk.Button(
            controls, text="Call Cambio", command=self.call_cambio,
            font=("Arial", 10, "bold"), width=12
        )
        self.cambio_button.pack(side="right", padx=4)

        self.new_button = tk.Button(
            controls, text="New Game", command=self.new_game,
            font=("Arial", 10, "bold"), width=10
        )
        self.new_button.pack(side="right", padx=4)

        self.canvas.bind("<Configure>", lambda event: self.redraw())
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.show_instructions()
        self.new_game()

    # ----- setup and turn control -----

    def show_instructions(self):
        instructions = (
            "HOW TO PLAY CAMBIO\n\n"
            "1. Enter the number of players (2–6).\n"
            "2. Enter each player's name when prompted.\n"
            "3. Choose the player who takes the first turn.\n"
            "4. Each player is privately shown two of their four cards at setup.\n"
            "5. At the start of a turn, the player may call Cambio using the Call Cambio button.\n"
            "6. If Cambio is not called, draw a card. Choose a card in your hand and press Swap Selected, or press Discard Draw.\n"
            "7. When swapping, the selected hand card is replaced by the drawn card; the replaced card goes to the discard pile.\n"
            "8. When discarding, the drawn card goes to the discard pile. Special abilities are then offered for: 7/8 (peek at your own card), 9/10 (peek at an opponent's card), J/Q (exchange cards with an opponent), and black Kings (peek at one of yours and one opponent's, then optionally exchange).\n"
            "9. Whenever a card is added to the discard pile by a swap or discard, every player gets one chance in turn order to stick either one of their own cards or an opponent's card. If the selected card matches the top discard rank, your own card is discarded (own-card stick) or exchanged with the opponent's card (opponent-card stick). If it does not match, you draw a penalty card.\n\n"
            "Use the on-screen buttons and prompts for input (this version uses a graphical interface rather than console commands)."
        )
        messagebox.showinfo("Cambio — Instructions", instructions, parent=self.root)

    def new_game(self):
        count = simpledialog.askinteger(
            "New Cambio Game", "How many players? (2–6)",
            parent=self.root, minvalue=2, maxvalue=6
        )
        if count is None:
            if self.game is None:
                self.root.destroy()
            return

        names = []
        for i in range(count):
            name = simpledialog.askstring(
                "Player Names", f"Enter the name of player {i + 1}:",
                parent=self.root
            )
            if not name or not name.strip():
                name = f"Player {i + 1}"
            names.append(name.strip())

        starter = simpledialog.askinteger(
            "Starting Player",
            f"Who starts? Enter a number from 1 to {count}.",
            parent=self.root, minvalue=1, maxvalue=count
        )
        if starter is None:
            starter = 1

        self.game = Cambio(count)
        self.game.initialize_players(names)
        self.game.start(starter - 1)
        self.initial_peek_cards = {i: set() for i in range(count)}
        self.initial_peek_active = set(range(count))

        # Each player privately looks at two cards before the round begins.
        for player_index, player in enumerate(self.game.players):
            first = 1
            second = 2

            self.initial_peek_cards[player_index].update({first - 1, second - 1})
            first_card = player.cards[first - 1]
            second_card = player.cards[second - 1]
            messagebox.showinfo(
                "Private Peek",
                f"{player.name}, remember these cards:\n\n"
                f"Card {first}: {first_card}\n"
                f"Card {second}: {second_card}\n\n"
                "Pass the device to the next player. Keep these cards secret!",
                parent=self.root
            )

        self.selected_card = None
        self.drawn_card = None
        self.action_mode = None
        self.ability_selection = {}
        self.set_status(f"{self.game.current().name}'s turn. Select Draw Card or Call Cambio.")
        self.refresh_controls()
        self.redraw()

    def set_status(self, message):
        self.status.config(text=message)

    def refresh_controls(self):
        if self.game is None:
            return
        drawing = self.game.state == GameState.DRAWING
        ability = self.game.pending_ability_card is not None
        ended = self.game.state == GameState.ENDED
        final_round = self.game.cambio_caller is not None

        self.draw_button.config(
            state="normal" if not drawing and not ability and not ended else "disabled"
        )
        self.discard_button.config(
            state="normal" if drawing else "disabled"
        )
        self.swap_button.config(
            state="normal" if drawing and self.selected_card is not None else "disabled"
        )
        self.cambio_button.config(
            state="normal" if not final_round and not ended and not drawing else "disabled"
        )
        # Sticking is handled automatically as a table-wide round whenever
        # a card enters the discard pile; it is no longer a separate button action.
        self.stick_button.config(state="disabled")
        can_end_turn = (
            not drawing and not ability and not ended
        )
        self.end_turn_button.config(
            state="normal" if can_end_turn else "disabled"
        )

    def draw_card(self):
        try:
            self.drawn_card = self.game.draw_card()
            self.selected_card = None
            self.set_status(
                f"{self.game.current().name} drew a card. "
                "Choose a hand card to replace it, or discard the draw."
            )
        except Exception as error:
            messagebox.showerror("Cannot Draw", str(error), parent=self.root)
        self.refresh_controls()
        self.redraw()

    def discard_draw(self):
        try:
            card = self.game.discard_drawn_card()
            self.drawn_card = None
            self.selected_card = None
            self.refresh_controls()
            self.redraw()
            self.stick_round_message = f"{card} was discarded."
            if self.game.pending_ability_card is not None:
                self.resolve_ability_dialog()
            else:
                self.begin_stick_round(self.stick_round_message)
        except Exception as error:
            messagebox.showerror("Discard Error", str(error), parent=self.root)

    def swap_draw(self):
        if self.selected_card is None:
            return
        try:
            replaced = self.game.keep_drawn_card(self.selected_card)
            self.drawn_card = None
            self.selected_card = None
            self.refresh_controls()
            self.redraw()
            self.begin_stick_round(f"{replaced} was replaced and discarded.")
        except Exception as error:
            messagebox.showerror("Swap Error", str(error), parent=self.root)

    def call_cambio(self):
        try:
            caller = self.game.current().name
            self.game.call_cambio()
            self.set_status(
                f"{caller} called CAMBIO! Each other player gets one final turn."
            )
            self.refresh_controls()
            self.redraw()
            self.advance_after_turn()
        except Exception as error:
            messagebox.showerror("Cambio Error", str(error), parent=self.root)

    def after_action(self, message):
        self.offer_stick(message)

    def offer_stick(self, message):
        self.set_status(message + " You may now end your turn.")
        self.refresh_controls()
        self.redraw()

    def advance_after_turn(self):
        # Initial peeks are visible only during each player's first turn.
        # Once that player finishes the turn, those cards stay hidden.
        ending_player = self.game.current_player
        self.initial_peek_active.discard(ending_player)
        self.game.advance_turn()
        self.selected_card = None
        self.drawn_card = None
        if self.game.state == GameState.ENDED:
            self.show_results()
            return
        self.set_status(
            f"It is now {self.game.current().name}'s turn. "
            "Pass the device, then continue."
        )
        self.refresh_controls()
        self.redraw()

    def end_turn(self):
        if self.game.state == GameState.DRAWING:
            messagebox.showinfo(
                "Finish Your Turn", "Swap the drawn card or discard it first.",
                parent=self.root
            )
            return
        if self.game.pending_ability_card is not None:
            messagebox.showinfo(
                "Resolve Ability", "Resolve the special-card ability first.",
                parent=self.root
            )
            return
        self.advance_after_turn()

    # ----- special card abilities -----

    def resolve_ability_dialog(self):
        card = self.game.pending_ability_card
        if card is None:
            return
        players = self.game.players
        current = self.game.current_player

        if card.rank in ("7", "8"):
            index = simpledialog.askinteger(
                "Card Ability",
                f"{card.rank}: Choose one of your four cards to look at (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(self.game.current().cards)
            )
            if index is None:
                index = 1
            revealed = self.game.resolve_ability(own_index=index - 1)
            messagebox.showinfo(
                "Private Card Reveal",
                f"Your card {index} is {revealed}. Keep it secret!",
                parent=self.root
            )

        elif card.rank in ("9", "10"):
            target = self.ask_target_player()
            if target is None:
                target = (current + 1) % len(players)
            index = simpledialog.askinteger(
                "Card Ability",
                f"{card.rank}: Choose a card belonging to {players[target].name} (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(players[target].cards)
            )
            if index is None:
                index = 1
            revealed = self.game.resolve_ability(
                target_player_index=target, target_index=index - 1
            )
            messagebox.showinfo(
                "Private Card Reveal",
                f"{players[target].name}'s card {index} is {revealed}.",
                parent=self.root
            )

        elif card.rank in ("Jack", "Queen"):
            target = self.ask_target_player()
            if target is None:
                target = (current + 1) % len(players)
            own_index = simpledialog.askinteger(
                "Card Exchange",
                "Choose one of your cards to exchange (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(self.game.current().cards)
            )
            target_index = simpledialog.askinteger(
                "Card Exchange",
                f"Choose one of {players[target].name}'s cards (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(players[target].cards)
            )
            if own_index is None:
                own_index = 1
            if target_index is None:
                target_index = 1
            self.game.resolve_ability(
                own_index=own_index - 1,
                target_player_index=target,
                target_index=target_index - 1
            )
            messagebox.showinfo(
                "Ability Complete", "The selected cards have been exchanged.",
                parent=self.root
            )

        elif card.rank == "King" and card.suit in ("Clubs", "Spades"):
            target = self.ask_target_player()
            if target is None:
                target = (current + 1) % len(players)
            own_index = simpledialog.askinteger(
                "Black King Ability",
                "Choose one of your cards to reveal (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(self.game.current().cards)
            )
            target_index = simpledialog.askinteger(
                "Black King Ability",
                f"Choose one of {players[target].name}'s cards to reveal (1–4).",
                parent=self.root, minvalue=1, maxvalue=len(players[target].cards)
            )
            if own_index is None:
                own_index = 1
            if target_index is None:
                target_index = 1
            own_card, target_card = self.game.resolve_ability(
                own_index=own_index - 1,
                target_player_index=target,
                target_index=target_index - 1,
                swap=False
            )
            do_swap = messagebox.askyesno(
                "Black King",
                f"Your card: {own_card}\n"
                f"{players[target].name}'s card: {target_card}\n\n"
                "Would you like to exchange them?",
                parent=self.root
            )
            # The ability has already been cleared; perform the optional
            # exchange directly if the player chooses yes.
            if do_swap:
                own_cards = self.game.current().get_cards()
                target_cards = players[target].get_cards()
                own_cards[own_index - 1], target_cards[target_index - 1] = (
                    target_cards[target_index - 1], own_cards[own_index - 1]
                )
                self.game.current().set_cards(own_cards)
                players[target].set_cards(target_cards)

        self.refresh_controls()
        self.redraw()
        # The discard event's stick round happens after any special ability.
        if self.stick_round_message:
            message = self.stick_round_message
            self.stick_round_message = ""
            self.begin_stick_round(message)
        else:
            self.set_status("Special ability resolved. You may end your turn.")

    def ask_target_player(self):
        options = [
            f"{i + 1}: {player.name}"
            for i, player in enumerate(self.game.players)
            if i != self.game.current_player
        ]
        choice = simpledialog.askstring(
            "Choose Opponent",
            "Enter the number of the player to target:\n" + "\n".join(options),
            parent=self.root
        )
        if choice is None:
            return None
        try:
            index = int(choice) - 1
        except ValueError:
            return None
        if index == self.game.current_player or not 0 <= index < len(self.game.players):
            return None
        return index

    # ----- table-wide stick round -----

    def start_stick(self):
        messagebox.showinfo(
            "Stick Round",
            "Stick opportunities are offered to every player automatically "
            "after a card is added to the discard pile.",
            parent=self.root
        )

    def begin_stick_round(self, message):
        """Give every player one opportunity to stick after a discard event."""
        if self.game.discard_pile.look_top_card() is None:
            self.offer_stick(message)
            return
        current = self.game.current_player
        # Start with the next player, then include the player who made the discard.
        self.stick_round_queue = [
            (current + offset) % self.game.num_players
            for offset in range(1, self.game.num_players + 1)
        ]
        self.stick_round_message = message
        self.process_next_stick()

    def process_next_stick(self):
        if not self.stick_round_queue:
            message = self.stick_round_message
            self.stick_round_message = ""
            self.offer_stick(message + " Stick round complete.")
            return

        player_index = self.stick_round_queue.pop(0)
        player = self.game.players[player_index]
        top = self.game.discard_pile.look_top_card()
        if top is None or self.game.state == GameState.ENDED:
            self.process_next_stick()
            return

        take_action = messagebox.askyesnocancel(
            "Stick Opportunity",
            f"{player.name}, the top discard is {top}.\n\n"
            "Yes = try to stick one of an opponent's cards (if it matches, give them one of yours).\n"
            "No = try to stick one of your own cards.\n"
            "Cancel = pass.",
            parent=self.root
        )
        if take_action is None:
            self.process_next_stick()
            return

        try:
            if take_action is False:
                own_index = simpledialog.askinteger(
                    "Stick Your Card",
                    f"{player.name}: choose your card index to stick (1–{len(player.cards)}).",
                    parent=self.root, minvalue=1, maxvalue=len(player.cards)
                )
                if own_index is not None:
                    success = self.game.stick_card_for_player(
                        player_index, own_index - 1
                    )
                else:
                    success = None
            else:
                target_options = [
                    f"{i + 1}: {other.name}"
                    for i, other in enumerate(self.game.players)
                    if i != player_index
                ]
                choice = simpledialog.askstring(
                    "Choose Opponent",
                    f"{player.name}, enter the opponent's player number:\n" +
                    "\n".join(target_options), parent=self.root
                )
                try:
                    target_index = int(choice) - 1 if choice is not None else None
                except ValueError:
                    target_index = None
                if (target_index is None or target_index == player_index
                        or not 0 <= target_index < self.game.num_players):
                    success = None
                else:
                    target_player = self.game.players[target_index]
                    opponent_card = simpledialog.askinteger(
                        "Opponent Card",
                        f"Choose {target_player.name}'s card (1–{len(target_player.cards)}).",
                        parent=self.root, minvalue=1,
                        maxvalue=len(target_player.cards)
                    )
                    give_card = simpledialog.askinteger(
                        "Give Them Your Card",
                        f"Choose which of your cards to give {target_player.name} (1–{len(player.cards)}).",
                        parent=self.root, minvalue=1, maxvalue=len(player.cards)
                    )
                    if opponent_card is not None and give_card is not None:
                        success = self.game.stick_card_for_player(
                            player_index, give_card - 1,
                            target_index, opponent_card - 1
                        )
                    else:
                        success = None

            if success is True:
                messagebox.showinfo(
                    "Stick Successful",
                    f"{player.name} successfully stuck a matching card.",
                    parent=self.root
                )
            elif success is False:
                messagebox.showwarning(
                    "Stick Failed",
                    f"{player.name}'s card did not match. They received a penalty card.",
                    parent=self.root
                )
        except Exception as error:
            messagebox.showerror("Stick Error", str(error), parent=self.root)

        self.refresh_controls()
        self.redraw()
        self.process_next_stick()

    # ----- card drawing and click selection -----

    def on_canvas_click(self, event):
        if self.game is None or self.game.state == GameState.ENDED:
            return
        if self.game.state != GameState.DRAWING:
            return
        if self.drawn_card is None:
            return

        for index, bounds in enumerate(self.hand_bounds):
            x1, y1, x2, y2 = bounds
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_card = index
                self.set_status(
                    f"Selected card {index + 1}. Click Swap Selected to replace it."
                )
                self.refresh_controls()
                self.redraw()
                return

    def draw_card_shape(self, x, y, card=None, face_up=True,
                        width=76, height=108, selected=False):
        c = self.canvas
        outline = self.GOLD if selected else "#302a22"
        line_width = 4 if selected else 2
        if not face_up or card is None:
            c.create_rectangle(
                x, y, x + width, y + height,
                fill="#304b87", outline=outline, width=line_width
            )
            c.create_rectangle(
                x + 6, y + 6, x + width - 6, y + height - 6,
                outline="#e5d7b5", width=2
            )
            # Simple diagonal pattern replacing the original pygame masks.
            for offset in range(-height, width, 12):
                c.create_line(
                    x + max(0, offset), y + max(0, -offset),
                    x + min(width, offset + height), y + min(height, height + offset),
                    fill="#8294c2", width=1
                )
            c.create_text(
                x + width / 2, y + height / 2,
                text="✦", fill="#f7f0dc", font=("Arial", 25, "bold")
            )
            return

        c.create_rectangle(
            x, y, x + width, y + height,
            fill=self.CREAM, outline=outline, width=line_width
        )
        symbol = Card.SUIT_SYMBOLS[card.suit]
        color = card.color()
        rank = card.short_rank()
        c.create_text(
            x + 9, y + 8, text=rank, anchor="nw",
            fill=color, font=("Arial", 11, "bold")
        )
        c.create_text(
            x + 10, y + 25, text=symbol, anchor="nw",
            fill=color, font=("Arial", 13, "bold")
        )
        c.create_text(
            x + width / 2, y + height / 2 + 2,
            text=symbol, fill=color, font=("Arial", 34, "bold")
        )
        c.create_text(
            x + width - 9, y + height - 8, text=rank, anchor="se",
            fill=color, font=("Arial", 11, "bold")
        )
        c.create_text(
            x + width - 10, y + height - 25, text=symbol, anchor="se",
            fill=color, font=("Arial", 13, "bold")
        )

    def redraw(self):
        if not hasattr(self, "canvas") or self.game is None:
            return
        self.canvas.delete("all")
        self.hand_bounds = []

        width = max(self.canvas.winfo_width(), 900)
        height = max(self.canvas.winfo_height(), 600)
        self.canvas.create_rectangle(
            18, 18, width - 18, height - 18,
            fill=self.FELT, outline="#d6b56d", width=5
        )
        self.canvas.create_text(
            width / 2, 42, text="CAMBIO",
            fill="#fff4d6", font=("Georgia", 25, "bold")
        )

        # Player labels and hidden hands around the table.
        count = len(self.game.players)
        positions = {
            2: [(width / 2, height - 145), (width / 2, 125)],
            3: [(width / 2, height - 145), (width * .25, 145), (width * .75, 145)],
            4: [(width / 2, height - 145), (width * .22, height / 2),
                (width / 2, 125), (width * .78, height / 2)],
            5: [(width / 2, height - 145), (width * .18, height * .68),
                (width * .25, 135), (width * .75, 135),
                (width * .82, height * .68)],
            6: [(width / 2, height - 145), (width * .18, height * .68),
                (width * .18, height * .30), (width / 2, 125),
                (width * .82, height * .30), (width * .82, height * .68)]
        }[count]

        for player_index, player in enumerate(self.game.players):
            px, py = positions[player_index]
            is_current = player_index == self.game.current_player
            label_color = self.GOLD if is_current else "white"
            score_text = (
                f"{player.name}  •  {player.get_points()} pts"
                if self.game.state == GameState.ENDED or is_current
                else f"{player.name}  •  {len(player.cards)} cards"
            )
            self.canvas.create_text(
                px, py - 20, text=score_text, fill=label_color,
                font=("Arial", 12, "bold")
            )

            cards = player.get_cards()
            card_w, card_h = 60, 86
            gap = 8
            total_w = len(cards) * card_w + max(0, len(cards) - 1) * gap
            start_x = px - total_w / 2
            for card_index, card in enumerate(cards):
                cx = start_x + card_index * (card_w + gap)
                cy = py
                face_up = (
                    self.game.state == GameState.ENDED
                    or (
                        is_current
                        and player_index in self.initial_peek_active
                        and card_index in self.initial_peek_cards.get(player_index, set())
                    )
                )
                selected = (
                    is_current and self.selected_card == card_index
                    and self.game.state == GameState.DRAWING
                )
                self.draw_card_shape(
                    cx, cy, card if face_up else None,
                    face_up=face_up, width=card_w, height=card_h,
                    selected=selected
                )
                if is_current:
                    self.hand_bounds.append((cx, cy, cx + card_w, cy + card_h))
                    self.canvas.create_text(
                        cx + card_w / 2, cy + card_h + 13,
                        text=str(card_index + 1), fill="white",
                        font=("Arial", 9, "bold")
                    )

        # Draw pile and discard pile in the middle.
        center_x = width / 2
        center_y = height / 2
        self.canvas.create_text(
            center_x - 90, center_y - 82, text="DRAW PILE",
            fill="white", font=("Arial", 10, "bold")
        )
        self.draw_card_shape(center_x - 125, center_y - 65, face_up=False)
        self.canvas.create_text(
            center_x + 90, center_y - 82, text="DISCARD",
            fill="white", font=("Arial", 10, "bold")
        )
        top_discard = self.game.discard_pile.look_top_card()
        if top_discard is None:
            self.draw_card_shape(center_x + 52, center_y - 65, face_up=False)
        else:
            self.draw_card_shape(center_x + 52, center_y - 65, top_discard)

        if self.drawn_card is not None:
            self.canvas.create_text(
                center_x, center_y + 75, text="YOUR DRAW",
                fill=self.GOLD, font=("Arial", 10, "bold")
            )
            self.draw_card_shape(
                center_x - 38, center_y + 88, self.drawn_card,
                face_up=True, width=76, height=108
            )

        if self.game.state == GameState.CAMBIO_CALLED:
            self.canvas.create_text(
                center_x, center_y + 35,
                text=f"CAMBIO CALLED — {self.game.final_turns_remaining} final turns left",
                fill=self.GOLD, font=("Arial", 12, "bold")
            )
        elif self.game.state == GameState.ENDED:
            self.canvas.create_text(
                center_x, center_y + 35, text="GAME OVER",
                fill=self.GOLD, font=("Arial", 17, "bold")
            )

    def show_results(self):
        self.refresh_controls()
        self.redraw()
        results = sorted(self.game.scores(), key=lambda item: item[1])
        lines = ["Final scores (lowest score wins):", ""]
        for name, points in results:
            lines.append(f"{name}: {points} points")
        if results:
            lines.extend(["", f"Winner: {results[0][0]}"])
        messagebox.showinfo("Cambio Results", "\n".join(lines), parent=self.root)
        self.set_status("Game over. Select New Game to play again.")


def main():
    root = tk.Tk()
    CambioApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
