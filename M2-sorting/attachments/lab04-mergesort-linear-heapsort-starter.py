#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 4. MergeSort, Counting, Radix и HeapSort: оценка производительности — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-04 и правилами использования генеративного ИИ
(docs/ai-verification.md). QuickSort перенесите из собственной ЛР 3.

Запуск: python lab04-mergesort-linear-heapsort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
from unicodedata import digit


# ---------------------------------------------------------------------------
# 1. Сортировки (реализуются вручную; sorted() используется только как эталон)
# ---------------------------------------------------------------------------


def merge(left: list, right: list, key) -> list:
    """Стабильное слияние двух отсортированных списков в новый список.

    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: O(m), где m = длина списка, количество сравнений = m - 1. TODO (обосновать в отчёте).
    """
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

    # TODO: два индекса, сравнение key(left[i]) <= key(right[j])
    raise NotImplementedError


def merge_sort(a: list, key=lambda x: x) -> list:
    """MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: O(n log n), где n - сложность разбиения массива на подмассивы,
    log n - сложность слияния массивов TODO."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right, key)

    # TODO: рекурсивное деление пополам + merge()
    raise NotImplementedError


def counting_sort(a: list[int], key_max: int) -> list[int]:
    """Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].

    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память: TODO — выразить через n и k = key_max + 1;
    ограничение диапазона ключей обсудить в отчёте.

    Последовательность действий:
    1. Создать массив для записи количества встречающихся чисел, равных индексу элемента массива.
    Массив имеет размер (key_max - 1).
    2. Записать количество втречающихся элементов по индексу этого числа (учитывать вариант, при котором одно и то же число может встречаться несколько раз)
    3. Создать итоговый отсортированный массив на основе массива индексов
    4.  Вывести отсортированный массив в return
    """
    # TODO: реализовать; проход расстановки — с конца массива (иначе теряется устойчивость)

    if a == [] or a is None: return []
    # 1. Создание необходимых переменных
    count = [0] * (key_max - 1)
    out = []

    # 2. Получение массива индексов
    for i in a:
        count[i] += 1

    # 3. Создание итогового массива
    for i in range(key_max):
        out.extend([i] * count[i])

    # 4. Вывод итогового ответа
    return out

def radix_sort_lsd(a: list[int]) -> list[int]:
    """RadixSort LSD по десятичным разрядам, неотрицательные целые.

    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему. Ожидаемая сложность: TODO — выразить через n и число разрядов d.

    # Сложность: О(d * (n + k)),
    # где d - количество разрядов
    # n - количество элементов
    # k - количество значений

    """
    # TODO: цикл по разрядам (exp = 1, 10, 100, ...) с устойчивой сортировкой
    # по цифре (a[i] // exp) % 10; объяснить, почему без устойчивости
    # внутреннего прохода алгоритм неверен

    # Сложность: О(d * (n + k)),
    # где d - количество разрядов
    # n - количество элементов
    # k - количество значений

    if a == [] or a is None: return []
    if a == [0]: return [0]

    exp = 1
    # Последовательность действий:

    # 1. Определение максимального разряда элементов
    # 2. Сортировка подсчетом по каждому разряду чисел из массива

    while max(a) // exp > 0:
        out = counting_sort(a, exp)
        exp *= 10
    return out

def sift_down(a: list[int], i: int, n: int) -> None:
    """Просейка вниз элемента i в куче a[0:n] (max-heap), на месте."""
    # TODO: спуск с обменом с большим из потомков, пока нарушено свойство кучи
    raise NotImplementedError


def heap_sort(a: list[int]) -> None:
    """HeapSort in-place: сортирует список a на месте, без вспомогательного массива.

    Схема: построение max-кучи просейками вниз (снизу вверх, O(n)),
    затем обмен вершины с последним элементом и просейка. Сложность: TODO.
    """
    # TODO: построение кучи + фаза извлечения максимумов
    raise NotImplementedError


def quick_sort(a: list[int]) -> list[int]:
    """QuickSort с рандомизацией опорного элемента — перенести из своей ЛР 3."""

    def quick_sort(a: list, rng: random.Random | None = None) -> list:
        """QuickSort с выбором опорного через rng.randrange.
        Возвращает новый список.

        Ожидаемая сложность: в среднем O(N logN), в худшем случае O(n^2)
        (обосновать в отчёте, объяснить роль рандомизации).

        rng передаётся снаружи, чтобы запуск был воспроизводим по seed варианта.
        """

        # Базовый случай: пустой или одноэлементный массив
        if len(a) <= 1:
            return a.copy()

        if rng is None:
            rng = random.Random()

        # Случайный выбор опорного элемента
        pivot = a[rng.randrange(0, len(a))]

        # Разделение массива на три части
        less = []
        equal = []
        greater = []

        for i in a:
            if i < pivot:
                less.append(i)

            elif i == pivot:
                equal.append(i)

            else:
                greater.append(i)

        # Рекурсивная сортировка частей
        return (
                quick_sort(less, rng)
                + equal
                + quick_sort(greater, rng)
        )


# ---------------------------------------------------------------------------
# 2. Верификация: инварианты + сверка с эталоном sorted()
#    (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Граничные и типовые случаи, стабильность, сверка с эталоном sorted()."""
    # Граничные случаи: пустой массив, один элемент, все элементы равны
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([5, 5, 5]) == [5, 5, 5]
    assert counting_sort([], key_max=10) == []
    assert radix_sort_lsd([0]) == [0]
    single = [42]
    heap_sort(single)
    assert single == [42]

    # Стабильность слияния: пары (ключ, порядковый номер); эталон sorted() стабилен,
    # поэтому при равных ключах порядок номеров обязан совпасть
    rng = random.Random(0)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    assert merge_sort(pairs, key=lambda p: p[0]) == sorted(pairs, key=lambda p: p[0])

    # Случайные тесты: инвариант перестановки + сверка с эталоном
    for _ in range(200):
        a = [rng.randint(0, 999) for _ in range(rng.randint(0, 60))]
        expected = sorted(a)
        assert merge_sort(a) == expected
        assert counting_sort(a, key_max=999) == expected
        assert radix_sort_lsd(a) == expected
        buf = list(a)
        heap_sort(buf)
        assert buf == expected
        assert sorted(buf) == expected  # выход — перестановка входа
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 3. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5
SMALL_KEY_MAX = 100        # узкий диапазон: counting уместен
WIDE_KEY_MAX = 10**9       # широкий диапазон: counting теряет смысл (обсудить в отчёте)


