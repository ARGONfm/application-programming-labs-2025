import argparse
import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt

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

    # 1. Чтение аннотации в DataFrame
    if not os.path.exists(args.annotation):
        print(f"Ошибка: файл {args.annotation} не найден!")
        return

    df = pd.read_csv(args.annotation)

    # 2. Переименовывание колонок
    df = df.rename(columns={
        "absolute_path": "Абсолютный путь",
        "relative_path": "Относительный путь"
    })

    # 3. Добавление колонки "Отношение сторон (w/h)"
    ratios = []
    for abs_path in df["Абсолютный путь"]:
        img = cv2.imread(abs_path)
        if img is None:
            ratios.append(0.0)
            print(f"Предупреждение: не удалось прочитать {abs_path}")
        else:
            h, w = img.shape[:2]
            ratio = w / h if h != 0 else 0.0
            ratios.append(round(ratio, 2))

    df["Отношение сторон (w/h)"] = ratios

    # 4. Добавление колонки для гистограммы — диапазоны
    def get_ratio_bin(ratio):
        if ratio < 0.5: return "0-0.5"
        elif 0.5 <= ratio < 1.0: return "0.5-1.0"
        elif 1.0 <= ratio < 1.5: return "1.0-1.5"
        elif 1.5 <= ratio < 2.0: return "1.5-2.0"
        else: return "2.0+"

    df["Диапазон отношения сторон"] = df["Отношение сторон (w/h)"].apply(get_ratio_bin)

    # 5. Сортировка по новой колонке
    df_sorted = df.sort_values(by="Отношение сторон (w/h)", ascending=False)
    print("Первые 5 строк отсортированного DataFrame:")
    print(df_sorted.head())

    # 6. Фильтрация по новой колонке (пример: горизонтальные изображения, ratio > 1.0)
    filtered = df_sorted[df_sorted["Отношение сторон (w/h)"] > 1.0]
    print(f"\nИзображений с ratio > 1.0 (горизонтальные): {len(filtered)}")

    # 7. Гистограмма по диапазонам
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

    # 8. Сохранение DataFrame
    df_sorted.to_csv(args.output_csv, index=False, encoding="utf-8")
    print(f"DataFrame сохранён: {args.output_csv}")

if __name__ == "__main__":
    main()