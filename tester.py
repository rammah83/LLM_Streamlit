# exemple of use kwargs in function
def test(**kwargs):
    print(*kwargs)


my_dict = {"a": 1, "b": 2, "c": 3}
test(**my_dict)
