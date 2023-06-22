import operator
import random


def generate_operation():
    """Generate a random arithmetic operation and its result."""
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv
    }
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(list(ops.keys()))
    result = ops[op](num1, num2)
    return f"{num1} {op} {num2}", result


def verify_answer(answer, session):
    """Verify if the provided answer matches the stored result."""
    return session.get('result') == int(answer)
