import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def pixelate_image(image: np.ndarray, pixel_size: int) -> np.ndarray:
    """
    Преобразует изображение в пиксель-арт.
    pixel_size — размер одного "пиксельного" блока в пикселях (например, 8, 16, 32)
    """
    if pixel_size <= 1:
        return image.copy()

    h, w = image.shape[:2]

    small = cv2.resize(image,
                       (w // pixel_size, h // pixel_size),
                       interpolation=cv2.INTER_LINEAR)

    pixelated = cv2.resize(small,
                           (w, h),
                           interpolation=cv2.INTER_NEAREST)

    return pixelated


def main():
    # НАСТРОЙКА АРГУМЕНТОВ
    parser = argparse.ArgumentParser(description="ЛР3 — Превратить изображение в пиксель-арт")
    parser.add_argument("--input", type=str, required=True,
                        help="Путь к исходному изображению (например, pig_images/000001.jpg)")
    parser.add_argument("--output", type=str, default="pixel_art_result.jpg",
                        help="Куда сохранить результат (по умолчанию: pixel_art_result.jpg)")
    parser.add_argument("--pixel-size", type=int, default=16,
                        help="Размер одного пикселя в пиксель-арте (8, 16, 32 и т.д.), по умолчанию 16")
    args = parser.parse_args()

    # ЧТЕНИЕ ИЗОБРАЖЕНИЯ
    if not os.path.exists(args.input):
        print(f"Ошибка: файл {args.input} не найден!")
        return

    # OpenCV читает в формате BGR
    original_bgr = cv2.imread(args.input)
    if original_bgr is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    # Переводим в RGB для правильного отображения в matplotlib
    original_rgb = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)

    # ПРЕОБРАЗОВАНИЕ
    pixelated_rgb = pixelate_image(original_rgb, args.pixel_size)

    # Переводим обратно в BGR для сохранения через OpenCV
    pixelated_bgr = cv2.cvtColor(pixelated_rgb, cv2.COLOR_RGB2BGR)

    # СОХРАНЕНИЕ РЕЗУЛЬТАТА
    cv2.imwrite(args.output, pixelated_bgr)
    print(f"Пиксель-арт сохранён ? {args.output}")

    # ВЫВОД ИНФОРМАЦИИ
    h, w = original_rgb.shape[:2]
    print(f"Исходный размер: {w} ? {h} пикселей")
    print(f"Размер пикселя в арте: {args.pixel_size} ? {args.pixel_size}")

    # ВИЗУАЛИЗАЦИЯ
    plt.figure(figsize=(16, 8))

    # Оригинал
    plt.subplot(1, 2, 1)
    plt.title(f"Оригинал ({w}?{h})", fontsize=16)
    plt.imshow(original_rgb)
    plt.axis("off")

    # Пиксель-арт
    plt.subplot(1, 2, 2)
    plt.title(f"Пиксель-арт (блок {args.pixel_size}?{args.pixel_size})", fontsize=16)
    plt.imshow(pixelated_rgb)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("\nГотово! Всё выполнено по ТЗ.")

if __name__ == "__main__":
    main()