# -*- coding: cp1251 -*-
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from lab4 import add_aspect_ratio_columns  # »мпортируем функцию из lab4.py

def main():
    # Ќј—“–ќ… ј ј–√”ћ≈Ќ“ќ¬
    parser = argparse.ArgumentParser(description="Ћ–4 Ч јнализ изображений (отношение сторон)")
    parser.add_argument("--annotation", type=str, default="pig_images/annotation.csv",
                        help="ѕуть к annotation.csv из Ћ–2")
    parser.add_argument("--output-csv", type=str, default="images_with_ratio.csv",
                        help=" уда сохранить DataFrame")
    parser.add_argument("--output-plot", type=str, default="histogram_ratio.png",
                        help=" уда сохранить график")
    args = parser.parse_args()

    # ѕ–ќ¬≈– ј ‘ј…Ћј јЌЌќ“ј÷»»
    if not os.path.exists(args.annotation):
        print(f"ќшибка: файл {args.annotation} не найден!")
        print("”бедитесь, что папка pig_images с annotation.csv лежит в той же директории.")
        return

    # „“≈Ќ»≈ » ѕ≈–≈»ћ≈Ќќ¬јЌ»≈
    df = pd.read_csv(args.annotation)
    df = df.rename(columns={
        "absolute_path": "јбсолютный путь",
        "relative_path": "ќтносительный путь"
    })

    # ƒќЅј¬Ћ≈Ќ»≈ Ќќ¬џ’  ќЋќЌќ  (через функцию из lab4.py)
    df = add_aspect_ratio_columns(df)

    # —ќ–“»–ќ¬ ј
    df_sorted = df.sort_values(by="ќтношение сторон (w/h)", ascending=False)
    print("ѕервые 5 строк отсортированного DataFrame:")
    print(df_sorted.head())

    # ‘»Ћ№“–ј÷»я
    filtered = df_sorted[df_sorted["ќтношение сторон (w/h)"] > 1.0]
    print(f"\n»зображений с ratio > 1.0 (горизонтальные): {len(filtered)}")

    # √»—“ќ√–јћћј
    plt.figure(figsize=(10, 6))
    df_sorted["ƒиапазон отношени¤ сторон"].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title("√истограмма распределени¤ отношени¤ сторон изображений")
    plt.xlabel("ƒиапазон отношени¤ сторон (w/h)")
    plt.ylabel(" оличество изображений")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(args.output_plot)
    plt.show()
    print(f"√рафик сохранЄн: {args.output_plot}")

    # —ќ’–јЌ≈Ќ»≈ DATAFRAME
    df_sorted.to_csv(args.output_csv, index=False, encoding="utf-8")
    print(f"DataFrame сохранЄн: {args.output_csv}")

if __name__ == "__main__":
    main()