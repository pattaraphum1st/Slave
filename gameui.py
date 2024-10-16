import tkinter as tk
from tkinter import messagebox
import random
import math


class CardGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Slave Card Game - Player Windows")
        self.root.geometry("200x200")
        self.root.withdraw()  # Hide the root window since it's unnecessary

        # Game logic data
        self.game = CardGame()  # Initialize the game logic
        self.selected_cards = []  # Store selected cards for multi-select
        self.current_turn = 0  # Track which player's turn it is (0 = Player 1, 1 = Player 2, etc.)
        self.round_winner = None  # Track the winner of the last round
        self.winners = []  # Track players who won the game in order

        # Automatically start the game with the first player who has '03c'
        self.first_player = self.game.find_first_player('03c')
        if self.first_player is not None:
            self.current_turn = self.first_player+1
            self.game.table = ['03c']
            self.game.players[self.first_player].remove_cards(['03c'])

        # Create a separate window for each player
        self.player_windows = []
        self.cards_left_labels = []  # Store cards left labels for updating later
        self.create_player_windows()

        # Now update the UI once all windows are created
        self.update_ui()

        # Start the tkinter loop
        self.root.mainloop()

    def create_player_windows(self):
        """Creates separate windows for each player."""
        for i in range(4):
            player_window = tk.Toplevel(self.root)
            player_window.title(f"Player {i + 1}")
            player_window.geometry("600x400")
            player_window.config(bg="lightyellow")

            # Label showing which player this window is for
            tk.Label(player_window, text=f"Player {i + 1}", font=("Arial", 16), bg="lightyellow").pack()

            # Display other players' remaining cards and keep track of their labels
            labels = []
            for j in range(4):
                if i != j:  # Other players
                    label = tk.Label(player_window, text=f"Player {j + 1} CARDS LEFT: {len(self.game.players[j].cards)}", font=("Arial", 12))
                    label.pack()
                    labels.append(label)
                else:
                    labels.append(None)  # Player themselves has no label
            self.cards_left_labels.append(labels)

            # Table display in each player's window
            table_card_label = tk.Label(player_window, text="TABLE\nEMPTY", font=("Arial", 16), bg="lightgreen", width=20, height=4)
            table_card_label.pack(pady=10)

            # Create a frame to display the player's own cards
            card_frame = tk.Frame(player_window, bg="lightyellow")
            card_frame.pack(pady=20)

            # Play and Surrender buttons
            play_button = tk.Button(player_window, text="Play Selected Cards", command=lambda i=i: self.play_selected_cards(i), font=("Arial", 14), bg="lightgreen")
            play_button.pack(pady=5)

            surrender_button = tk.Button(player_window, text="Surrender", command=lambda i=i: self.surrender(i), font=("Arial", 14), bg="red")
            surrender_button.pack(pady=5)

            # Add player window details to list
            self.player_windows.append({
                "window": player_window,
                "card_frame": card_frame,
                "table_card_label": table_card_label,
                "play_button": play_button,
                "surrender_button": surrender_button,
                "player_id": i
            })

    def update_ui(self):
        """Update the player windows to reflect the current state of the game."""
        # Update each player's window
        for player_window_info in self.player_windows:
            player_id = player_window_info["player_id"]
            card_frame = player_window_info["card_frame"]
            table_card_label = player_window_info["table_card_label"]
            play_button = player_window_info["play_button"]
            surrender_button = player_window_info["surrender_button"]

            # Clear old cards
            for widget in card_frame.winfo_children():
                widget.destroy()

            # Update table card display in the player's window
            if len(self.game.table) > 0:
                table_card_label.config(text="TABLE\n" + " ".join(self.game.table))
            else:
                table_card_label.config(text="TABLE\nEMPTY")

            # Display player's own cards (interactive if it's their turn)
            self.game.players[player_id].sort_cards()
            for j, card in enumerate(self.game.players[player_id].cards):
                if player_id == self.current_turn:  # Only allow interaction for the current player
                    # Create the button first
                    btn = tk.Button(card_frame, text=card, width=8, height=3)
                    # Set the command, passing `btn` and `player_id` using default arguments in the lambda to capture the correct references
                    btn.config(command=lambda j=j, btn=btn, player_id=player_id: self.toggle_select_card(j, player_id, btn))
                    btn.pack(side=tk.LEFT, padx=5)
                    # Highlight selected cards
                    if card in self.selected_cards:
                        btn.config(bg="yellow")
                else:
                    # Display cards without interaction for other players
                    tk.Label(card_frame, text=card, width=8, height=3).pack(side=tk.LEFT, padx=5)

            # Enable buttons only for the current player
            if player_id == self.current_turn:
                play_button.config(state=tk.NORMAL)
                surrender_button.config(state=tk.NORMAL)
            else:
                play_button.config(state=tk.DISABLED)
                surrender_button.config(state=tk.DISABLED)

        # Update "cards left" labels for each player
        self.update_cards_left_labels()

    def update_cards_left_labels(self):
        """Update the number of cards left labels in each player's window."""
        for i, labels in enumerate(self.cards_left_labels):
            for j, label in enumerate(labels):
                if label:
                    # Update the label for players other than the current one
                    label.config(text=f"Player {j + 1} CARDS LEFT: {len(self.game.players[j].cards)}")

    def toggle_select_card(self, card_index, player_id, button):
        """Toggle selection of a card in the current player's hand and highlight the selected card."""
        card = self.game.players[player_id].cards[card_index]
        if card in self.selected_cards:
            self.selected_cards.remove(card)  # Deselect the card
            button.config(bg="SystemButtonFace")  # Reset the button background color to default
        else:
            self.selected_cards.append(card)  # Select the card
            button.config(bg="yellow")  # Highlight selected card
        self.update_ui()  # Update the UI to reflect changes

    def play_selected_cards(self, player_id):
        """Play the selected cards and process the move."""
        if not self.selected_cards:
            messagebox.showerror("Error", "You must select at least one card to play.")
            return

        # Validate the selected cards
        if not CardUtils.is_valid_selection(self.selected_cards, self.game.table):
            messagebox.showerror("Error", "Invalid selection. Cards must be the same rank and no more than 4 cards.")
            return

        # First turn, the player can play any cards
        if self.game.first_turn:
            self.game.table = self.selected_cards[:]  # Update the table with selected cards
            self.game.players[player_id].remove_cards(self.selected_cards)
            self.game.first_turn = False
        else:
            # Check the even/odd rule and card strength comparison
            if len(self.selected_cards) % 2 != len(self.game.table) % 2:
                messagebox.showerror("Error", "You must play an even number of cards during an even round or an odd number during an odd round.")
                return

            if not self.game.compair(self.selected_cards, self.game.table):
                messagebox.showerror("Error", "Selected cards are not stronger than the table cards.")
                return

            # Valid play
            self.game.table = self.selected_cards[:]
            self.game.players[player_id].remove_cards(self.selected_cards)

        # Clear selected cards
        self.selected_cards = []

        # Check if the player has won the game (finished all cards)
        if len(self.game.players[player_id].cards) == 0:
            self.winners.append(player_id)  # Track the player as a game winner
            messagebox.showinfo("Game Winner", f"Player {self.game.players[player_id].id + 1} has won the game by finishing all cards!")

            # Check if we have 3 winners, which means the game is over for the remaining player
            if len(self.winners) == 3:
                remaining_player = self.get_remaining_player()
                self.winners.append(remaining_player)  # The last player automatically loses
                self.show_podium()
                return  # End the game

            # If the game is not over, the player won but the turn moves to the next player
            self.next_turn()
            self.update_ui()  # Ensure the UI reflects the next player's turn
            return

        # Move to the next player's turn if no one has won
        self.next_turn()

        # Update the UI for the next round
        self.update_ui()


    def surrender(self, player_id):
        """Process the player's surrender."""
        self.game.surrender[player_id] = 1  # Mark the player as surrendered
        self.game.tsurrender = sum(self.game.surrender)

        # Clear selected cards when a player surrenders
        self.selected_cards = []

        # Dynamic threshold: 3 minus the number of players who have already won
        surrender_threshold = 3 - len(self.winners)

        # If enough players have surrendered, the remaining player wins the round
        if self.game.tsurrender >= surrender_threshold:
            remaining_player = self.get_remaining_player()
            messagebox.showinfo("Round Over", f"Player {remaining_player + 1} wins this round by default!")

            # Check if the remaining player has finished all cards (won the game)
            if len(self.game.players[remaining_player].cards) == 0:
                self.winners.append(remaining_player)  # They win the game
                messagebox.showinfo("Game Winner", f"Player {remaining_player + 1} has won the game by finishing all cards!")

                # If 3 players have won, end the game with a podium
                if len(self.winners) == 3:
                    self.show_podium()
                    return  # End the game

            self.round_winner = remaining_player
            self.reset_round(clear_table=False)  # Do not clear the table
        else:
            messagebox.showinfo("Surrender", f"Player {player_id + 1} has surrendered for this round.")
            # Move to the next player's turn
            self.next_turn()

        # Update the UI for the next round and clear selected card highlights
        self.update_ui()

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_turn = (self.current_turn + 1) % 4
        # Skip players who have won the game (no cards left) or have already surrendered
        while self.game.surrender[self.current_turn] == 1 or len(self.game.players[self.current_turn].cards) == 0:
            self.current_turn = (self.current_turn + 1) % 4


    def get_remaining_player(self):
        """Returns the index of the player who has not surrendered in the round."""
        for i, surrendered in enumerate(self.game.surrender):
            if surrendered == 0 and len(self.game.players[i].cards) > 0:
                return i
        return None

    def reset_round(self, clear_table=False):
        """Resets the round state for the next round."""
        self.game.surrender = [0, 0, 0, 0]  # Reset surrender status for all players
        self.game.tsurrender = 0

        if clear_table:
            self.game.table = []  # Clear the table only if specified

        self.game.first_turn = True  # Set the next round as the first turn

        # The winner of the previous round starts the next round if they still have cards left
        if self.round_winner is not None and len(self.game.players[self.round_winner].cards) > 0:
            self.current_turn = self.round_winner
        else:
            # If the round winner has no cards, find the next player
            self.current_turn = self.get_next_player_with_cards()

        # Clear selected cards
        self.selected_cards = []
        self.update_ui()

    def get_next_player_with_cards(self, current_player):
        """Find the next player who still has cards left to play, starting from the current player."""
        for i in range(1, 5):  # Check the next 4 players in a circular manner
            next_player = (current_player + i) % 4  # Use modulo to wrap around the player index
            if len(self.game.players[next_player].cards) > 0 and next_player not in self.winners:
                return next_player
        return None  # Fallback case if no players have cards left


    def show_podium(self):
        """Display the podium with the order of winners."""
        podium = "\n".join([f"{i + 1}. Player {self.winners[i] + 1}" for i in range(4)])
        messagebox.showinfo("Podium", f"Game Over! Here are the results:\n\n{podium}")
        self.root.quit()  # Exit the game after showing the podium


