from board_helpers.board_consts import TileType, BOARD
from board_helpers.move_info import MoveInfo
from typing import Dict

class TilesCoutner:
    def __init__(self, location: str, move: str) -> None:
        info = MoveInfo(location, move)
        self.x = info.x
        self.y = info.y
        self.isVertical = info.isVertical
        self.left = len(move)


    def __call__(self) -> Dict[TileType, int]:
        result = {type: 0 for type in TileType}
        while(self.left > 0 and self.__is_in_bounds()):
            result[BOARD[self.__x_dis()][self.__y_dis()]] += 1
            self.__step()
        return result


    def __step(self) -> None:
        if self.isVertical:
            self.y+=1
        else:
            self.x+=1
        self.left-=1

    def __x_dis(self, other_x = 8) -> int:
        return abs(self.x - other_x)


    def __y_dis(self, other_y = 8) -> int:
        return abs(self.y - other_y)
    
    def __is_in_bounds(self) -> bool:
        return 0 <= self.x <= 15 and 0 <= self.y <= 15