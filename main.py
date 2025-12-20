import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from lab4 import add_aspect_ratio_columns  # Èìïîðòèðóåì ôóíêöèþ èç lab4.py

def main():
    # ÍÀÑÒÐÎÉÊÀ ÀÐÃÓÌÅÍÒÎÂ
    parser = argparse.ArgumentParser(description="ËÐ4 — Àíàëèç èçîáðàæåíèé (îòíîøåíèå ñòîðîí)")
    parser.add_argument("--annotation", type=str, default="pig_images/annotation.csv",
                        help="Ïóòü ê annotation.csv èç ËÐ2")
    parser.add_argument("--output-csv", type=str, default="images_with_ratio.csv",
                        help="Êóäà ñîõðàíèòü DataFrame")
    parser.add_argument("--output-plot", type=str, default="histogram_ratio.png",
                        help="Êóäà ñîõðàíèòü ãðàôèê")
    args = parser.parse_args()

    # ÏÐÎÂÅÐÊÀ ÔÀÉËÀ ÀÍÍÎÒÀÖÈÈ
    if not os.path.exists(args.annotation):
        print(f"Îøèáêà: ôàéë {args.annotation} íå íàéäåí!")
        print("Óáåäèòåñü, ÷òî ïàïêà pig_images ñ annotation.csv ëåæèò â òîé æå äèðåêòîðèè.")
        return

    # ×ÒÅÍÈÅ È ÏÅÐÅÈÌÅÍÎÂÀÍÈÅ
    df = pd.read_csv(args.annotation)
    df = df.rename(columns={
        "absolute_path": "Àáñîëþòíûé ïóòü",
        "relative_path": "Îòíîñèòåëüíûé ïóòü"
    })

    # ÄÎÁÀÂËÅÍÈÅ ÍÎÂÛÕ ÊÎËÎÍÎÊ (÷åðåç ôóíêöèþ èç lab4.py)
    df = add_aspect_ratio_columns(df)

    # ÑÎÐÒÈÐÎÂÊÀ
    df_sorted = df.sort_values(by="Îòíîøåíèå ñòîðîí (w/h)", ascending=False)
    print("Ïåðâûå 5 ñòðîê îòñîðòèðîâàííîãî DataFrame:")
    print(df_sorted.head())

    # ÔÈËÜÒÐÀÖÈß
    filtered = df_sorted[df_sorted["Îòíîøåíèå ñòîðîí (w/h)"] > 1.0]
    print(f"\nÈçîáðàæåíèé ñ ratio > 1.0 (ãîðèçîíòàëüíûå): {len(filtered)}")

    # ÃÈÑÒÎÃÐÀÌÌÀ
    plt.figure(figsize=(10, 6))
    df_sorted["Äèàïàçîí îòíîøåíèÿ ñòîðîí"].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title("Ãèñòîãðàììà ðàñïðåäåëåíèÿ îòíîøåíèÿ ñòîðîí èçîáðàæåíèé")
    plt.xlabel("Äèàïàçîí îòíîøåíèÿ ñòîðîí (w/h)")
    plt.ylabel("Êîëè÷åñòâî èçîáðàæåíèé")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(args.output_plot)
    plt.show()
    print(f"Ãðàôèê ñîõðàí¸í: {args.output_plot}")

    # ÑÎÕÐÀÍÅÍÈÅ DATAFRAME
    df_sorted.to_csv(args.output_csv, index=False, encoding="utf-8")
    print(f"DataFrame ñîõðàí¸í: {args.output_csv}")

if __name__ == "__main__":

    main()