class CardGame:
    def __init__(self):
        self.won = []
        self.table = []
        self.deck = self.create_deck()
        self.players = [Player(i) for i in range(4)]
        self.surrender = [0, 0, 0, 0]
        self.tsurrender = 0
        self.first_turn = True  # Track if it's the first player's turn in a new round
        self.shuffle_deck()
        self.deal_cards()

    def create_deck(self):
        """Creates a standard deck of cards."""
        return ['03c', '03d', '03h', '03s', '04c', '04d', '04h', '04s', 
                '05c', '05d', '05h', '05s', '06c', '06d', '06h', '06s', 
                '07c', '07d', '07h', '07s', '08c', '08d', '08h', '08s', 
                '09c', '09d', '09h', '09s', '10c', '10d', '10h', '10s', 
                '0jc', '0jd', '0jh', '0js', '0qc', '0qd', '0qh', '0qs', 
                '0kc', '0kd', '0kh', '0ks', '0ac', '0ad', '0ah', '0as', 
                '02c', '02d', '02h', '02s']

    def shuffle_deck(self):
        """Shuffles the deck."""
        random.shuffle(self.deck)

    def deal_cards(self):
        """Deals cards to players."""
        for player in self.players:
            player.cards = []
        
        for i in range(math.floor(len(self.deck) / 4)):
            for player in self.players:
                player.cards.append(self.deck.pop(0))

    def find_first_player(self, card):
        """Finds the first player with the specified card."""
        for i, player in enumerate(self.players):
            if card in player.cards:
                return i
        return None

    def compair(self, select, table):
        """Compares selected cards with table cards."""
        vselect = CardUtils.card_convert(select)
        vtable = CardUtils.card_convert(table)
        tvselect = CardUtils.card_sum(vselect)
        tvtable = CardUtils.card_sum(vtable)
        return tvselect > tvtable


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cards = []

    def sort_cards(self):
        """Sorts the player's cards."""
        self.cards = CardUtils.card_sort(self.cards)

    def remove_cards(self, selected):
        """Removes selected cards from the player's hand."""
        self.cards = list(set(self.cards) - set(selected))


