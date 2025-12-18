# -*- coding: cp1251 -*-
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from lab4 import add_aspect_ratio_columns  # Импортируем функцию из lab4.py

def main():
    # НАСТРОЙКА АРГУМЕНТОВ
    parser = argparse.ArgumentParser(description="ЛР4 — Анализ изображений (отношение сторон)")
    parser.add_argument("--annotation", type=str, default="pig_images/annotation.csv",
                        help="Путь к annotation.csv из ЛР2")
    parser.add_argument("--output-csv", type=str, default="images_with_ratio.csv",
                        help="Куда сохранить DataFrame")
    parser.add_argument("--output-plot", type=str, default="histogram_ratio.png",
                        help="Куда сохранить график")
    args = parser.parse_args()

    # ПРОВЕРКА ФАЙЛА АННОТАЦИИ
    if not os.path.exists(args.annotation):
        print(f"Ошибка: файл {args.annotation} не найден!")
        print("Убедитесь, что папка pig_images с annotation.csv лежит в той же директории.")
        return

    # ЧТЕНИЕ И ПЕРЕИМЕНОВАНИЕ
    df = pd.read_csv(args.annotation)
    df = df.rename(columns={
        "absolute_path": "Абсолютный путь",
        "relative_path": "Относительный путь"
    })

    # ДОБАВЛЕНИЕ НОВЫХ КОЛОНОК (через функцию из lab4.py)
    df = add_aspect_ratio_columns(df)

    # СОРТИРОВКА
    df_sorted = df.sort_values(by="Отношение сторон (w/h)", ascending=False)
    print("Первые 5 строк отсортированного DataFrame:")
    print(df_sorted.head())

    # ФИЛЬТРАЦИЯ
    filtered = df_sorted[df_sorted["Отношение сторон (w/h)"] > 1.0]
    print(f"\nИзображений с ratio > 1.0 (горизонтальные): {len(filtered)}")

    # ГИСТОГРАММА
    plt.figure(figsize=(10, 6))
    df_sorted["Диапазон отношения сторон"].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title("Гистограмма распределения отношения сторон изображений")
    plt.xlabel("Диапазон отношения сторон (w/h)")
    plt.ylabel("Количество изображений")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(args.output_plot)
    plt.show()
    print(f"График сохранён: {args.output_plot}")

    # СОХРАНЕНИЕ DATAFRAME
    df_sorted.to_csv(args.output_csv, index=False, encoding="utf-8")
    print(f"DataFrame сохранён: {args.output_csv}")

if __name__ == "__main__":
    main()