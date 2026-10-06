import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()

        # Coordinates where the AI has scored a hit.
        self.hits = set()

    def choose(self):
        # First, look for untried cells adjacent to previous hits.
        adjacent_options = set()

        for r, c in self.hits:
            neighbors = [
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1)
            ]

            for pos in neighbors:
                if (
                    0 <= pos[0] < self.size
                    and 0 <= pos[1] < self.size
                    and pos not in self.tried
                ):
                    adjacent_options.add(pos)

        # Prefer a cell next to a previous hit.
        if adjacent_options:
            pos = random.choice(list(adjacent_options))

        else:
            # If there are no useful adjacent cells,
            # choose from every remaining untried cell.
            options = [
                (r, c)
                for r in range(self.size)
                for c in range(self.size)
                if (r, c) not in self.tried
            ]

            # No cells left to fire at.
            if not options:
                return None

            pos = random.choice(options)

        # Mark the coordinate as tried before returning it.
        self.tried.add(pos)

        return f"{pos[0] + 1},{pos[1] + 1}"

    def register_hit(self, pos):
        """Tell the AI that its previous shot was a hit."""
        self.hits.add(pos)
