from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()

        # Coordinates already fired at by the player.
        self.player_shots = set()

        self._setup()

    def _setup(self):
        # -------------------------
        # Player fleet
        # -------------------------

        self.player.place_ship({
            (1, 1),
            (1, 2),
            (1, 3)
        })

        self.player.place_ship({
            (3, 1),
            (4, 1),
            (5, 1)
        })

        # -------------------------
        # Enemy fleet
        # -------------------------

        self.enemy.place_ship({
            (2, 2),
            (2, 3),
            (2, 4)
        })

        self.enemy.place_ship({
            (4, 1),
            (5, 1)
        })

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print(
            "Enemy ship cells remaining:",
            self.enemy.remaining_cells()
        )

    def run(self):
        print("Battleship")

        while True:
            self.show()

            raw = input("> ").strip().lower()

            # -------------------------
            # Quit
            # -------------------------

            if raw == "q":
                print("Game ended.")
                return

            # -------------------------
            # Parse player coordinate
            # -------------------------

            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue

            # -------------------------
            # Validate coordinate
            # -------------------------

            if not (
                0 <= pos[0] < Board.SIZE
                and 0 <= pos[1] < Board.SIZE
            ):
                print("Outside board.")
                continue

            # -------------------------
            # Prevent repeated player shot
            # -------------------------

            if pos in self.player_shots:
                print("Already fired there.")
                continue

            self.player_shots.add(pos)

            # -------------------------
            # Player fires
            # -------------------------

            result = self.enemy.fire(pos)

            # Print exactly ONE result for this shot.
            if result["result"] == "hit":
                print("HIT!")

            elif result["result"] == "miss":
                print("MISS!")

            elif result["result"] == "sunk":
                print("HIT!")
                print("You sank a ship!")

            # A repeat should never reach here because
            # player_shots prevents it.
            elif result["result"] == "repeat":
                print("Already fired there.")
                continue

            # -------------------------
            # Check player victory
            # -------------------------

            if self.enemy.all_sunk():
                print("You sank the entire fleet!")
                return

            # -------------------------
            # AI chooses a coordinate
            # -------------------------

            ai_pos = self.ai.choose()

            if ai_pos is None:
                print("AI has no remaining coordinates.")
                return

            # Convert AI's coordinate string into
            # the internal zero-based representation.
            try:
                ar, ac = map(int, ai_pos.split(","))
                player_pos = (ar - 1, ac - 1)
            except ValueError:
                continue

            # -------------------------
            # AI fires
            # -------------------------

            print("AI fired at", ai_pos)

            ai_result = self.player.fire(player_pos)

            # Print exactly ONE result for the AI's shot.
            if ai_result["result"] == "hit":
                print("AI scored a hit.")

                # Tell the AI about the successful shot
                # so it can prioritize nearby cells.
                self.ai.register_hit(player_pos)

            elif ai_result["result"] == "miss":
                print("AI missed.")

            elif ai_result["result"] == "sunk":
                print("AI scored a hit.")
                print("AI sank one of your ships.")

                # A sunk shot is still a successful hit.
                self.ai.register_hit(player_pos)

            elif ai_result["result"] == "repeat":
                # AI should normally never reach this case
                # because ai.py tracks every tried coordinate.
                print("AI fired at a coordinate it already tried.")

            # -------------------------
            # Check AI victory
            # -------------------------

            if self.player.all_sunk():
                print("AI sank your entire fleet!")
                return
