class Board:
    SIZE = 6

    def __init__(self):
        # Each ship is stored as a separate set of coordinates.
        self.ships = []

        # All coordinates that have been fired at.
        self.shots = set()

        # Coordinates that actually hit a ship.
        self.hit_cells = set()

    def place_ship(self, cells):
        """Add a new ship to the board."""
        ship = set(cells)
        self.ships.append(ship)

    def fire(self, pos):
        """
        Fire at a coordinate.

        Returns:
            repeat -> coordinate was already fired at
            hit    -> ship was hit but not sunk
            sunk   -> the ship was completely destroyed
            miss   -> no ship at the coordinate
        """

        # Prevent repeated shots.
        if pos in self.shots:
            return {
                "result": "repeat",
                "ship": None
            }

        self.shots.add(pos)

        # Check every ship individually.
        for ship in self.ships:
            if pos in ship:
                self.hit_cells.add(pos)

                # Check whether this particular ship is completely hit.
                if ship <= self.hit_cells:
                    return {
                        "result": "sunk",
                        "ship": ship
                    }

                return {
                    "result": "hit",
                    "ship": ship
                }

        return {
            "result": "miss",
            "ship": None
        }

    def all_sunk(self):
        """Return True when every ship has been completely destroyed."""
        return all(ship <= self.hit_cells for ship in self.ships)

    def sunk_ships(self):
        """Return a list of ships that have been completely destroyed."""
        return [
            ship for ship in self.ships
            if ship <= self.hit_cells
        ]

    def remaining_cells(self):
        """Return the total number of enemy ship cells not yet hit."""
        return sum(
            len(ship - self.hit_cells)
            for ship in self.ships
        )
