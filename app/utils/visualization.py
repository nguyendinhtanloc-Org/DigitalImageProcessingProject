"""
Visualization utilities for Streamlit app
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow import keras


def generate_gradcam_heatmap(model, img_array, last_conv_layer_name=None):
    """
    Generate Grad-CAM heatmap for visualization
    
    Args:
        model: Keras model
        img_array: Preprocessed image array
        last_conv_layer_name: Name of last conv layer (auto-detect if None)
    
    Returns:
        heatmap: numpy array of heatmap
    """
    # For Sequential models, we need to build it first
    # Call the model once to ensure all layers are built
    _ = model(img_array, training=False)
    
    # Auto-detect last conv layer if not specified
    if last_conv_layer_name is None:
        last_conv_layer_name = None
        for layer in reversed(model.layers):
            if isinstance(layer, keras.layers.Conv2D):
                last_conv_layer_name = layer.name
                break
        
        if last_conv_layer_name is None:
            raise ValueError("No Conv2D layer found in model")
    
    # Get the last conv layer
    last_conv_layer = model.get_layer(last_conv_layer_name)
    
    # CRITICAL: Remove sigmoid activation from final Dense layer to get raw logits
    # This prevents gradient saturation when prediction is 0.0 or 1.0
    # Find and clone the model without final activation
    try:
        # Method 1: Try to access Dense layer and remove activation
        dense_layers = [l for l in model.layers if isinstance(l, keras.layers.Dense) and l.units == 1]
        
        if dense_layers:
            final_dense = dense_layers[-1]
            
            # Create a new model that outputs logits (before sigmoid)
            # We'll construct functional model without final activation
            input_shape = img_array.shape[1:]
            new_input = keras.Input(shape=input_shape)
            
            x = new_input
            conv_output = None
            logit_output = None
            
            for layer in model.layers[:-1]:  # All layers except last Dense
                if isinstance(layer, keras.layers.Dropout):
                    x = layer(x, training=False)  # Dropout off during inference
                else:
                    x = layer(x)
                
                if layer.name == last_conv_layer_name:
                    conv_output = x
            
            # Add final Dense layer WITHOUT activation
            logit_output = keras.layers.Dense(1, name='logits_no_activation')(x)
            
            # Create grad model
            grad_model = keras.models.Model(
                inputs=new_input,
                outputs=[conv_output, logit_output]
            )
            
            # Copy weights from original Dense layer
            grad_model.get_layer('logits_no_activation').set_weights(final_dense.get_weights())
            
        else:
            raise ValueError("Cannot find final Dense layer")
            
    except Exception as e:
        print(f"[WARNING] Failed to remove sigmoid: {e}")
        # Fallback to original approach
        try:
            grad_model = keras.models.Model(
                inputs=model.input,
                outputs=[last_conv_layer.output, model.output]
            )
        except AttributeError:
            input_shape = img_array.shape[1:]
            new_input = keras.Input(shape=input_shape)
            
            x = new_input
            conv_output = None
            
            for layer in model.layers:
                x = layer(x)
                if layer.name == last_conv_layer_name:
                    conv_output = x
            
            grad_model = keras.models.Model(
                inputs=new_input,
                outputs=[conv_output, x]
            )
    
    # Compute gradient using GradientTape
    with tf.GradientTape() as tape:
        # Forward pass - tape will automatically watch trainable variables
        conv_outputs, logits = grad_model(img_array)
        
        # Watch conv_outputs explicitly for gradient computation
        tape.watch(conv_outputs)
        
        # For saturated predictions, we still compute gradient
        # Use the raw output value (logits or predictions)
        class_output = logits[0, 0]
    
    # Debug: print predictions
    print(f"[DEBUG] Logits: {logits.numpy()}")
    print(f"[DEBUG] Class output value: {class_output.numpy():.4f}")
    
    # Compute gradients of output wrt conv outputs
    # Even if output is saturated, we may still get some gradients from earlier layers
    grads = tape.gradient(class_output, conv_outputs)
    
    # Debug: check gradients
    if grads is None:
        print("[ERROR] Gradients are None!")
        return np.zeros((18, 18))  # Return empty heatmap
    
    print(f"[DEBUG] Grads shape: {grads.shape}, min: {tf.reduce_min(grads).numpy():.6f}, max: {tf.reduce_max(grads).numpy():.6f}")
    
    # Use ReLU on gradients (only positive gradients)
    # This helps with saturated activations
    grads = tf.nn.relu(grads)
    
    print(f"[DEBUG] After ReLU - Grads min: {tf.reduce_min(grads).numpy():.6f}, max: {tf.reduce_max(grads).numpy():.6f}")
    
    # Compute guided gradients (average pooling)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    print(f"[DEBUG] Pooled grads min: {tf.reduce_min(pooled_grads).numpy():.6f}, max: {tf.reduce_max(pooled_grads).numpy():.6f}")
    
    # Weight the conv outputs by the gradients
    conv_outputs = conv_outputs[0]
    pooled_grads = pooled_grads[..., tf.newaxis]
    heatmap = conv_outputs @ pooled_grads
    heatmap = tf.squeeze(heatmap)
    
    print(f"[DEBUG] Heatmap before normalize - min: {tf.reduce_min(heatmap).numpy():.4f}, max: {tf.reduce_max(heatmap).numpy():.4f}")
    
    # Normalize heatmap to [0, 1]
    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val
    else:
        print("[WARNING] Heatmap max value is 0! Returning empty heatmap.")
    
    print(f"[DEBUG] Final heatmap - min: {tf.reduce_min(heatmap).numpy():.4f}, max: {tf.reduce_max(heatmap).numpy():.4f}")
    
    return heatmap.numpy()


def overlay_heatmap_on_image(image, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap on original image
    
    Args:
        image: PIL Image or numpy array
        heatmap: Grad-CAM heatmap (2D array)
        alpha: Transparency of heatmap overlay
        colormap: OpenCV colormap
    
    Returns:
        superimposed_img: PIL Image with heatmap overlay
    """
    # Convert PIL to numpy if needed
    if isinstance(image, Image.Image):
        img = np.array(image)
    else:
        img = image
    
    # Ensure image is RGB (convert grayscale to RGB if needed)
    if len(img.shape) == 2:  # Grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    elif img.shape[2] == 1:  # Grayscale with channel dimension
        img = cv2.cvtColor(img.squeeze(), cv2.COLOR_GRAY2RGB)
    
    # Resize heatmap to match image dimensions
    heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to RGB color map
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    # Ensure both images have the same dtype and shape
    img = img.astype(np.float32)
    heatmap_colored = heatmap_colored.astype(np.float32)
    
    # Blend heatmap with original image
    superimposed_img = heatmap_colored * alpha + img * (1 - alpha)
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    
    return Image.fromarray(superimposed_img)


