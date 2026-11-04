from decorators import even_check


@even_check
def add(a, b):
    return a + b


@even_check
def multiply(a, b):
    return a * b
