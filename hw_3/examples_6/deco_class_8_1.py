class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


@CountCalls  # вызывается без () т к ф-ция передается при инициализации класса
def say_hi():
    print("Hi!")


say_hi()
say_hi()
say_hi()

# f ' <text> { <expression> <optional !s, !r, or !a> <optional : format specifier> } <text>
"""!r' calls repr() on the expression, and '!a' calls ascii() 
on the expression. These conversions are applied before the call 
to format(). The only reason to use '!s' is if you want to specify 
a format specifier that applies to str, not to the type of the 
expression."""