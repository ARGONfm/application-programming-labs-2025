import argparse
import os
import time
import csv
import threading
from icrawler.builtin import BingImageCrawler
from typing import Tuple


# ИТЕРАТОР ПО ПУТЯМ ИЗ АННОТАЦИИ
class ImagePathIterator:
    """Итератор для построчного чтения annotation.csv (absolute_path, relative_path)"""

    def __init__(self, path: str):
        with open(path, encoding="utf-8") as f:
            self.data = list(csv.reader(f))[1:]
        self.idx = 0

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self) -> Tuple[str, str]:
        if self.idx >= len(self.data):
            raise StopIteration
        row = self.data[self.idx]
        self.idx += 1
        return row[0], row[1] 


# СКАЧИВАНИЕ С ОСТАНОВКОЙ
def download_images(folder: str, max_time: int, min_count: int):
    """Скачивает изображения 'pig' до достижения min_count или истечения max_time"""
    os.makedirs(folder, exist_ok=True)
    start_time = time.time()
    print(f"Начато скачивание в папку: {folder}")
    print(f"Условие остановки: {min_count} изображений или {max_time} секунд\n")

    # Запуск icrawler в отдельном daemon-потоке 
    crawler = BingImageCrawler(storage={"root_dir": folder}, downloader_threads=10)
    thread = threading.Thread(
        target=crawler.crawl,
        kwargs={"keyword": "pig", "max_num": 9999, "min_size": (200, 200)},
        daemon=True
    )
    thread.start()

    shown = 0
    while time.time() - start_time < max_time:
        files = [f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        count = len(files)

        if count > shown:
            shown = count
            print(f"  Скачано изображений: {count}")
            if count >= min_count:
                print(f"\nДостигнуто минимальное количество ({min_count}). Остановка.")
                break
        time.sleep(1)

    total = len([f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    elapsed = time.time() - start_time
    print(f"\nСкачивание завершено. Всего: {total} изображений за {elapsed:.1f} сек")
    return total


# СОЗДАНИЕ ФАЙЛА АННОТАЦИИ
def create_annotation(folder: str, csv_path: str):
    """Создаёт CSV-файл с абсолютными и относительными путями к изображениям"""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path"])
        for filename in sorted(os.listdir(folder)):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                abs_path = os.path.abspath(os.path.join(folder, filename))
                rel_path = os.path.join(folder, filename)
                writer.writerow([abs_path, rel_path])


# ОСНОВНАЯ ПРОГРАММА
def main():
    parser = argparse.ArgumentParser(description="Лабораторная работа №2 — скачивание изображений pig")
    parser.add_argument("--time", type=int, required=True, help="Максимальное время работы (секунды)")
    parser.add_argument("--min-images", type=int, default=50, help="Минимальное количество изображений")
    parser.add_argument("--dir", default="pig_images", help="Папка для сохранения изображений")
    args = parser.parse_args()

    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №2 — ВАРИАНТ 16")
    print("=" * 60)

    # 1. Скачивание с контролем времени и количества
    count = download_images(args.dir, args.time, args.min_images)

    # 2. Создание аннотации
    annotation_path = os.path.join(args.dir, "annotation.csv")
    create_annotation(args.dir, annotation_path)
    print(f"Аннотация сохранена: {annotation_path}")

    # 3. Демонстрация работы итератора
    print("\nПроверка итератора (первые 5 записей):")
    for i, (_, rel_path) in enumerate(ImagePathIterator(annotation_path)):
        if i < 5:
            print(f"  {rel_path}")
        else:
            print("  ...")
            break

    print("\n" + "=" * 60)
    print(f"ЗАДАНИЕ ВЫПОЛНЕНО. Скачано изображений: {count}")
    print("=" * 60)


if __name__ == "__main__":
    main()