def plot_confidence_gauge(confidence, prediction):
    """
    Create a gauge chart for confidence visualization
    
    Args:
        confidence: Confidence score (0-100)
        prediction: "Normal" or "Pneumonia"
    
    Returns:
        fig: Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Colors
    if prediction.lower() == "normal":
        color = '#10b981'  # Green
    else:
        color = '#ef4444'  # Red
    
    # Create gauge
    ax.barh(0, confidence, height=0.5, color=color, alpha=0.8)
    ax.barh(0, 100 - confidence, left=confidence, height=0.5, color='#e5e7eb', alpha=0.5)
    
    # Styling
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Confidence (%)', fontsize=12)
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add text
    ax.text(confidence / 2, 0, f'{confidence:.1f}%', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    plt.tight_layout()
    return fig


def plot_training_history(history_dict):
    """
    Plot training history (accuracy and loss curves)
    
    Args:
        history_dict: Dictionary with 'accuracy', 'val_accuracy', 'loss', 'val_loss'
    
    Returns:
        fig: Matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy
    ax1.plot(history_dict['accuracy'], label='Training', linewidth=2)
    ax1.plot(history_dict['val_accuracy'], label='Validation', linewidth=2)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Loss
    ax2.plot(history_dict['loss'], label='Training', linewidth=2)
    ax2.plot(history_dict['val_loss'], label='Validation', linewidth=2)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def create_comparison_table(cnn_metrics, resnet_metrics):
    """
    Create model comparison table using Streamlit dataframe
    
    Args:
        cnn_metrics: Dict with CNN metrics
        resnet_metrics: Dict with ResNet metrics
    
    Returns:
        Pandas DataFrame for display
    """
    import pandas as pd
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    
    data = []
    for metric, label in zip(metrics, labels):
        cnn_val = cnn_metrics.get(metric, 0)
        resnet_val = resnet_metrics.get(metric, 0)
        winner = 'CNN' if cnn_val > resnet_val else 'ResNet-50'
        
        data.append({
            'Metric': label,
            'CNN': f"{cnn_val:.1%}",
            'ResNet-50': f"{resnet_val:.1%}",
            'Winner': winner
        })
    
    df = pd.DataFrame(data)
    return df


def create_metrics_cards(accuracy, precision, recall, f1_score):
    """
    Create HTML cards for metrics display
    
    Args:
        accuracy, precision, recall, f1_score: Float values (0-1)
    
    Returns:
        HTML string with metric cards
    """
    metrics = [
        ('Accuracy', accuracy, '#3b82f6'),
        ('Precision', precision, '#10b981'),
        ('Recall', recall, '#f59e0b'),
        ('F1 Score', f1_score, '#8b5cf6')
    ]
    
    cards_html = "<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0;'>"
    
    for name, value, color in metrics:
        cards_html += f"""
<div style="background: white; padding: 1.2rem; border-radius: 10px; border-left: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
    <div style="color: #64748b; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">{name}</div>
    <div style="color: {color}; font-size: 2rem; font-weight: 700;">{value:.1%}</div>
</div>
"""
    
    cards_html += "</div>"
    return cards_html
