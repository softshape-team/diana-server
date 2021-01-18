from django.urls import reverse


def rvs(name, *, args=None, kwargs=None, params: dict = None):
    first = reverse(name, args=args, kwargs=kwargs)

    if params is None:
        return first

    second = "?"
    for param in params.items():
        second += f"{param[0]}={param[1]}&"

    second = second[:-1]
    return first + second
