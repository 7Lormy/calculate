from calc_errors import *
import re


def validate_operator(tokens):
    # Проверка корректности последовательности операторов между числами.

    operator_count = 0
    bracket_level = 0  # Уровень вложенности скобок

    for token in tokens:
        # Определяем тип токена
        is_number = token.replace('.', '').isdigit()
        is_binary_operator = token in ["+", "-", "*", "/", "|", "^", "%"]
        is_unary_operator = token in ["$", "~"]
        is_open_bracket = token == "("
        is_close_bracket = token == ")"

        if is_number:
            # Встретили число - сбрасываем счетчик операторов
            operator_count = 0
        elif is_open_bracket:
            # Открывающая скобка - сбрасываем счетчик и увеличиваем уровень вложенности
            operator_count = 0
            bracket_level += 1
        elif is_close_bracket:
            # Закрывающая скобка - сбрасываем счетчик и уменьшаем уровень вложенности
            operator_count = 0
            bracket_level -= 1
        elif is_binary_operator or is_unary_operator:
            operator_count += 1

            # Проверяем, что не более 2 операторов подряд (только если вне скобок)
            if operator_count >= 3 and bracket_level == 0:
                raise TooManyOperatorsError()

            # Если два оператора подряд вне скобок, проверяем, что второй - унарный
            if operator_count == 2 and bracket_level == 0 and not is_unary_operator:
                raise InvalidOperatorSequenceError()


def tokenize(expression):
    # Предварительная обработка выражения

    pattern = r'\d*\.?\d+\s+\d*\.?\d+' # ищем два числа, разделенные пробелами без оператора.
    if re.search(pattern, expression):
        raise TokenizationError("Между двумя числами отсутствует оператор")
    expr = expression.replace(" ", "").replace("**", "^").replace("//", "|")

    tokens = []
    current_token = ""
    if expr.startswith(('++', '--', '+-', '-+')):
        raise MultipleUnaryOperatorsError() # ошибка двух и более знаков в самом начале

    for i, char in enumerate(expr, 0):
        # Обработка скобок - всегда отдельные токены
        if char in "()":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
            continue

        # Обработка операторов (кроме + и - которые могут быть унарными)
        if char in "*/^|%":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
            continue

        # Обработка + и - которые могут быть унарными или бинарными
        if char in "+-":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            # Определяем унарный или бинарный оператор
            if not tokens or tokens[-1] in ["(", "+", "-", "*", "/", "^", "|", "$", "~", "%"]:
                # Унарный оператор
                tokens.append("$" if char == "+" else "~")
            else:
                # Бинарный оператор
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
            continue

        # Обработка чисел
        if char.isdigit() or char == ".":
            # Если предыдущий токен - унарный оператор, объединяем

            current_token += char
            continue
        raise TokenizationError("Неизвестный символ", i, char) # обработка ошибки с неизвестным символом
    # Добавляем последний токен
    if current_token:

        tokens.append(current_token)

    return tokens