import pytest

from OrodaelTurrim.Structure.Position import OffsetPosition


@pytest.mark.parametrize('position,result', [
    (OffsetPosition(0, 0), [OffsetPosition(0, -1), OffsetPosition(1, -1),
                            OffsetPosition(1, 0), OffsetPosition(0, 1),
                            OffsetPosition(-1, 0), OffsetPosition(-1, -1)]),
    (OffsetPosition(-4, 4), [OffsetPosition(-4, 3), OffsetPosition(-3, 3),
                             OffsetPosition(-3, 4), OffsetPosition(-4, 5),
                             OffsetPosition(-5, 4), OffsetPosition(-5, 3)]),
    (OffsetPosition(-5, 5), [OffsetPosition(-5, 4), OffsetPosition(-4, 5),
                             OffsetPosition(-4, 6), OffsetPosition(-5, 6),
                             OffsetPosition(-6, 6), OffsetPosition(-6, 5)])
])
def test_neighbour_offset(position, result):
    assert position.get_all_neighbours() == result
