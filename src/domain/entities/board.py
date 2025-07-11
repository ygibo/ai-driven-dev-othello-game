"""
オセロゲームのボード状態を管理するBoardエンティティ
"""
from typing import List, Tuple
from ..value_objects.stone_color import StoneColor


class Board:
    """オセロゲームのボード状態を管理するエンティティ"""
    
    BOARD_SIZE = 8
    
    def __init__(self):
        """ボードを初期化"""
        self._board: List[List[StoneColor]] = []
        self._initialize_board()
        self._set_initial_stones()
    
    def put(self, row: int, col: int, color: StoneColor) -> None:
        """指定位置に石を置く"""
        if not self.is_valid_position(row, col):
            raise ValueError(f"無効な位置です: ({row}, {col})")
        
        if not self.is_empty(row, col):
            raise ValueError(f"既に石が置かれています: ({row}, {col})")
        
        if not color.is_player():
            raise ValueError(f"プレイヤーの石ではありません: {color}")
        
        self._board[row][col] = color
    
    def reverse(self, cells: List[Tuple[int, int]]) -> None:
        """指定されたセルの石を裏返す"""
        for row, col in cells:
            if not self.is_valid_position(row, col):
                raise ValueError(f"無効な位置です: ({row}, {col})")
            
            current_color = self._board[row][col]
            if not current_color.is_player():
                raise ValueError(f"裏返す石がありません: ({row}, {col})")
            
            self._board[row][col] = current_color.opposite()
    
    def get_board(self) -> List[List[StoneColor]]:
        """ボード状態のコピーを返す"""
        return [row[:] for row in self._board]
    
    def get_cell_state(self, row: int, col: int) -> StoneColor:
        """指定位置の石の状態を取得"""
        if not self.is_valid_position(row, col):
            raise ValueError(f"無効な位置です: ({row}, {col})")
        
        return self._board[row][col]
    
    def is_empty(self, row: int, col: int) -> bool:
        """指定位置が空かどうかを判定"""
        if not self.is_valid_position(row, col):
            return False
        
        return self._board[row][col] == StoneColor.EMPTY
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """指定位置が有効かどうかを判定"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def get_stone_count(self, color: StoneColor) -> int:
        """指定色の石の数を取得"""
        count = 0
        for row in self._board:
            for cell in row:
                if cell == color:
                    count += 1
        return count
    
    def is_board_full(self) -> bool:
        """ボードが満杯かどうかを判定"""
        return self.get_stone_count(StoneColor.EMPTY) == 0
    
    def _initialize_board(self) -> None:
        """ボードを空の状態で初期化"""
        self._board = []
        for _ in range(self.BOARD_SIZE):
            row = [StoneColor.EMPTY] * self.BOARD_SIZE
            self._board.append(row)
    
    def _set_initial_stones(self) -> None:
        """初期配置の石を設定"""
        # 中央4マスに白黒2個ずつ配置
        # [3][3] = WHITE, [3][4] = BLACK
        # [4][3] = BLACK, [4][4] = WHITE
        center = self.BOARD_SIZE // 2
        self._board[center - 1][center - 1] = StoneColor.WHITE
        self._board[center - 1][center] = StoneColor.BLACK
        self._board[center][center - 1] = StoneColor.BLACK
        self._board[center][center] = StoneColor.WHITE