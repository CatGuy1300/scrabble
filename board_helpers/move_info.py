from typing import Tuple
import string

CapitalLetter = str

class MoveInfo:
    def __init__(self, location: str, move: str) -> None:
        self.move = move
        self.x, self.y, self.isVertical = self.__extract_info(location)

    def __extract_info(self, location: str) -> Tuple[int, int, bool]:
        if location[0] in string.ascii_letters:
            return self.__capital_letter_to_num(location[0]), int(location[1:]), True
        else:
            return self.__capital_letter_to_num(location[-1]), int(location[:-1]), False
        
    def __capital_letter_to_num(self, letter: CapitalLetter) -> int:
        return ord(letter) - ord('A') + 1
