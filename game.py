import random
import math

class CardGame:
    def __init__(self):
        self.won = []
        self.table = []
        self.deck = self.create_deck()
        self.players = [Player(i) for i in range(4)]
        self.surrender = [0, 0, 0, 0]
        self.tsurrender = 0
        self.first_turn = True  # Track if it's the first player's turn in a new round

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

    def play(self):
        """Main game loop."""
        self.shuffle_deck()
        self.deal_cards()
        
        for player in self.players:
            player.sort_cards()
        
        first_player = self.find_first_player('03c')
        self.table = ['03c']
        current_player_index = (first_player + 1) % 4
        self.players[first_player].remove_cards(['03c'])

        while len(self.won) < 3:
            if self.tsurrender >= 3:
                current_player_index = self.surrender.index(0)
                self.table = []  # Reset table when all but one have surrendered
                self.first_turn = True  # Reset for a new round
            
            self.surrender = [0, 0, 0, 0]
            self.tsurrender = 0

            while self.tsurrender < 3:
                current_player = self.players[current_player_index]
                if self.surrender[current_player_index] != 1 or len(current_player.cards) == 0:
                    print(f'\nplayer1: {len(self.players[0].cards)} player2: {len(self.players[1].cards)} player3: {len(self.players[2].cards)} player4: {len(self.players[3].cards)}')
                    print(f'table: {self.table}')
                    print(f'player {current_player.id + 1}')
                    print(current_player.get_sorted_cards())

                    if current_player.surrender_choice():
                        self.surrender[current_player_index] = 1
                        self.tsurrender = sum(self.surrender)
                        current_player_index = (current_player_index + 1) % 4
                        continue

                    while True:
                        selected_cards = current_player.select_cards(self.table)
                        if selected_cards is not None:  # Ensure selected_cards is not None
                            if self.first_turn:
                                # The first player in the round can play any number of cards
                                self.table = selected_cards
                                self.first_turn = False  # From now on, apply even/odd rule
                                current_player.remove_cards(selected_cards)
                                if len(current_player.cards) == 0:
                                    self.won.append(current_player.id)
                                break
                            else:
                                # For subsequent players, check if the number of selected cards matches the table parity
                                if len(selected_cards) % 2 != len(self.table) % 2:
                                    print("Error: You must play an even number of cards during an even round or an odd number during an odd round. Try again.")
                                elif self.table and not self.compair(selected_cards, self.table):  # Skip comparison if table is empty
                                    print("Error: Selected cards are not stronger than the table cards. Try again.")
                                else:
                                    # Valid selection
                                    self.table = selected_cards
                                    current_player.remove_cards(selected_cards)
                                    if len(current_player.cards) == 0:
                                        self.won.append(current_player.id)
                                    break
                        else:
                            print("Error: Invalid card selection. Please enter valid cards.")
                current_player_index = (current_player_index + 1) % 4
        
        print("Winning order:", self.won)

    def find_first_player(self, card):
        """Finds the first player with the specified card."""
        for i, player in enumerate(self.players):
            if card in player.cards:
                return i
        return -1

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

    def get_sorted_cards(self):
        """Returns the sorted cards."""
        return CardUtils.card_sort(self.cards)

    def surrender_choice(self):
        """Asks the player if they want to surrender."""
        choice = input(f"Player {self.id + 1}, surrender? [y/n]: ")
        return choice == 'y'

    def select_cards(self, table):
        """Asks the player to select cards and ensures they are valid and in the player's hand."""
        try:
            selected = input("Enter the list of selected cards: ").split()
            # Check if selected cards are in the player's hand
            if not set(selected).issubset(set(self.cards)):
                print("Error: You cannot play cards that are not in your hand. Try again.")
                return None
            if CardUtils.is_valid_selection(selected, table):
                return selected
        except Exception as e:
            print(e)
        return None

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



# Initialize the game
game = CardGame()

# Start the game
game.play()