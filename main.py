from Polish import *
from tokenize import *
from eval_polish import *
from calc_errors import *
from testy import *
import re

def main():

    print("Калькулятор запущен!")
    print("Для выхода введите 'выход' или 'exit'")
    print("Для запуска тестов введите 'test'")

    while True:
        try:
            vvod = input("\nВведите выражение: ")

            # Ошибка двух и более бинарных операций между двумя числами

            # Проверка на команду выхода
            if vvod.lower() in ['выход', 'exit', 'quit']:
                print("Прощайте!")
                break

            if vvod.lower() == 'test':
                from testy import run_all_tests
                run_all_tests()
                continue

            # Пропускаем пустые строки
            if not vvod.strip():
                continue


            pattern = r'\d*\.\d*\.\d*'
            matches = re.findall(pattern, vvod)
            for match in matches:
                if match:
                    raise InvalidFloatFormatError(f"Число {match} содержит более одной точки")

            tokens = tokenize(vvod)
            validate_operator(tokens)
            rpn_tokens = Polish(tokens)
            result = eval_polish(rpn_tokens)
            print("Результат:", result)

        except CalculatorError as e:
            print(e)

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем. До свидания!")
            break

        except Exception as e:
            print("Неожиданная ошибка:", e)


if __name__ == "__main__":
    main()