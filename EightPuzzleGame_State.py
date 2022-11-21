import numpy as np


class State:
    tile_seq = []
    depth = 0
    weight = 0

    def __init__(self, tile_seq=[], depth=0, weight=0, parent=None):
        self.tile_seq = tile_seq
        self.depth = depth
        self.weight = weight
        self.parent = parent

    def getTile_1d(self):
        tiles = np.zeros(len(self.tile_seq) * len(self.tile_seq[0]))
        index = 0
        for row in self.tile_seq:
            for item in row:
                # tiles[index] = item
                index += 1
        return tiles

    def equals(self, obj):
        op = obj.tile_seq
        comparison = self.tile_seq == op
        return comparison.all()

    def get_tiles(self):
        return self.tile_seq

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node != None:
            path_back.append(node.tile_seq.copy())
            node = node.parent
        return list(reversed(path_back))

    def check_solvability(self):
        """ Checks if the given state is solvable """
        tiles = self.tile_seq.copy().flatten()
        inversion = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if (tiles[i] > tiles[j]) and tiles[i] != 0 and tiles[j] != 0:
                    inversion += 1

        return (inversion, inversion % 2 == 0)