from ZNS.structure.Position import *
import pytest


@pytest.mark.parametrize('cube,offset', [
    (CubicPosition(-2, 3, -1), OffsetPosition(-2, -2)),
    (CubicPosition(-2, -1, 3), OffsetPosition(-2, +2)),
    (CubicPosition(2, -3, 1), OffsetPosition(2, 2)),
    (CubicPosition(2, 1, -3), OffsetPosition(2, -2)),
    (CubicPosition(0, 0, 0), OffsetPosition(0, 0))
])
def test_cubic_to_offset(cube, offset):
    assert cube.offset == offset


@pytest.mark.parametrize('cube,offset', [
    (CubicPosition(-2, 3, -1), OffsetPosition(-2, -2)),
    (CubicPosition(-2, -1, 3), OffsetPosition(-2, +2)),
    (CubicPosition(2, -3, 1), OffsetPosition(2, 2)),
    (CubicPosition(2, 1, -3), OffsetPosition(2, -2)),
    (CubicPosition(0, 0, 0), OffsetPosition(0, 0))
])
def test_offset_to_cubic(cube, offset):
    assert offset.cubic == cube


@pytest.mark.parametrize('cube,axial', [
    (CubicPosition(-2, 2, 0), AxialPosition(-2, 0)),
    (CubicPosition(-2, 0, 2), AxialPosition(-2, 2)),
    (CubicPosition(2, -2, 0), AxialPosition(2, 0)),
    (CubicPosition(+2, 0, -2), AxialPosition(+2, -2)),
    (CubicPosition(0, 0, 0), AxialPosition(0, 0))
])
def test_axial_to_cubic(cube, axial):
    assert axial.cubic == cube


@pytest.mark.parametrize('cube,axial', [
    (CubicPosition(-2, 2, 0), AxialPosition(-2, 0)),
    (CubicPosition(-2, 0, 2), AxialPosition(-2, 2)),
    (CubicPosition(2, -2, 0), AxialPosition(2, 0)),
    (CubicPosition(+2, 0, -2), AxialPosition(+2, -2)),
    (CubicPosition(0, 0, 0), AxialPosition(0, 0))
])
def test_cubic_to_axial(cube, axial):
    assert axial == cube.axial
