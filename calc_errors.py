class CalculatorError(Exception):
    # Базовый класс для всех ошибок калькулятора
    pass



class TokenizationError(CalculatorError):
    # Ошибка c неизвестным символом
    def __init__(self, message, position=None, symbol=None):
        self.message = message
        self.position = position
        self.symbol = symbol
        if position is not None and symbol is not None:
            super().__init__(f"Ошибка! {message}: {symbol}")
        elif symbol is not None:
            super().__init__(f"Ошибка! {message}: {symbol}")
        else:
            super().__init__(f"Ошибка! {message}")

class MultipleUnaryOperatorsError(TokenizationError):
    # Несколько унарных операторов в начале выражения
    def __init__(self):
        super().__init__("В начале выражения не может быть более одного унарного оператора '+' или '-'")


class InvalidFloatFormatError(TokenizationError):
    # Неверный формат числа типа Float
    def __init__(self, number_string):
        super().__init__(f"Неверный формат числа типа Float. {number_string}")





class EvaluationError(CalculatorError):
    # Ошибка вычисления
    def __init__(self, message, operator=None):
        self.message = message
        self.operator = operator
        if operator is not None:
            super().__init__(f"Ошибка вычисления! {message} оператор: '{operator}'")
        else:
            super().__init__(f"Ошибка вычисления! {message}")


class InsufficientOperandsError(EvaluationError):
    # Недостаточно операндов
    def __init__(self, operator, expected, actual):
        super().__init__(f"Недостаточно операндов. Ожидалось: {expected}, получено: {actual}", operator)

class FloatOperandError(EvaluationError):
    # Ошибка при использовании чисел типа Float в целочисленном делении
    def __init__(self):
        super().__init__("Целочисленное деление не поддерживает числа с плавающей точкой", "//")

class FloatOperandInModError(EvaluationError):
    # Ошибка при использовании чисел типа Float в операции взятия остатка
    def __init__(self):
        super().__init__("Операция взятия остатка не поддерживает числа с плавающей точкой", "%")





class MathError(CalculatorError):
    # Класс для математических ошибок
    def __init__(self, message):
        super().__init__(f"Математическая ошибка! {message}")

class DivisionByZeroError(MathError):
    # Ошибка деления на ноль
    def __init__(self):
        super().__init__("Деление на ноль.")

class IntegerDivisionByZeroError(MathError):
    # Ошибка целочисленного деления на ноль
    def __init__(self):
        super().__init__("Целочисленное деление на ноль")


class ParsingError(CalculatorError):
    # Ошибка парсинга
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        if token is not None:
            super().__init__(f"Ошибка парсинга! {message} (токен: '{token}')")
        else:
            super().__init__(f"Ошибка парсинга! {message}")

class TooManyOperatorsError(ParsingError):
    # 3 и более операторов подряд между числами
    def __init__(self):
        super().__init__("Не может быть трех и более операторов подряд")

class InvalidOperatorSequenceError(ParsingError):
    # Неверная последовательность двух операторов между числами
    def __init__(self):
        super().__init__("Если между числами два оператора, второй должен быть унарным")




















class InvalidNumberFormatError(TokenizationError):
    """Неверный формат числа"""
    def __init__(self, number_string):
        super().__init__(f"Неверный формат числа: '{number_string}'")

class UnbalancedParenthesesError(ParsingError):
    """Несбалансированные скобки"""
    def __init__(self):
        super().__init__("Несбалансированные скобки")

class UnknownTokenError(ParsingError):
    """Неизвестный токен"""
    def __init__(self, token):
        super().__init__("Неизвестный токен", token)

class UnknownOperatorError(ParsingError):
    """Неизвестный оператор"""
    def __init__(self, operator):
        super().__init__("Неизвестный оператор", operator)



class InvalidExpressionError(EvaluationError):
    """Некорректное выражение"""
    def __init__(self, reason="в стеке осталось более одного значения"):
        super().__init__(f"Некорректное выражение: {reason}")