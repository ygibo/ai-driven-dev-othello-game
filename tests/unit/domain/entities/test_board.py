"""
Boardエンティティのテストコード
"""
import pytest
from typing import List
from src.domain.entities.board import Board
from src.domain.value_objects.stone_color import StoneColor


class TestBoard:
    """Boardエンティティのテストクラス"""
    
    def test_init_creates_empty_board_with_initial_stones(self):
        """初期化時に空のボードが作成され、初期石が配置されることを確認"""
        board = Board()
        
        # ボードサイズの確認
        board_state = board.get_board()
        assert len(board_state) == 8
        assert all(len(row) == 8 for row in board_state)
        
        # 初期石の配置を確認
        assert board.get_cell_state(3, 3) == StoneColor.WHITE
        assert board.get_cell_state(3, 4) == StoneColor.BLACK
        assert board.get_cell_state(4, 3) == StoneColor.BLACK
        assert board.get_cell_state(4, 4) == StoneColor.WHITE
        
        # 初期石以外は空であることを確認
        empty_count = board.get_stone_count(StoneColor.EMPTY)
        assert empty_count == 64 - 4  # 全64マス - 初期石4個
    
    def test_put_valid_position_places_stone(self):
        """有効な位置に石を置くことができることを確認"""
        board = Board()
        
        # 空の位置に石を置く
        board.put(2, 3, StoneColor.BLACK)
        
        assert board.get_cell_state(2, 3) == StoneColor.BLACK
        assert board.get_stone_count(StoneColor.BLACK) == 3  # 初期2個 + 1個
    
    def test_put_invalid_position_raises_error(self):
        """無効な位置に石を置こうとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.put(-1, 0, StoneColor.BLACK)
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.put(8, 0, StoneColor.BLACK)
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.put(0, -1, StoneColor.BLACK)
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.put(0, 8, StoneColor.BLACK)
    
    def test_put_occupied_position_raises_error(self):
        """既に石が置かれた位置に石を置こうとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="既に石が置かれています"):
            board.put(3, 3, StoneColor.BLACK)  # 初期石が置かれている位置
    
    def test_put_empty_stone_raises_error(self):
        """EMPTYを石として置こうとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="プレイヤーの石ではありません"):
            board.put(2, 3, StoneColor.EMPTY)
    
    def test_reverse_valid_cells_flips_stones(self):
        """有効な位置の石を裏返すことができることを確認"""
        board = Board()
        
        # 初期状態で白石を黒石に裏返す
        board.reverse([(3, 3), (4, 4)])
        
        assert board.get_cell_state(3, 3) == StoneColor.BLACK
        assert board.get_cell_state(4, 4) == StoneColor.BLACK
        assert board.get_stone_count(StoneColor.BLACK) == 4
        assert board.get_stone_count(StoneColor.WHITE) == 0
    
    def test_reverse_invalid_position_raises_error(self):
        """無効な位置の石を裏返そうとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.reverse([(-1, 0)])
    
    def test_reverse_empty_cell_raises_error(self):
        """空のセルを裏返そうとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="裏返す石がありません"):
            board.reverse([(0, 0)])  # 空のセル
    
    def test_get_board_returns_copy(self):
        """get_board()がボード状態のコピーを返すことを確認"""
        board = Board()
        
        board_copy = board.get_board()
        
        # コピーを変更しても元のボードに影響しないことを確認
        board_copy[0][0] = StoneColor.BLACK
        assert board.get_cell_state(0, 0) == StoneColor.EMPTY
    
    def test_get_cell_state_valid_position(self):
        """有効な位置のセル状態を取得できることを確認"""
        board = Board()
        
        assert board.get_cell_state(3, 3) == StoneColor.WHITE
        assert board.get_cell_state(0, 0) == StoneColor.EMPTY
    
    def test_get_cell_state_invalid_position_raises_error(self):
        """無効な位置のセル状態を取得しようとするとエラーが発生することを確認"""
        board = Board()
        
        with pytest.raises(ValueError, match="無効な位置です"):
            board.get_cell_state(-1, 0)
    
    def test_is_empty_valid_positions(self):
        """is_empty()が正しく動作することを確認"""
        board = Board()
        
        # 空のセル
        assert board.is_empty(0, 0) is True
        
        # 石が置かれたセル
        assert board.is_empty(3, 3) is False
        
        # 無効な位置
        assert board.is_empty(-1, 0) is False
        assert board.is_empty(8, 0) is False
    
    def test_is_valid_position(self):
        """is_valid_position()が正しく動作することを確認"""
        board = Board()
        
        # 有効な位置
        assert board.is_valid_position(0, 0) is True
        assert board.is_valid_position(7, 7) is True
        assert board.is_valid_position(3, 4) is True
        
        # 無効な位置
        assert board.is_valid_position(-1, 0) is False
        assert board.is_valid_position(8, 0) is False
        assert board.is_valid_position(0, -1) is False
        assert board.is_valid_position(0, 8) is False
    
    def test_get_stone_count(self):
        """get_stone_count()が正しく動作することを確認"""
        board = Board()
        
        # 初期状態
        assert board.get_stone_count(StoneColor.BLACK) == 2
        assert board.get_stone_count(StoneColor.WHITE) == 2
        assert board.get_stone_count(StoneColor.EMPTY) == 60
        
        # 石を追加
        board.put(2, 3, StoneColor.BLACK)
        assert board.get_stone_count(StoneColor.BLACK) == 3
        assert board.get_stone_count(StoneColor.EMPTY) == 59
    
    def test_is_board_full(self):
        """is_board_full()が正しく動作することを確認"""
        board = Board()
        
        # 初期状態では満杯ではない
        assert board.is_board_full() is False
        
        # 全てのセルを埋める（実際には実装が困難なので、EMPTYの数を0にする状況をテスト）
        # テスト用に全セルに石を置く
        for row in range(8):
            for col in range(8):
                if board.is_empty(row, col):
                    board.put(row, col, StoneColor.BLACK)
        
        assert board.is_board_full() is True
    
    def test_board_size_constant(self):
        """BOARD_SIZE定数が正しく設定されていることを確認"""
        assert Board.BOARD_SIZE == 8
    
    def test_initial_stone_placement(self):
        """初期石の配置が正しいことを詳細に確認"""
        board = Board()
        
        # 中央4マスの確認
        assert board.get_cell_state(3, 3) == StoneColor.WHITE
        assert board.get_cell_state(3, 4) == StoneColor.BLACK
        assert board.get_cell_state(4, 3) == StoneColor.BLACK
        assert board.get_cell_state(4, 4) == StoneColor.WHITE
        
        # 中央4マス以外は空であることを確認
        for row in range(8):
            for col in range(8):
                if (row, col) not in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                    assert board.get_cell_state(row, col) == StoneColor.EMPTY
    
    def test_reverse_multiple_stones(self):
        """複数の石を一度に裏返すことができることを確認"""
        board = Board()
        
        # 複数の石を裏返す
        cells_to_reverse = [(3, 3), (3, 4), (4, 3)]
        board.reverse(cells_to_reverse)
        
        # 裏返った石の確認
        assert board.get_cell_state(3, 3) == StoneColor.BLACK  # WHITE -> BLACK
        assert board.get_cell_state(3, 4) == StoneColor.WHITE  # BLACK -> WHITE
        assert board.get_cell_state(4, 3) == StoneColor.WHITE  # BLACK -> WHITE
        
        # 裏返されなかった石の確認
        assert board.get_cell_state(4, 4) == StoneColor.WHITE  # 元のまま
    
    def test_reverse_empty_list(self):
        """空のリストでreverse()を呼び出してもエラーが発生しないことを確認"""
        board = Board()
        
        # 空のリストで裏返し処理を実行
        board.reverse([])
        
        # 初期状態と変わらないことを確認
        assert board.get_cell_state(3, 3) == StoneColor.WHITE
        assert board.get_cell_state(3, 4) == StoneColor.BLACK
        assert board.get_cell_state(4, 3) == StoneColor.BLACK
        assert board.get_cell_state(4, 4) == StoneColor.WHITE