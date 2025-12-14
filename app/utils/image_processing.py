"""
Image preprocessing and enhancement utilities
"""
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2


def adjust_brightness(image, factor=1.0):
    """
    Adjust image brightness
    
    Args:
        image: PIL Image
        factor: Brightness factor (0.0 = black, 1.0 = original, >1.0 = brighter)
    
    Returns:
        PIL Image
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image, factor=1.0):
    """
    Adjust image contrast
    
    Args:
        image: PIL Image
        factor: Contrast factor (0.0 = gray, 1.0 = original, >1.0 = more contrast)
    
    Returns:
        PIL Image
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def adjust_sharpness(image, factor=1.0):
    """
    Adjust image sharpness
    
    Args:
        image: PIL Image
        factor: Sharpness factor (0.0 = blurred, 1.0 = original, >1.0 = sharper)
    
    Returns:
        PIL Image
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def apply_clahe(image):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    Useful for enhancing X-ray images
    
    Args:
        image: PIL Image
    
    Returns:
        PIL Image
    """
    # Convert to grayscale if needed
    img_array = np.array(image.convert('L'))
    
    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(img_array)
    
    # Convert back to PIL
    return Image.fromarray(enhanced).convert('RGB')


def denoise_image(image, strength=10):
    """
    Apply denoising filter
    
    Args:
        image: PIL Image
        strength: Denoising strength (higher = more smoothing)
    
    Returns:
        PIL Image
    """
    img_array = np.array(image)
    
    if len(img_array.shape) == 3:
        denoised = cv2.fastNlMeansDenoisingColored(img_array, None, strength, strength, 7, 21)
    else:
        denoised = cv2.fastNlMeansDenoising(img_array, None, strength, 7, 21)
    
    return Image.fromarray(denoised)


def apply_homomorphic_filter(image, gamma_h=2.0, gamma_l=0.5, c=1.0, cutoff=30):
    """
    Apply Homomorphic filtering for illumination normalization
    Useful for X-ray images with uneven lighting
    
    Args:
        image: PIL Image
        gamma_h: High frequency gain (amplify details)
        gamma_l: Low frequency gain (suppress illumination)
        c: Sharpness parameter
        cutoff: Cutoff frequency
    
    Returns:
        PIL Image
    """
    # Convert to grayscale
    img_array = np.array(image.convert('L'), dtype=np.float32)
    
    # Add small epsilon to avoid log(0)
    img_array = np.maximum(img_array, 1.0)
    
    # Take log transform
    img_log = np.log(img_array)
    
    # FFT
    img_fft = np.fft.fft2(img_log)
    img_fft_shift = np.fft.fftshift(img_fft)
    
    # Create Gaussian high-pass filter
    rows, cols = img_array.shape
    crow, ccol = rows // 2, cols // 2
    
    # Create meshgrid for distance calculation
    x = np.arange(-ccol, cols - ccol)
    y = np.arange(-crow, rows - crow)
    X, Y = np.meshgrid(x, y)
    D = np.sqrt(X**2 + Y**2)
    
    # Homomorphic filter H(u,v)
    H = (gamma_h - gamma_l) * (1 - np.exp(-c * (D**2 / cutoff**2))) + gamma_l
    
    # Apply filter
    img_fft_filtered = img_fft_shift * H
    
    # Inverse FFT
    img_ifft = np.fft.ifftshift(img_fft_filtered)
    img_filtered = np.real(np.fft.ifft2(img_ifft))
    
    # Exp to reverse log
    img_exp = np.exp(img_filtered)
    
    # Normalize to 0-255 with better scaling
    img_min = np.min(img_exp)
    img_max = np.max(img_exp)
    img_normalized = ((img_exp - img_min) / (img_max - img_min) * 255).astype(np.uint8)
    
    return Image.fromarray(img_normalized)


def resize_with_aspect_ratio(image, target_size=224):
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: PIL Image
        target_size: Target size for the smaller dimension
    
    Returns:
        PIL Image
    """
    width, height = image.size
    
    if width < height:
        new_width = target_size
        new_height = int(height * target_size / width)
    else:
        new_height = target_size
        new_width = int(width * target_size / height)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def center_crop(image, crop_size=224):
    """
    Center crop image to square
    
    Args:
        image: PIL Image
        crop_size: Size of the crop
    
    Returns:
        PIL Image
    """
    width, height = image.size
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    
    return image.crop((left, top, right, bottom))


def preprocess_xray(image, enhance=True):
    """
    Complete preprocessing pipeline for X-ray images
    
    Args:
        image: PIL Image
        enhance: Apply CLAHE enhancement
    
    Returns:
        PIL Image
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply CLAHE for better contrast
    if enhance:
        image = apply_clahe(image)
    
    # Denoise
    image = denoise_image(image, strength=8)
    
    # Resize with aspect ratio
    image = resize_with_aspect_ratio(image, target_size=256)
    
    # Center crop to square
    image = center_crop(image, crop_size=224)
    
    return image


def create_image_grid(images, predictions, confidences, grid_size=(2, 2)):
    """
    Create a grid of images with predictions (for batch processing)
    
    Args:
        images: List of PIL Images
        predictions: List of prediction labels
        confidences: List of confidence scores
        grid_size: Tuple (rows, cols)
    
    Returns:
        PIL Image of grid
    """
    rows, cols = grid_size
    img_size = 224
    
    # Create blank canvas
    canvas = Image.new('RGB', (cols * img_size, rows * img_size), 'white')
    
    for idx, (img, pred, conf) in enumerate(zip(images, predictions, confidences)):
        if idx >= rows * cols:
            break
        
        row = idx // cols
        col = idx % cols
        
        # Resize image
        img_resized = img.resize((img_size, img_size))
        
        # Paste on canvas
        canvas.paste(img_resized, (col * img_size, row * img_size))
    
    return canvas
