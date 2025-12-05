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