class CardUtils:
    @staticmethod
    def card_convert(card):
        """Converts card for internal comparison."""
        ncard = []
        for i in range(len(card)):
            new = 0
            if card[i][:2] == '0j':
                new += 11
            elif card[i][:2] == '0q':
                new += 12
            elif card[i][:2] == '0k':
                new += 13
            elif card[i][:2] == '0a':
                new += 14
            elif card[i][:2] == '02':
                new += 15
            else:
                new += float(card[i][:2])

            if card[i][-1:] == 'c':
                new += 0.1
            elif card[i][-1:] == 'd':
                new += 0.2
            elif card[i][-1:] == 'h':
                new += 0.3
            elif card[i][-1:] == 's':
                new += 0.4
            ncard.append(new)
        return ncard

    @staticmethod
    def card_rconvert(card):
        """Reverse converts the card from internal representation."""
        ncard = []
        for i in range(len(card)):
            if int(card[i]) == 10:
                new = '10'
            else:
                new = '0'
            if int(card[i]) == 11:
                new += 'j'
            elif int(card[i]) == 12:
                new += 'q'
            elif int(card[i]) == 13:
                new += 'k'
            elif int(card[i]) == 14:
                new += 'a'
            elif int(card[i]) == 15:
                new += '2'
            elif int(card[i]) == 10:
                pass
            else:
                new += str(int(card[i]))

            if round(card[i] - math.floor(card[i]), 1) == 0.1:
                new += 'c'
            elif round(card[i] - math.floor(card[i]), 1) == 0.2:
                new += 'd'
            elif round(card[i] - math.floor(card[i]), 1) == 0.3:
                new += 'h'
            elif round(card[i] - math.floor(card[i]), 1) == 0.4:
                new += 's'

            ncard.append(new)
        return ncard

    @staticmethod
    def quick_sort(arr):
        """Performs a quick sort on the list."""
        if len(arr) < 2:
            return arr
        else:
            pivot = arr[0]
            less = [i for i in arr[1:] if i <= pivot]
            greater = [i for i in arr[1:] if i > pivot]
            return CardUtils.quick_sort(less) + [pivot] + CardUtils.quick_sort(greater)

    @staticmethod
    def card_sort(card):
        """Sorts a deck of cards."""
        vcard = CardUtils.card_convert(card)
        sorted_vcard = CardUtils.quick_sort(vcard)
        return CardUtils.card_rconvert(sorted_vcard)

    @staticmethod
    def card_sum(arr):
        """Calculates the sum of the card values."""
        result = 1
        for i in arr:
            result = i * result * 3
        return result

    @staticmethod
    def is_valid_selection(select, table):
        """Validates the selected cards."""
        if len(select) == 0:
            return False
        if select[0][:2] == select[len(select) - 2][:2] == select[len(select) - 1][:2] and len(select) <= 4:
            return True
        return False


# Main game loop
if __name__ == "__main__":
    CardGameUI()
