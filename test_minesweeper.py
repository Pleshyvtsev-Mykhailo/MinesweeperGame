import pytest
from unittest.mock import patch
from main import Cell, Board

@pytest.fixture
def clean_cell():
    """Фікстура для створення чистої клітинки перед кожним тестом"""
    return Cell(0, 0)

@pytest.fixture
def small_board():
    """Фікстура для створення невеликого ігрового поля 3х3 з 2 мінами"""
    return Board(rows=3, cols=3, num_mines=2)

@pytest.mark.cell_logic
def test_cell_initial_state(clean_cell):
    """Перевірка базового стану клітинки після створення"""
    assert clean_cell.is_mine is False
    assert clean_cell.is_revealed is False
    assert clean_cell.is_flagged is False
    assert clean_cell.neighbor_mines == 0

@pytest.mark.cell_logic
def test_toggle_flag(clean_cell):
    """Перевірка встановлення та зняття прапорця"""
    clean_cell.toggle_flag()
    assert clean_cell.is_flagged is True
    clean_cell.toggle_flag()
    assert clean_cell.is_flagged is False

@pytest.mark.parametrize("initial_flag, expected_reveal", [
    (True, False),
    (False, True)
])

@pytest.mark.logic
def test_reveal_with_flags(clean_cell, initial_flag, expected_reveal):
    """Параметризований тест: перевірка, чи відкривається клітинка залежно від прапорця"""
    if initial_flag:
        clean_cell.toggle_flag()
    
    clean_cell.reveal()
    assert clean_cell.is_revealed == expected_reveal

@pytest.mark.logic
def test_calculate_neighbors_with_mock(small_board):
    """
    Тест із мокуванням: фіксуємо вихідні значення random.randint,
    щоб міни гарантовано лягли в координати (0,0) та (0,1).
    Це дозволяє точно перевірити математику підрахунку сусідів.
    """
    with patch('random.randint', side_effect=[0, 0, 0, 1]):
        small_board.generate_mines(first_click_x=2, first_click_y=2)
    
    assert small_board.grid[0][1].neighbor_mines == 2