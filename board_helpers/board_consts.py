from enum import Enum

TileType = Enum('TileType', ['N', 'L2', 'L3', 'W2', 'W3'])


BOARD = [
            [TileType.N,  TileType.N,  TileType.N,  TileType.N,  TileType.L2, TileType.N,  TileType.N,  TileType.W3,],
            [TileType.N,  TileType.L2, TileType.N,  TileType.N,  TileType.N,  TileType.L2, TileType.N,  TileType.N,],
            [TileType.N,  TileType.N,  TileType.L3, TileType.N,  TileType.N,  TileType.N,  TileType.L3, TileType.N,],
            [TileType.N,  TileType.N,  TileType.N,  TileType.W2, TileType.N,  TileType.N,  TileType.N,  TileType.N,],
            [TileType.L2, TileType.N,  TileType.N,  TileType.N,  TileType.W2, TileType.N,  TileType.N,  TileType.L2,],
            [TileType.N,  TileType.L2, TileType.N,  TileType.N,  TileType.N,  TileType.W2, TileType.N , TileType.N,],
            [TileType.N,  TileType.N,  TileType.L3, TileType.N,  TileType.N,  TileType.N,  TileType.W2, TileType.N,],
            [TileType.W3, TileType.N,  TileType.N,  TileType.N,  TileType.L2, TileType.N,  TileType.N,  TileType.W3,],

        ]