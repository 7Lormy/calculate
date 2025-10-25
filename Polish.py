from calc_errors import *

def Polish(tokens):
    output = []
    stack = []
    priority = {"-": 1, "+": 1, "*": 2, "/": 2, "%": 2, "|": 2, "^": 3, "~": 4, "$": 4}
    flag = True
    for token in tokens:
        if token.isdigit() or token.replace(".", "").isdigit():
            output.append(token)
            flag = False
        elif token == "-" and flag:
            stack.append("~")
            flag = True
        elif token == "+" and flag:
            stack.append("$")
            flag = True
        elif token in ["+", "/", "-", "*", "|", "^", "%"]:
            # Бинарные операторы. Выталкиваем операторы с высшим или равным приоритетом
            # Учитываем ассоциативность: ^ - правоассоциативен, остальные - левоассоциативны
            while (stack and stack[-1] != "(" and stack[-1] in priority and
                   (priority[stack[-1]] > priority[token] or
                    (priority[stack[-1]] == priority[token] and token != "^"))):
                output.append(stack.pop())
            stack.append(token)
            flag = True
        elif token in ["$", "~"]:
            # 100% унарные
            stack.append(token)
            flag = True
        elif token == "(":
            stack.append(token)
            flag = True
        elif token == ")":
            # Закрывающая скобка, выталкиваем до открывающей
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop() # Убираем открывающую скобку
            else:
                raise UnbalancedParenthesesError()
            flag = False
        else:
            raise UnknownTokenError(token)
    # Выталкиваем оставшиеся операторы из стека
    while stack:
        if stack[-1] == "(":
            raise UnbalancedParenthesesError()
        output.append(stack.pop())
    return output