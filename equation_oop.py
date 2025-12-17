import sys
import math

class SquareRoots:

    def __init__(self):
        # Объявление коэффициентов
        self.coef_A = 0.0
        self.coef_B = 0.0
        self.coef_C = 0.0
        # Количество корней
        self.num_roots = 0
        # Список корней
        self.roots_list = []

    def get_coef(self, index, prompt):
        try:
            # Пробуем прочитать коэффициент из командной строки
            coef_str = sys.argv[index]
        except:
            # Вводим с клавиатуры
            print(prompt)
            coef_str = input()
        # Переводим строку в действительное число
        coef = float(coef_str)
        return coef

    def get_coefs(self):
        self.coef_A = self.get_coef(1, 'Введите коэффициент А:')
        self.coef_B = self.get_coef(2, 'Введите коэффициент B:')
        self.coef_C = self.get_coef(3, 'Введите коэффициент C:')

    def get_biquadrate_roots(self, root):
        if root == 0.0:
            self.num_roots += 1
            self.roots_list.append(root)
        elif root > 0.0:
            self.num_roots += 2
            self.roots_list.append(math.sqrt(root))
            self.roots_list.append(-math.sqrt(root))

    def calculate_roots(self):
        a = self.coef_A
        b = self.coef_B
        c = self.coef_C
        # Вычисление дискриминанта и корней
        D = b*b - 4*a*c
        if D == 0.0:
            root = -b / (2.0*a)
            self.get_biquadrate_roots(root)
        elif D > 0.0:
            sqD = math.sqrt(D)
            root1 = (-b + sqD) / (2.0*a)
            root2 = (-b - sqD) / (2.0*a)
            self.get_biquadrate_roots(root1)
            self.get_biquadrate_roots(root2)

    def print_roots(self):
        # Проверка отсутствия ошибок при вычислении корней
        if self.num_roots != len(self.roots_list):
            print(('Ошибка. Уравнение содержит {} действительных корней, ' +\
                'но было вычислено {} корней.').format(self.num_roots, len(self.roots_list)))
        else:
            if self.num_roots == 0:
                print('Нет корней')
            elif self.num_roots == 1:
                print('Один корень: {}'.format(self.roots_list[0]))
            elif self.num_roots == 2:
                print('Два корня: {} и {}'.format(self.roots_list[0], self.roots_list[1]))
            elif self.num_roots == 3:
                print('Три корня: {}, {} и {}'.format(self.roots_list[0], self.roots_list[1], self.roots_list[2]))
            elif self.num_roots == 4:
                print('Четыре корня: {}, {}, {} и {}'.format(self.roots_list[0], self.roots_list[1], self.roots_list[2], self.roots_list[3]))



def main():
    # Создание объекта класса
    r = SquareRoots()
    # Последовательный вызов необходимых методов
    r.get_coefs()
    r.calculate_roots()
    r.print_roots()

# Если сценарий запущен из командной строки
if __name__ == "__main__":
    main()

# Пример запуска
# roots_oop.py 1 0 -4
