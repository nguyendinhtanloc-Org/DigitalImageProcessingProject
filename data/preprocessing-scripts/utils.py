import cv2
import numpy as np

TARGET_SIZE = 256


def resize_with_padding(image, target_size=TARGET_SIZE):
    h, w = image.shape[:2]
    scale = target_size / max(h, w)

    new_h = int(h * scale)
    new_w = int(w * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    pad_h = target_size - new_h
    pad_w = target_size - new_w

    top = pad_h // 2
    bottom = pad_h - top
    left = pad_w // 2
    right = pad_w - left

    return cv2.copyMakeBorder(resized, top, bottom, left, right,
                              cv2.BORDER_CONSTANT, value=0)


def apply_homomorphic_filter(img, d0=10, gamma_l=0.5, gamma_h=2.0, c=2):
    img_log = np.log1p(img.astype(float) / 255)

    M, N = img_log.shape
    F = np.fft.fft2(img_log)
    F_shift = np.fft.fftshift(F)

    u = np.arange(N) - N / 2
    v = np.arange(M) - M / 2
    U, V = np.meshgrid(u, v)

    D2 = U ** 2 + V ** 2

    H = (gamma_h - gamma_l) * (1 - np.exp(-c * (D2 / (d0 ** 2)))) + gamma_l

    G_shift = F_shift * H
    G = np.fft.ifftshift(G_shift)
    g = np.fft.ifft2(G)
    g = np.abs(g)
    g = np.expm1(g)
    g = np.clip(g, 0, 1)

    return (g * 255).astype(np.uint8)


def apply_clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


def process_image_pipeline(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = resize_with_padding(img, target_size=TARGET_SIZE)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = apply_homomorphic_filter(img, d0=30, gamma_l=0.5, gamma_h=1.2)
    img = apply_clahe(img)

    return img


def preprocess_image_for_model(image_path_or_array, model_type='cnn'):
    if isinstance(image_path_or_array, str):
        img = cv2.imread(image_path_or_array)
    else:
        img = image_path_or_array

    if img is None:
        raise ValueError("Cannot read image")

    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img

    processed = process_image_pipeline(img_gray)
    normalized = processed.astype('float32') / 255.0

    if model_type == 'resnet':
        final = np.stack([normalized] * 3, axis=-1)
    else:
        final = np.expand_dims(normalized, axis=-1)

    return np.expand_dims(final, axis=0)
