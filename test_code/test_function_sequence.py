import functools
from typing import Callable

ComposableFunction = Callable[[float], float]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def func1(x: float) -> float:
    pass

def func2(x: float) -> float:
    pass

def main():
    x = 12
    myfunc = compose(func1, func2, func1, func2)
    result = myfunc(x)
