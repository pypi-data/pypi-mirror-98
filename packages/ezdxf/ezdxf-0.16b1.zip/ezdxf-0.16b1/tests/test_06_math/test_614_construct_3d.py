# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
import pytest

from ezdxf.math import (
    is_planar_face, Vec3, Vec2, subdivide_face, intersection_ray_ray_3d,
    normal_vector_3p, X_AXIS, Y_AXIS, Z_AXIS, subdivide_ngons,
    distance_point_line_3d,
)

from ezdxf.render.forms import square, circle

REGULAR_FACE = Vec3.list([(0, 0, 0), (1, 0, 1), (1, 1, 1), (0, 1, 0)])
IRREGULAR_FACE = Vec3.list([(0, 0, 0), (1, 0, 1), (1, 1, 0), (0, 1, 0)])
REGULAR_FACE_WRONG_ORDER = Vec3.list(
    [(0, 0, 0), (1, 1, 1), (1, 0, 1), (0, 1, 0)])


def test_face_count():
    assert is_planar_face(REGULAR_FACE[:3]) is True
    assert is_planar_face(REGULAR_FACE[:2]) is False


def test_regular_face():
    assert is_planar_face(REGULAR_FACE) is True


def test_irregular_face():
    assert is_planar_face(IRREGULAR_FACE) is False


def test_does_not_detect_wrong_order():
    assert is_planar_face(REGULAR_FACE_WRONG_ORDER) is True


def test_subdivide_square_in_quads():
    b = square(2)
    result = list(subdivide_face(b, quads=True))
    assert len(result) == 4
    assert result[0] == ((0, 0), (1, 0), (1, 1), (0, 1))


def test_subdivide_square_in_triangles():
    b = square(2)
    result = list(subdivide_face(b, quads=False))
    assert len(result) == 8
    assert result[0] == ((0, 1), (0, 0), (1, 1))
    assert result[1] == ((0, 0), (1, 0), (1, 1))


def test_subdivide_triangle():
    t = Vec3.list([(0, 0), (2, 0), (1, 2)])
    assert len(list(subdivide_face(t, quads=True))) == 3
    assert len(list(subdivide_face(t, quads=False))) == 6


def test_subdivide_ngons():
    hexagon = list(circle(6))
    result = list(subdivide_ngons([hexagon]))
    assert len(result) == 6


def test_subdivide_vec2_square_in_quads():
    b = Vec2.list(square(2))
    result = list(subdivide_face(b, quads=True))
    assert len(result) == 4
    assert result[0] == ((0, 0), (1, 0), (1, 1), (0, 1))


def test_intersection_ray_ray_3d_1():
    ray1 = (Vec3(0, 0, 0), Vec3(1, 0, 0))
    ray2 = (Vec3(0, 0, 0), Vec3(0, 0, 1))

    # parallel rays return a 0-tuple
    result = intersection_ray_ray_3d(ray1, ray1)
    assert len(result) == 0
    assert bool(result) is False

    # intersecting rays return a 1-tuple
    result = intersection_ray_ray_3d(ray1, ray2)
    assert len(result) == 1
    assert bool(result) is True
    assert result == (Vec3(0, 0, 0),)

    # not intersecting and not parallel rays return a 2-tuple
    line3 = (Vec3(0, 0, 1), Vec3(0, 1, 1))
    result = intersection_ray_ray_3d(ray1, line3)
    assert len(result) == 2
    assert bool(result) is True
    # returns points of closest approach on each ray
    assert Vec3(0, 0, 1) in result
    assert Vec3(0, 0, 0) in result


def test_intersection_ray_ray_3d_2():
    ray1 = (Vec3(1, 0, 0), Vec3(1, 1, 0))
    ray2 = (Vec3(0, 0.5, 0), Vec3(1, 0.5, 0))
    result = intersection_ray_ray_3d(ray1, ray2)
    assert len(result) == 1


def test_intersection_ray_ray_3d_random():
    for _ in range(5):
        intersection_point = Vec3.random(5)
        ray1 = (intersection_point, intersection_point + Vec3.random())
        ray2 = (intersection_point, intersection_point - Vec3.random())

        result = intersection_ray_ray_3d(ray1, ray2)
        assert len(result) == 1
        assert result[0].isclose(intersection_point)


def test_normal_vector_for_3_points():
    # normal_vector_3p(a, b, c)
    # a->b = v1
    # a->c = v2
    o = Vec3(0, 0, 0)
    assert normal_vector_3p(o, X_AXIS, Y_AXIS) == Z_AXIS
    assert normal_vector_3p(o, Y_AXIS, X_AXIS) == -Z_AXIS
    assert normal_vector_3p(o, Z_AXIS, X_AXIS) == Y_AXIS
    assert normal_vector_3p(o, X_AXIS, Z_AXIS) == -Y_AXIS
    assert normal_vector_3p(o, Y_AXIS, Z_AXIS) == X_AXIS
    assert normal_vector_3p(o, Z_AXIS, Y_AXIS) == -X_AXIS


@pytest.mark.parametrize('points, expected', [
    ([(10, 3), (0, 0), (1, 0)], 3),  # left of line
    ([(-10, 0), (0, 0), (1, 0)], 0),  # on line
    ([(2, -4), (0, 0), (1, 0)], 4),  # right of line
    ([(5, 0), (0, 5), (0, 2)], 5),
    ([(1, 0, 1), (1, 1, 1), (0, 0, 0)], 0.8164965809277259),
])
def test_distance_point_line_3d(points, expected):
    p, a, b = Vec3.generate(points)
    assert distance_point_line_3d(p, a, b) == pytest.approx(expected)


if __name__ == '__main__':
    pytest.main([__file__])
