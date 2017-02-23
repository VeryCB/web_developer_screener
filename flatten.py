def flatten(array):
    flattened = []

    for item in array:
        if isinstance(item, int):
            flattened.append(item)
        else:
            flattened.extend(flatten(item))

    return flattened


def test_flatten():
    assert flatten([[1,2,[3]],4]) == [1,2,3,4]
