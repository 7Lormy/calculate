from calc_errors import *
from main import tokenize, Polish, eval_polish


def run_all_tests():
    # Запускаем все тесты и возвращает статистику
    print("=" * 50)
    print("ЗАПУСК ТЕСТОВ КАЛЬКУЛЯТОРА")
    print("=" * 50)

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    # Группы тестов
    test_groups = [
        (test_basic_operations, "Базовые операции"),
        (test_float_operations, "Операции с числами с плавающей точкой"),
        (test_unary_operators, "Унарные операторы"),
        (test_parentheses, "Работа со скобками"),
        (test_operator_priority, "Приоритет операторов"),
        (test_error_cases, "Обработка ошибок"),
        (test_edge_cases, "Крайние случаи")
    ]

    # Запуск всех групп тестов
    for test_function, group_name in test_groups:
        print(f"\n--- {group_name} ---")
        passed, failed = test_function()
        total_tests += (passed + failed)
        passed_tests += passed
        failed_tests += failed

    # Вывод итогов
    print("\n" + "=" * 50)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено: {passed_tests}")
    print(f"Провалено: {failed_tests}")
    print(f"Успешность: {passed_tests / max(total_tests, 1) * 100:.1f}%")
    print("=" * 50)

    return passed_tests == total_tests


def test_basic_operations():
    # Тесты базовых операций
    tests = [
        ("2+2", 4.0),
        ("5-3", 2.0),
        ("4*3", 12.0),
        ("10/2", 5.0),
        ("7%3", 1.0),
        ("7|2", 3.0),
        ("2^3", 8.0),
    ]
    return run_test_group(tests, "Базовые операции")


def test_float_operations():
    # Тесты операций с плавающей точкой
    tests = [
        ("2.5+3.5", 6.0),
        ("5.5-2.5", 3.0),
        ("2.5*4", 10.0),
        ("7.5/2.5", 3.0),
        ("3.14*2", 6.28),
    ]
    return run_test_group(tests, "Операции с числами с плавающей точкой")


def test_unary_operators():
    # Тесты унарных операторов
    tests = [
        ("+5", 5.0),
        ("-3", -3.0),
        ("2+-3", -1.0),
        ("-2*3", -6.0),
        ("+2*-3", -6.0),
        ("-(-3)", 3.0),
    ]
    return run_test_group(tests, "Унарные операторы")


def test_parentheses():
    # Тесты со скобками
    tests = [
        ("(2+3)*4", 20.0),
        ("2+(3*4)", 14.0),
        ("((2+3)*4)/2", 10.0),
        ("(1+2)*(3+4)", 21.0),
    ]
    return run_test_group(tests, "Работа со скобками")


def test_operator_priority():
    # Тесты приоритета операторов
    tests = [
        ("2+3*4", 14.0),
        ("2*3+4", 10.0),
        ("2+3*4-1", 13.0),
        ("2^3*2", 16.0),
        ("2*3^2", 18.0),
    ]
    return run_test_group(tests, "Приоритет операторов")


def test_error_cases():
    # Тесты обработки ошибок
    error_tests = [
        ("2/0", DivisionByZeroError),
        ("2|0", IntegerDivisionByZeroError),
        ("2.5|3", FloatOperandError),
        ("2.5%3", FloatOperandInModError),
        ("2 2", TokenizationError),
        ("(2+3", UnbalancedParenthesesError),
        ("2+3)", UnbalancedParenthesesError),
        ("2@3", TokenizationError),
    ]
    return run_error_test_group(error_tests, "Обработка ошибок")


def test_edge_cases():
    # Тесты крайних случаев
    tests = [
        ("0+0", 0.0),
        ("1*0", 0.0),
        ("0*5", 0.0),
        ("1^0", 1.0),
        ("0^5", 0.0),
        ("5%1", 0.0),
        ("1|1", 1.0),
    ]
    return run_test_group(tests, "Граничные случаи")


def run_test_group(tests, group_name):
    # Запускаем группу обычных тестов
    passed = 0
    failed = 0

    for expression, expected in tests:
        try:
            tokens = tokenize(expression)
            rpn = Polish(tokens)
            result = eval_polish(rpn)

            # Сравниваем с ожидаемым результатом (с учетом погрешности float)
            if abs(result - expected) < 1e-10:
                print(f"✓ {expression} = {expected}")
                passed += 1
            else:
                print(f"✗ {expression} = {result} (ожидалось {expected})")
                failed += 1

        except Exception as e:
            print(f"✗ {expression} - Неожиданная ошибка: {e}")
            failed += 1

    return passed, failed


def run_error_test_group(error_tests, group_name):
    # Запускаем группу тестов на ошибки
    passed = 0
    failed = 0

    for expression, expected_error in error_tests:
        try:
            tokens = tokenize(expression)
            rpn = Polish(tokens)
            result = eval_polish(rpn)
            print(f"✗ {expression} - Ожидалась ошибка {expected_error.__name__}, но получен результат {result}")
            failed += 1

        except expected_error:
            print(f"✓ {expression} - Корректно вызвана ошибка {expected_error.__name__}")
            passed += 1

        except Exception as e:
            if isinstance(e, CalculatorError):
                print(f"✗ {expression} - Вызвана ошибка {type(e).__name__}, но ожидалась {expected_error.__name__}")
            else:
                print(f"✗ {expression} - Неожиданная ошибка: {e}")
            failed += 1

    return passed, failed


if __name__ == "__main__":
    run_all_tests()