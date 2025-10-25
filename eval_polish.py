from calc_errors import *

def eval_polish(rpn_tokens):

    stack = []

    for token in rpn_tokens:
        if token.isdigit() or token.replace('.', '').isdigit():
            # Число - кладем в стек
            stack.append(float(token))
        elif token == '~':
            # Унарный минус - берем один операнд
            if len(stack) < 1:
                raise InsufficientOperandsError("унарный минус", 1, len(stack))
            left = stack.pop()
            stack.append(-left)
        elif token == '$':
            # Унарный плюс - просто возвращает число (ничего не меняет)
            if len(stack) < 1:
                raise InsufficientOperandsError("унарный плюс", 1, len(stack))
            left = stack.pop()
            stack.append(left)
        else:
            # Бинарный оператор - берем два операнда
            if len(stack) < 2:
                raise InsufficientOperandsError(token, 2, len(stack))
            right = stack.pop()
            left = stack.pop()

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == "%":
                if left == 0:
                    raise DivisionByZeroError()

                if not (left.is_integer() and right.is_integer()):
                    raise FloatOperandInModError()

                result = left % right
            elif token == '/':
                if right == 0:
                    raise DivisionByZeroError() # ошибка деления на ноль
                result = left / right
            elif token == '|':
                # Целочисленное деление

                if right == 0:
                    raise IntegerDivisionByZeroError()

                if not (left.is_integer() and right.is_integer()):
                    raise FloatOperandError()

                result = float(int(left) // int(right))
                result = float(left // right)  # Используем оператор целочисленного деления
            elif token == '^':
                result = left ** right
            else:
                raise UnknownOperatorError(token)

            stack.append(result)

    if len(stack) != 1:
        raise InvalidExpressionError()

    return stack[0]