import cv2

def pixelate_image(image, pixel_size: int):
    """Преобразует изображение в пиксель-арт."""
    if pixel_size <= 1:
        return image.copy()

    h, w = image.shape[:2]
    small = cv2.resize(image, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated