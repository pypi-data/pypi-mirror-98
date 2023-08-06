from cccalendar import _get_date_square_coordinates


def test_get_date_square_coordinates():
    # e.g. 01/01/2021
    day_of_week = 4  # Friday
    week_of_month = 0  # First week
    scale = 10  # Arbitrary
    corners, centre = _get_date_square_coordinates(day_of_week, week_of_month, scale)
    assert corners[0] == (40, 0)
    assert corners[1] == (40, 5)
    assert corners[2] == (45, 5)
    assert corners[3] == (45, 0)
    assert centre == (42.5, 2.5)

    # e.g. 30/11/2020
    day_of_week = 0  # Monday
    week_of_month = 5  # Sixth week
    scale = 10  # Arbitrary
    corners, centre = _get_date_square_coordinates(day_of_week, week_of_month, scale)
    assert corners[0] == (0, 50)
    assert corners[1] == (0, 55)
    assert corners[2] == (5, 55)
    assert corners[3] == (5, 50)
    assert centre == (2.5, 52.5)
