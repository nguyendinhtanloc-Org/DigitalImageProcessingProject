"""
Debug script to inspect CNN model structure for Grad-CAM
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np

print("Loading model...")
model = keras.models.load_model('models/cnn_pneumonia_model.keras')

print("\n" + "="*60)
print("MODEL SUMMARY")
print("="*60)
model.summary()

print("\n" + "="*60)
print("LAYER DETAILS")
print("="*60)
for i, layer in enumerate(model.layers):
    print(f"{i}: {layer.name} ({layer.__class__.__name__})")
    if hasattr(layer, 'output_shape'):
        print(f"   Output shape: {layer.output_shape}")

print("\n" + "="*60)
print("LOOKING FOR CONV2D LAYERS")
print("="*60)
conv_layers = []
for layer in model.layers:
    if isinstance(layer, keras.layers.Conv2D):
        conv_layers.append(layer.name)
        print(f"✓ Found Conv2D: {layer.name}")

if not conv_layers:
    print("❌ NO Conv2D layers found!")
else:
    print(f"\n✅ Total Conv2D layers: {len(conv_layers)}")
    print(f"Last Conv2D layer: {conv_layers[-1]}")

print("\n" + "="*60)
print("TEST PREDICTION")
print("="*60)

# Try to find input shape from first layer
first_layer = model.layers[0]
if hasattr(first_layer, 'input_shape'):
    expected_shape = first_layer.input_shape
    print(f"Expected input shape from first layer: {expected_shape}")

# Create dummy inputs with different sizes to test
test_sizes = [
    (1, 144, 144, 1),
    (1, 150, 150, 1),  # From model summary
    (1, 224, 224, 1),
]

for test_shape in test_sizes:
    print(f"\nTesting with input shape: {test_shape}")
    try:
        dummy_input = np.random.rand(*test_shape).astype(np.float32)
        output = model.predict(dummy_input, verbose=0)
        print(f"  ✅ SUCCESS! Output shape: {output.shape}, value: {output[0][0]:.4f}")
        break
    except Exception as e:
        print(f"  ❌ FAILED: {str(e)[:100]}")

print("\n" + "="*60)
print("MODEL TYPE CHECK")
print("="*60)
print(f"Model type: {type(model)}")
print(f"Is Functional? {isinstance(model, keras.models.Model)}")
print(f"Is Sequential? {isinstance(model, keras.models.Sequential)}")

# Check if model has functional API structure
if hasattr(model, '_is_graph_network'):
    print(f"Is graph network: {model._is_graph_network}")
