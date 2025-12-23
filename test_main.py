import unittest
from main import (
    Database,
    StoredProcedure,
    ProcedureDatabase,
    create_sample_data,
    task1_sorted_procedures,
    task2_database_procedure_counts,
    task3_procedures_ending_with_ov
)


class TestTask1(unittest.TestCase):
    """Тесты для Задания 1: Отсортированные процедуры"""

    def test_sorted_procedures_with_sample_data(self):
        """Тест 1: Проверка сортировки процедур на тестовых данных"""
        # Получаем тестовые данные
        databases, procedures, _ = create_sample_data()

        # Выполняем задание 1
        result = task1_sorted_procedures(databases, procedures)

        # Проверяем, что результат не пустой
        self.assertGreater(len(result), 0, "Результат не должен быть пустым")

        # Проверяем количество элементов
        self.assertEqual(len(result), 6, "Должно быть 6 процедур")

        # Проверяем сортировку по алфавиту (по имени процедуры)
        procedure_names = [item[0] for item in result]
        sorted_names = sorted(procedure_names)
        self.assertEqual(procedure_names, sorted_names,
                        "Процедуры должны быть отсортированы по алфавиту")

        # Проверяем структуру данных
        for proc_name, exec_time, db_name in result:
            self.assertIsInstance(proc_name, str, "Имя процедуры должно быть строкой")
            self.assertIsInstance(exec_time, int, "Время выполнения должно быть числом")
            self.assertIsInstance(db_name, str, "Имя БД должно быть строкой")
            self.assertGreater(exec_time, 0, "Время выполнения должно быть положительным")

    def test_sorted_procedures_empty_data(self):
        """Тест: Проверка с пустыми данными"""
        databases = []
        procedures = []

        result = task1_sorted_procedures(databases, procedures)

        self.assertEqual(result, [], "При пустых данных должен быть пустой список")


class TestTask2(unittest.TestCase):
    """Тесты для Задания 2: Количество процедур в БД"""

    def test_database_procedure_counts_with_sample_data(self):
        """Тест 2: Проверка подсчета процедур в БД на тестовых данных"""
        databases, procedures, _ = create_sample_data()

        result = task2_database_procedure_counts(databases, procedures)

        # Проверяем количество БД с процедурами
        self.assertEqual(len(result), 3, "Должно быть 3 БД с процедурами")

        # Проверяем конкретные значения (сортируем для сравнения)
        expected_results = [
            ('Архивная база', 1),
            ('Основная база', 2),
            ('База отчетов', 3)
        ]

        # Сортируем expected_results по количеству процедур
        expected_sorted = sorted(expected_results, key=lambda x: x[1])

        # Проверяем каждую пару
        for (expected_db, expected_count), (actual_db, actual_count) in zip(expected_sorted, result):
            self.assertEqual(expected_db, actual_db,
                           f"Ожидалась БД '{expected_db}', получена '{actual_db}'")
            self.assertEqual(expected_count, actual_count,
                           f"Для БД '{actual_db}' ожидалось {expected_count} процедур, получено {actual_count}")

        # Проверяем сортировку по количеству процедур (возрастание)
        counts = [item[1] for item in result]
        self.assertEqual(counts, sorted(counts),
                        "Результат должен быть отсортирован по количеству процедур")

    def test_single_database_with_multiple_procedures(self):
        """Тест: Одна БД с несколькими процедурами"""
        databases = [Database(1, 'Тестовая БД')]
        procedures = [
            StoredProcedure(1, 'процедура1', 100, 1),
            StoredProcedure(2, 'процедура2', 200, 1),
            StoredProcedure(3, 'процедура3', 300, 1),
        ]

        result = task2_database_procedure_counts(databases, procedures)

        self.assertEqual(len(result), 1, "Должна быть одна БД")
        self.assertEqual(result[0][0], 'Тестовая БД', "Название БД должно совпадать")
        self.assertEqual(result[0][1], 3, "Должно быть 3 процедуры")


