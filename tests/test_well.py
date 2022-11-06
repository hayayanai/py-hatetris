import pytest
from src.well import Well


class TestWell:

    @pytest.fixture
    def field_filled_one(self) -> Well:
        field = Well()
        for x in range(Well.WIDTH):
            field.cellses[0][x].landed = True
        field.cellses[1][2].landed = True
        yield field

    @pytest.fixture
    def field_filled_two(self):
        field = Well()
        for x in range(Well.WIDTH):
            field.cellses[0][x].landed = True
            field.cellses[1][x].landed = True
        field.cellses[2][2].landed = True
        return field

    @pytest.fixture
    def field_heights(self):
        """
        ..#.
        ..#.
        ..##
        ..#.
        """
        field = Well()
        for y in range(4):
            field.cellses[y][2].landed = True
        field.cellses[1][3].landed = True
        return field

    @pytest.fixture
    def field_michael(self):
        board_blueprint = [
            "          ",
            "          ",
            "          ",
            "          ",
            "          ",
            "          ",
            "          ",
            "   ##     ",
            "   ##    #",
            "   ##    #",
            "   ###   #",
            "# ##### ##",
            "# ### # ##",
            "# ########",
            "# ####### ",
            "#### #####",
            " ####   ##",
            " #########",
            " #########",
            " #########",
        ]
        field = Well()
        board_blueprint.reverse()
        for y in range(len(board_blueprint)):
            for x in range(Well.WIDTH):
                field.at(x, y).landed = True if board_blueprint[y][x] == "#" else False
        return field

    @pytest.mark.parametrize(
        "y, x, expected",
        [
            (0, 3, False),
            (0, 2, True),
            (1, 2, False)
        ]
    )
    def test_delete_a_line(self, field_filled_one: Well, y, x, expected):
        field_filled_one.delete_lines()
        assert field_filled_one.cellses[y][x].landed is expected

    @pytest.mark.parametrize(
        "y, x, expected",
        [
            (0, 3, False),
            (0, 2, True),
            (1, 2, False),
            (2, 2, False)
        ]
    )
    def test_delete_lines(self, field_filled_two: Well, y, x, expected):
        field_filled_two.delete_lines()
        assert field_filled_two.cellses[y][x].landed is expected

    @pytest.mark.parametrize(
        "x, expected",
        [
            (0, 0),
            (1, 0),
            (2, 4),
            (3, 2),
            (4, 0)
        ]
    )
    def test_get_column_heights(self, field_heights: Well, x, expected):
        lis = field_heights.get_column_heights()
        assert lis[x] == expected

    def test_get_holes(self, field_heights: Well):
        assert field_heights.get_holes() == 1

    def test_get_holes2(self, field_michael: Well):
        assert field_michael.get_holes() == 10

    def test_get_row_transitions(self, field_michael: Well):
        assert field_michael.get_row_transitions() == 44

    def test_get_column_transitions(self, field_michael: Well):
        assert field_michael.get_column_transitions() == 14

    def test_get_cumulative_wells(self, field_michael: Well):
        assert field_michael.get_cumulative_wells() == 6

    def test_get_bumpiness(self, field_michael: Well):
        assert field_michael.get_bumpiness() == 23

    def test_get_aggregate_height(self, field_michael: Well):
        assert sum(field_michael.get_column_heights()) == 96

    def test_rows_cleared(self, field_michael: Well):
        assert field_michael.delete_lines() == 0
