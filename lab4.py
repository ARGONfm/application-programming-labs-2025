import cv2
import pandas as pd

def get_image_ratio(abs_path: str) -> float:
    """Вычисляет отношение сторон (ширина / высота) изображения по абсолютному пути."""
    img = cv2.imread(abs_path)
    if img is None:
        print(f"Предупреждение: не удалось прочитать {abs_path}")
        return 0.0
    h, w = img.shape[:2]
    return round(w / h if h != 0 else 0.0, 2)

def get_ratio_bin(ratio: float) -> str:
    """Определяет текстовый диапазон для гистограммы."""
    if ratio < 0.5:
        return "0-0.5"
    elif 0.5 <= ratio < 1.0:
        return "0.5-1.0"
    elif 1.0 <= ratio < 1.5:
        return "1.0-1.5"
    elif 1.5 <= ratio < 2.0:
        return "1.5-2.0"
    else:
        return "2.0+"

def add_aspect_ratio_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет две новые колонки: точное отношение и диапазон для гистограммы."""
    df["Отношение сторон (w/h)"] = df["Абсолютный путь"].apply(get_image_ratio)
    df["Диапазон отношения сторон"] = df["Отношение сторон (w/h)"].apply(get_ratio_bin)
    return df