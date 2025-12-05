import cv2
import numpy as np

TARGET_SIZE = 256

def resize_with_padding(image, target_size=TARGET_SIZE):
    old_size = image.shape[:2]
    ratio = float(target_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    image = cv2.resize(image, (new_size[1], new_size[0]), interpolation=cv2.INTER_AREA)
    delta_w = target_size - new_size[1]
    delta_h = target_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

def apply_homomorphic_filter(img, d0=10, gamma_l=0.5, gamma_h=2.0, c=2):
    img_log = np.log1p(np.array(img, dtype="float") / 255)
    M, N = img_log.shape
    F = np.fft.fft2(img_log)
    Fshift = np.fft.fftshift(F)
    P = M / 2
    Q = N / 2
    u, v = np.meshgrid(np.arange(N) - Q, np.arange(M) - P)
    D_squared = u**2 + v**2
    H = (gamma_h - gamma_l) * (1 - np.exp(-c * (D_squared / (d0 ** 2)))) + gamma_l
    G_shift = Fshift * H
    G = np.fft.ifftshift(G_shift)
    g = np.fft.ifft2(G)
    g = np.abs(g)
    g = np.expm1(g)
    g = np.clip(g, 0, 1)
    g = np.uint8(g * 255)
    return g

def apply_clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def process_image_pipeline(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = resize_with_padding(img, target_size=TARGET_SIZE)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = apply_homomorphic_filter(img, d0=30, gamma_l=0.5, gamma_h=1.5)
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

    img_processed = process_image_pipeline(img_gray)
    img_normalized = img_processed.astype('float32') / 255.0

    if model_type == 'resnet':
        img_final = np.stack((img_normalized,)*3, axis=-1)
    else:
        img_final = np.expand_dims(img_normalized, axis=-1)

    img_batch = np.expand_dims(img_final, axis=0)
    
    return img_batch