import argparse
import os
import cv2
import matplotlib.pyplot as plt
from lab3 import pixelate_image

def main():
    parser = argparse.ArgumentParser(description="ËÐ3 — Ïðåâðàòèòü èçîáðàæåíèå â ïèêñåëü-àðò")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="pixel_art_result.jpg")
    parser.add_argument("--pixel-size", type=int, default=16)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Îøèáêà: ôàéë {args.input} íå íàéäåí!")
        return

    original_bgr = cv2.imread(args.input)
    if original_bgr is None:
        print("Îøèáêà: íå óäàëîñü çàãðóçèòü èçîáðàæåíèå.")
        return

    original_rgb = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)
    pixelated_rgb = pixelate_image(original_rgb, args.pixel_size)
    pixelated_bgr = cv2.cvtColor(pixelated_rgb, cv2.COLOR_RGB2BGR)

    cv2.imwrite(args.output, pixelated_bgr)
    print(f"Ïèêñåëü-àðò ñîõðàí¸í: {args.output}")

    h, w = original_rgb.shape[:2]
    print(f"Èñõîäíûé ðàçìåð: {w} x {h} ïèêñåëåé")
    print(f"Ðàçìåð ïèêñåëÿ â àðòå: {args.pixel_size} x {args.pixel_size}")

    plt.figure(figsize=(16, 8))
    plt.subplot(1, 2, 1)
    plt.title(f"Îðèãèíàë ({w}x{h})", fontsize=16)
    plt.imshow(original_rgb)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title(f"Ïèêñåëü-àðò (áëîê {args.pixel_size}x{args.pixel_size})", fontsize=16)
    plt.imshow(pixelated_rgb)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("\nÃîòîâî! Âñ¸ âûïîëíåíî ïî ÒÇ.")

if __name__ == "__main__":

    main()