class TestTask3(unittest.TestCase):
    """Тесты для Задания 3: Процедуры, оканчивающиеся на 'ов'"""

    def test_procedures_ending_with_ov_with_sample_data(self):
        """Тест 3: Проверка поиска процедур, оканчивающихся на 'ов'"""
        databases, procedures, relations = create_sample_data()

        result = task3_procedures_ending_with_ov(databases, procedures, relations)

        # Проверяем, что найдена хотя бы одна процедура
        self.assertGreater(len(result), 0, "Должна быть найдена хотя бы одна процедура")

        # Проверяем конкретную процедуру
        self.assertIn('формирование_отчетов', result,
                     "Должна быть найдена процедура 'формирование_отчетов'")

        # Проверяем, что процедуры действительно оканчиваются на 'ов'
        for proc_name in result.keys():
            self.assertTrue(proc_name.endswith('ов'),
                          f"Процедура '{proc_name}' должна оканчиваться на 'ов'")

        # Проверяем БД для процедуры 'формирование_отчетов'
        expected_dbs_for_reporting = ['Основная база', 'База отчетов']
        actual_dbs = result['формирование_отчетов']

        # Проверяем количество БД
        self.assertEqual(len(actual_dbs), 2,
                        f"Процедура 'формирование_отчетов' должна работать в 2 БД")

        # Проверяем конкретные БД (порядок не важен)
        for db_name in expected_dbs_for_reporting:
            self.assertIn(db_name, actual_dbs,
                         f"БД '{db_name}' должна быть в списке для процедуры 'формирование_отчетов'")

    def test_no_procedures_ending_with_ov(self):
        """Тест: Нет процедур, оканчивающихся на 'ов'"""
        databases = [Database(1, 'БД1'), Database(2, 'БД2')]
        procedures = [
            StoredProcedure(1, 'процедура_тест', 100, 1),
            StoredProcedure(2, 'тестовая', 200, 2),
        ]
        relations = [
            ProcedureDatabase(1, 1),
            ProcedureDatabase(2, 2),
        ]

        result = task3_procedures_ending_with_ov(databases, procedures, relations)

        self.assertEqual(result, {}, "При отсутствии процедур на 'ов' должен быть пустой словарь")


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def test_all_tasks_with_consistent_data(self):
        """Тест: Проверка согласованности данных между заданиями"""
        databases, procedures, relations = create_sample_data()

        # Выполняем все задания
        result1 = task1_sorted_procedures(databases, procedures)
        result2 = task2_database_procedure_counts(databases, procedures)
        result3 = task3_procedures_ending_with_ov(databases, procedures, relations)

        # Проверяем, что все процедуры из task3 есть в task1
        procedures_from_task1 = {item[0] for item in result1}
        for proc_name in result3.keys():
            self.assertIn(proc_name, procedures_from_task1,
                         f"Процедура '{proc_name}' из task3 должна быть в task1")

        # Проверяем, что БД из task2 существуют
        db_names_from_task2 = {item[0] for item in result2}
        all_db_names = {db.name for db in databases}
        for db_name in db_names_from_task2:
            self.assertIn(db_name, all_db_names,
                         f"БД '{db_name}' из task2 должна существовать")


def run_tests():
    """Запуск всех тестов"""
    # Создаем test suite
    loader = unittest.TestLoader()

    # Добавляем все тестовые классы
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestTask1))
    suite.addTest(loader.loadTestsFromTestCase(TestTask2))
    suite.addTest(loader.loadTestsFromTestCase(TestTask3))
    suite.addTest(loader.loadTestsFromTestCase(TestIntegration))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим статистику
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    return result


if __name__ == "__main__":
    # Запускаем все тесты
    test_result = run_tests()

    # Возвращаем код выхода: 0 если все тесты прошли, 1 если есть ошибки
    exit_code = 0 if test_result.wasSuccessful() else 1
    exit(exit_code)
