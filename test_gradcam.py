"""
Test Grad-CAM generation directly
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
sys.path.append('app')

from utils.visualization import generate_gradcam_heatmap

print("Loading model...")
model = keras.models.load_model('models/cnn_pneumonia_model.keras')

print("\nCreating test input...")
test_input = np.random.rand(1, 144, 144, 1).astype(np.float32)

print("\nModel layers:")
for i, layer in enumerate(model.layers):
    if isinstance(layer, keras.layers.Conv2D):
        print(f"  {i}: {layer.name} (Conv2D)")

print("\nAttempting to generate Grad-CAM...")
try:
    heatmap = generate_gradcam_heatmap(model, test_input)
    print(f"✅ SUCCESS! Heatmap shape: {heatmap.shape}")
    print(f"Heatmap min: {heatmap.min():.4f}, max: {heatmap.max():.4f}")
except Exception as e:
    print(f"❌ FAILED!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    
    # Try to debug more
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Check if we can manually create grad_model
    print("\n" + "="*60)
    print("DEBUGGING: Manual grad_model creation")
    print("="*60)
    
    # First call model to build it
    print("1. Building model with forward pass...")
    _ = model(test_input, training=False)
    print("   ✓ Model built")
    
    # Find last conv layer
    print("\n2. Finding last Conv2D layer...")
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, keras.layers.Conv2D):
            last_conv_layer = layer
            print(f"   ✓ Found: {layer.name}")
            break
    
    if last_conv_layer is None:
        print("   ❌ No Conv2D layer found!")
        sys.exit(1)
    
    # Try to get layer output
    print(f"\n3. Getting layer '{last_conv_layer.name}' output...")
    try:
        layer_output = last_conv_layer.output
        print(f"   ✓ Output tensor: {layer_output}")
    except Exception as e2:
        print(f"   ❌ Failed: {e2}")
        sys.exit(1)
    
    # Try to create grad_model
    print("\n4. Creating grad_model...")
    try:
        grad_model = keras.models.Model(
            inputs=model.input,
            outputs=[last_conv_layer.output, model.output]
        )
        print(f"   ✓ Grad model created")
        
        # Test grad_model
        print("\n5. Testing grad_model...")
        conv_out, pred_out = grad_model(test_input)
        print(f"   ✓ Conv output shape: {conv_out.shape}")
        print(f"   ✓ Prediction output shape: {pred_out.shape}")
        
    except Exception as e3:
        print(f"   ❌ Failed: {e3}")
        import traceback
        traceback.print_exc()
