"""
オセロの石の色を表す値オブジェクト
"""
from enum import Enum


class StoneColor(Enum):
    """オセロの石の色を表すEnum"""
    
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def opposite(self) -> 'StoneColor':
        """相手の色を返す"""
        if self == StoneColor.BLACK:
            return StoneColor.WHITE
        elif self == StoneColor.WHITE:
            return StoneColor.BLACK
        else:
            raise ValueError(f"EMPTYには相手の色がありません: {self}")
    
    def __str__(self) -> str:
        """文字列表現を返す"""
        name_mapping = {
            StoneColor.EMPTY: "空",
            StoneColor.BLACK: "黒",
            StoneColor.WHITE: "白"
        }
        return name_mapping[self]
    
    def is_player(self) -> bool:
        """プレイヤーの石かどうかを判定"""
        return self in (StoneColor.BLACK, StoneColor.WHITE)