import pytest

from Well import Well


class TestWell:

    @pytest.fixture
    def field_filled_one(self) -> Well:
        field = Well()
        for x in range(Well.wellWidth):
            field.cellses[0][x].landed = True
        field.cellses[1][2].landed = True
        yield field

    @pytest.fixture
    def field_filled_two(self):
        field = Well()
        for x in range(Well.wellWidth):
            field.cellses[0][x].landed = True
            field.cellses[1][x].landed = True
        field.cellses[2][2].landed = True
        return field

    @pytest.fixture
    def field_heights(self):
        field = Well()
        for y in range(4):
            field.cellses[y][2].landed = True
        field.cellses[1][3].landed = True
        return field.get_column_heights()

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
            (2, 3),
            (3, 1),
            (4, 0)
        ]
    )
    def test_get_column_heights(self, field_heights: list, x, expected):
        assert field_heights[x] == expected
