from dataclasses import dataclass
from operator import itemgetter
from typing import List, Tuple, Dict


@dataclass
class StoredProcedure:
    id: int
    name: str
    execution_time: int
    db_id: int


@dataclass
class Database:
    id: int
    name: str


@dataclass
class ProcedureDatabase:
    db_id: int
    proc_id: int


def create_sample_data() -> Tuple[List[Database], List[StoredProcedure], List[ProcedureDatabase]]:
    databases = [
        Database(1, 'Основная база'),
        Database(2, 'Архивная база'),
        Database(3, 'База отчетов'),
        Database(4, 'Тестовая база'),
    ]

    procedures = [
        StoredProcedure(1, 'расчет_отчета', 150, 1),
        StoredProcedure(2, 'резервное_копирование', 300, 2),
        StoredProcedure(3, 'генерация_статистики', 200, 3),
        StoredProcedure(4, 'очистка_данных', 250, 3),
        StoredProcedure(5, 'проверка_ввода', 100, 3),
        StoredProcedure(6, 'формирование_отчетов', 180, 1),
    ]

    procedures_databases = [
        ProcedureDatabase(1, 1),
        ProcedureDatabase(2, 2),
        ProcedureDatabase(3, 3),
        ProcedureDatabase(3, 4),
        ProcedureDatabase(3, 5),
        ProcedureDatabase(4, 1),
        ProcedureDatabase(4, 3),
        ProcedureDatabase(1, 6),
        ProcedureDatabase(3, 6),
    ]

    return databases, procedures, procedures_databases


def get_one_to_many(databases: List[Database],
                    procedures: List[StoredProcedure]) -> List[Tuple]:
    return [(p.name, p.execution_time, d.name)
            for d in databases
            for p in procedures
            if p.db_id == d.id]


def get_many_to_many(databases: List[Database],
                     procedures: List[StoredProcedure],
                     relations: List[ProcedureDatabase]) -> List[Tuple]:
    many_to_many_temp = [(d.name, pd.db_id, pd.proc_id)
                         for d in databases
                         for pd in relations
                         if d.id == pd.db_id]

    return [(p.name, p.execution_time, db_name)
            for db_name, db_id, proc_id in many_to_many_temp
            for p in procedures if p.id == proc_id]


def task1_sorted_procedures(databases: List[Database],
                           procedures: List[StoredProcedure]) -> List[Tuple]:
    one_to_many = get_one_to_many(databases, procedures)
    return sorted(one_to_many, key=itemgetter(0))


def task2_database_procedure_counts(databases: List[Database],
                                   procedures: List[StoredProcedure]) -> List[Tuple]:
    result = []
    for d in databases:
        # Подсчитываем процедуры для данной БД
        procedure_count = sum(1 for proc in procedures if proc.db_id == d.id)
        if procedure_count > 0:
            result.append((d.name, procedure_count))

    # Сортируем по количеству процедур (возрастание)
    return sorted(result, key=itemgetter(1))


def task3_procedures_ending_with_ov(databases: List[Database],
                                   procedures: List[StoredProcedure],
                                   relations: List[ProcedureDatabase]) -> Dict[str, List[str]]:
    many_to_many = get_many_to_many(databases, procedures, relations)

    result = {}
    for proc_name, exec_time, db_name in many_to_many:
        if proc_name.endswith('ов'):
            if proc_name not in result:
                result[proc_name] = []
            # Добавляем БД, если её ещё нет в списке
            if db_name not in result[proc_name]:
                result[proc_name].append(db_name)

    return result


def print_results(databases: List[Database],
                  procedures: List[StoredProcedure],
                  relations: List[ProcedureDatabase]) -> None:
    print("ЗАДАНИЕ 1: Все процедуры, отсортированные по имени")
    res1 = task1_sorted_procedures(databases, procedures)
    print(f"{'Процедура':<25} {'Время (ms)':<12} {'База данных':<20}")
    for proc_name, exec_time, db_name in res1:
        print(f"{proc_name:<25} {exec_time:<12} {db_name:<20}")

    print("ЗАДАНИЕ 2: Количество процедур в каждой БД")
    res2 = task2_database_procedure_counts(databases, procedures)
    print(f"{'База данных':<25} {'Кол-во процедур':<15}")
    for db_name, count in res2:
        print(f"{db_name:<25} {count:<15}")

    print("ЗАДАНИЕ 3: Процедуры, оканчивающиеся на 'ов' и БД, где они работают")
    res3 = task3_procedures_ending_with_ov(databases, procedures, relations)
    if res3:
        for proc_name, db_list in res3.items():
            print(f"\nПроцедура: {proc_name}")
            print(f"Работает в БД: {', '.join(db_list)}")
    else:
        print("Нет процедур, оканчивающихся на 'ов'")


def main() -> None:
    # Получаем тестовые данные
    databases, procedures, relations = create_sample_data()

    # Выводим результаты
    print_results(databases, procedures, relations)


if __name__ == "__main__":
    main()
