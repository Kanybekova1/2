import os
import string
import random

class BattleshipGame:
    def __init__(self):
        self.board_size = 7
        self.ship_sizes = [3, 2, 2, 1, 1, 1, 1]
        self.ships = []
        self.player_shots = []
        self.player_name = ""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def welcome(self):
        self.clear_screen()
        print("Welcome to Battleship!")
        self.player_name = input("Enter your name: ")

    def initialize_ships(self):
        while len(self.ships) < len(self.ship_sizes):
            ship_size = self.ship_sizes[len(self.ships)]
            ship = self.generate_ship(ship_size)
            if self.validate_ship(ship):
                self.ships.append(ship)

    def generate_ship(self, ship_size):
        direction = random.choice(["horizontal", "vertical"])
        if direction == "horizontal":
            start_row = random.randint(0, self.board_size - 1)
            start_col = random.randint(0, self.board_size - ship_size)
            ship = [(start_row, start_col + i) for i in range(ship_size)]
        else:
            start_row = random.randint(0, self.board_size - ship_size)
            start_col = random.randint(0, self.board_size - 1)
            ship = [(start_row + i, start_col) for i in range(ship_size)]
        return ship

    def validate_ship(self, ship):
        for cell in ship:
            row, col = cell
            if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                return False
            for other_ship in self.ships:
                if cell in other_ship:
                    return False
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (row + i, col + j) in other_ship:
                            return False
        return True

    def display_board(self, show_ships=False):
        self.clear_screen()
        print(f"Player: {self.player_name}\n")
        print("   A B C D E F G")
        for i in range(self.board_size):
            row = f"{i + 1} |"
            for j in range(self.board_size):
                if (i, j) in self.player_shots:
                    if (i, j) in [cell for ship in self.ships for cell in ship] and show_ships:
                        row += "X "
                    else:
                        row += "O "
                else:
                    row += "  "
            print(row)

    def convert_coordinates(self, coordinate):
        col_map = {char: index for index, char in enumerate(string.ascii_uppercase[:self.board_size])}
        col = col_map.get(coordinate[0].upper(), None)
        row = int(coordinate[1:]) - 1 if coordinate[1:].isdigit() else None
        return row, col

    def player_turn(self):
        while True:
            shot_input = input("Enter coordinates to shoot (e.g., A5): ")
            if len(shot_input) < 2:
                print("Invalid input. Please enter a letter and a digit (e.g., A5).")
                continue

            col, row = self.convert_coordinates(shot_input)
            if col is None or row is None or not (0 <= col < self.board_size) or not (0 <= row < self.board_size):
                print("Invalid coordinates. Please enter a valid location on the board.")
                continue

            if (row, col) in self.player_shots:
                print("You've already shot at this location. Try a different one.")
                continue

            self.player_shots.append((row, col))
            break

        for ship in self.ships:
            if (row, col) in ship:
                ship.remove((row, col))
                if len(ship) == 0:
                    print("You've sunk a ship!")
                else:
                    print("You've hit a ship!")
                return True

        print("You've missed!")
        return False

    def play_game(self):
        self.welcome()
        self.initialize_ships()
        while True:
            self.display_board()
            if all(len(ship) == 0 for ship in self.ships):
                print(f"Congratulations {self.player_name}! You've sunk all the ships!")
                break
            if not self.player_turn():
                input("Press Enter to continue...")
            self.display_board(show_ships=True)
            input("Press Enter to continue...")

if __name__ == "__main__":
    game = BattleshipGame()
    game.play_game()
