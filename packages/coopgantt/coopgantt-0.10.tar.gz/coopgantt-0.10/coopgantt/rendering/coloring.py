import random as rnd


def random_color():
    """
    http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
    """
    # r = lambda: random.randint(0,255)
    # return '#%02X%02X%02X' % (r(),r(),r())

    return rnd.sample(['#95F9C3', '#7ED9B4', '#67B9A4', '#509995', '#397885',  '#225876', '#0B3866'], 1)[0]