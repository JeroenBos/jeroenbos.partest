from typeguard import typeguard_ignore


def give_me_an_int(i: int):
    return i


@typeguard_ignore
def unguarded_give_me_an_int(i: int):
    return i
