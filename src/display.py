"""Pygame table display for the console-driven Cambio game."""

import threading

import pygame


class PygameDisplay:
    """Render game state while leaving all decisions to console prompts."""

    WIDTH = 1100
    HEIGHT = 760
    PANEL_WIDTH = 320
    PANEL_HEIGHT = 180
    CARD_WIDTH = 56
    CARD_HEIGHT = 78

    FELT = (32, 91, 67)
    PANEL = (23, 68, 51)
    PANEL_ACTIVE = (211, 176, 92)
    CREAM = (248, 242, 222)
    INK = (34, 39, 37)
    RED = (176, 48, 48)
    MUTED = (190, 211, 197)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Cambio")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 15)
        self.tiny_font = pygame.font.SysFont("arial", 12, bold=True)
        self.game = None
        self.running = True
        self.revealed_player = None

    def bind(self, game) -> None:
        """Attach the game whose state is shown in the window."""
        self.game = game
        self.refresh()

    def show_initial_cards(self, player_index: int) -> None:
        """Reveal only the current player's two starting cards."""
        self.revealed_player = player_index
        self.refresh()

    def hide_initial_cards(self) -> None:
        """Conceal the starting cards before the next player looks."""
        self.revealed_player = None
        self.refresh()

    def refresh(self) -> None:
        """Draw the current table state and process pending window events."""
        if not self.running:
            return
        self._process_events()
        if not self.running:
            return
        self._draw()
        pygame.display.flip()

    def console_input(self, prompt: str = "") -> str:
        """Read console input while keeping the pygame window responsive."""
        if not self.running:
            return input(prompt)

        result = []
        errors = []
        finished = threading.Event()

        def read_console():
            try:
                result.append(input(prompt))
            except BaseException as error:
                errors.append(error)
            finally:
                finished.set()

        reader = threading.Thread(target=read_console, daemon=True)
        reader.start()
        while not finished.is_set() and self.running:
            self._process_events()
            if self.running:
                self._draw()
                pygame.display.flip()
                self.clock.tick(30)
        reader.join()
        if errors:
            raise errors[0]
        return result[0]

    def close(self) -> None:
        """Close the display and release pygame resources."""
        if self.running:
            self.running = False
            pygame.quit()

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return

    def _draw(self) -> None:
        self.screen.fill(self.FELT)
        title = self.title_font.render("CAMBIO", True, self.CREAM)
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 30)))

        if self.game is None:
            hint = self.font.render(
                "Enter player details in the console to begin",
                True,
                self.MUTED,
            )
            self.screen.blit(hint, hint.get_rect(center=(self.WIDTH // 2, 100)))
            return

        players = self.game.get_players()
        current_index = self.game.get_current_player_index()
        status = self.game.get_game_state().name.replace("_", " ").title()
        current_name = players[current_index].get_name() if players else "-"
        status_text = self.small_font.render(
            f"{status}  |  Current turn: {current_name}",
            True,
            self.MUTED,
        )
        self.screen.blit(
            status_text,
            status_text.get_rect(center=(self.WIDTH // 2, 64)),
        )

        positions = (
            (30, 94),
            (390, 94),
            (750, 94),
            (30, 546),
            (390, 546),
            (750, 546),
        )
        for index, player in enumerate(players):
            self._draw_player(index, player, positions[index], index == current_index)

        self._draw_piles()

    def _draw_player(self, index: int, player, position, active: bool) -> None:
        x, y = position
        panel = pygame.Rect(x, y, self.PANEL_WIDTH, self.PANEL_HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL, panel, border_radius=14)
        border = self.PANEL_ACTIVE if active else (74, 120, 94)
        pygame.draw.rect(self.screen, border, panel, width=3, border_radius=14)

        name = self.font.render(player.get_name(), True, self.CREAM)
        self.screen.blit(name, (x + 14, y + 10))
        hand = player.get_cards()
        count = self.small_font.render(f"{len(hand)} cards", True, self.MUTED)
        self.screen.blit(count, (x + self.PANEL_WIDTH - count.get_width() - 14, y + 15))

        count_in_hand = max(1, len(hand))
        gap = 6
        card_width = min(
            self.CARD_WIDTH,
            (self.PANEL_WIDTH - 28 - gap * (count_in_hand - 1)) // count_in_hand,
        )
        card_height = max(38, int(card_width * self.CARD_HEIGHT / self.CARD_WIDTH))
        total_width = count_in_hand * card_width + (count_in_hand - 1) * gap
        card_x = x + (self.PANEL_WIDTH - total_width) // 2
        card_y = y + 68
        for card_index, card in enumerate(hand):
            visible = (
                index == self.revealed_player
                and card_index >= max(0, len(hand) - 2)
            )
            self._draw_card(
                card,
                (card_x + card_index * (card_width + gap), card_y),
                (card_width, card_height),
                face_up=visible,
            )

    def _draw_piles(self) -> None:
        center_y = self.HEIGHT // 2
        draw_x = 360
        discard_x = 684
        drawn_x = 522
        card_size = (76, 106)

        draw_count = self.game.get_draw_pile_count()
        for layer in range(min(3, (draw_count + 9) // 10)):
            self._draw_card_back((draw_x + layer * 4, center_y - 40 - layer * 4), card_size)
        deck_count = self.small_font.render(f"MAIN PILE  ({draw_count})", True, self.CREAM)
        self.screen.blit(deck_count, deck_count.get_rect(center=(draw_x + 38, center_y + 84)))

        discard = self.game.get_discard_cards()
        if discard:
            for layer in range(min(3, len(discard)) - 1):
                self._draw_card_back(
                    (discard_x + layer * 4, center_y - 40 - layer * 4),
                    card_size,
                )
            self._draw_card(discard[-1], (discard_x, center_y - 40), card_size)
        else:
            self._draw_card_back((discard_x, center_y - 40), card_size, empty=True)
        discard_count = self.small_font.render(
            f"DISCARD PILE  ({len(discard)})",
            True,
            self.CREAM,
        )
        self.screen.blit(
            discard_count,
            discard_count.get_rect(center=(discard_x + 38, center_y + 84)),
        )

        drawn_card = self.game.get_drawn_card()
        self._draw_card(
            drawn_card,
            (drawn_x, center_y - 40),
            card_size,
            face_up=drawn_card is not None,
        )
        drawn_label = self.small_font.render("DRAWN CARD", True, self.CREAM)
        self.screen.blit(
            drawn_label,
            drawn_label.get_rect(center=(drawn_x + 38, center_y + 84)),
        )

    def _draw_card(self, card, position, size, face_up=True) -> None:
        x, y = position
        width, height = size
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.CREAM, rect, border_radius=7)
        pygame.draw.rect(self.screen, (218, 210, 187), rect, width=2, border_radius=7)
        if not face_up or card is None:
            pygame.draw.rect(
                self.screen,
                (47, 76, 126),
                rect.inflate(-8, -8),
                border_radius=5,
            )
            pygame.draw.rect(
                self.screen,
                (207, 220, 244),
                rect.inflate(-14, -14),
                width=2,
                border_radius=4,
            )
            return

        if card.suit in ("Hearts", "Diamonds"):
            color = self.RED
            suit = "H" if card.suit == "Hearts" else "D"
        elif card.suit == "Clubs":
            color, suit = self.INK, "C"
        elif card.suit == "Spades":
            color, suit = self.INK, "S"
        else:
            color, suit = self.INK, "J"
        rank = "JOKER" if card.rank == "Joker" else card.rank
        label = self.tiny_font.render(f"{rank} {suit}", True, color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_card_back(self, position, size, empty=False) -> None:
        x, y = position
        width, height = size
        rect = pygame.Rect(x, y, width, height)
        if empty:
            pygame.draw.rect(self.screen, (30, 77, 58), rect, border_radius=7)
            pygame.draw.rect(self.screen, (114, 157, 132), rect, width=2, border_radius=7)
        else:
            self._draw_card(None, position, size, face_up=False)