def make_datasets(rng: random.Random, n: int) -> dict[str, list[int]]:
    """Массивы разных распределений и диапазонов ключей для размера n."""
    almost = list(range(n))
    for _ in range(max(1, n // 100)):  # ~1 % случайных обменов
        i, j = rng.randrange(n), rng.randrange(n)
        almost[i], almost[j] = almost[j], almost[i]
    return {
        "random_wide": [rng.randint(0, WIDE_KEY_MAX) for _ in range(n)],
        "random_small": [rng.randint(0, SMALL_KEY_MAX) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "almost_sorted": almost,
    }


def bench(fn, data: list[int]) -> float:
    """Медиана времени fn на копии data по REPEATS запускам, с прогревом.

    Каждый запуск получает свежую копию: сортировка на месте не должна
    превращать последующие запуски в сортировку уже отсортированного массива.
    """
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        buf = list(data)
        t0 = time.perf_counter()
        fn(buf)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    rng = random.Random(seed)
    algorithms = [
        ("merge_sort", merge_sort),
        ("counting_sort", lambda a: counting_sort(a, key_max=max(a, default=0))),
        ("radix_sort_lsd", radix_sort_lsd),
        ("heap_sort", heap_sort),
        ("quick_sort (ЛР 3)", quick_sort),
        ("sorted() (эталон)", sorted),
    ]
    for n in SIZES:
        datasets = make_datasets(rng, n)
        print(f"\nn = {n}:")
        for dist_name, data in datasets.items():
            print(f"  распределение {dist_name}:")
            for algo_name, fn in algorithms:
                if algo_name == "counting_sort" and dist_name == "random_wide":
                    # счётчики размера ~10^9 не помещаются в память — граница
                    # применимости counting; зафиксировать в таблице свойств
                    print(f"    {algo_name:>18}: пропуск (диапазон ключей)")
                    continue
                print(f"    {algo_name:>18}: t = {bench(fn, data):.6f} c")
    # TODO: построить log-log графики (matplotlib) по каждому распределению;
    # TODO: заполнить таблицу свойств: время (лучший/средний/худший),
    #       память, стабильность, ограничения — для всех шести сортировок;
    # TODO: объяснить расхождения замеров с асимптотикой в отчёте.


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
