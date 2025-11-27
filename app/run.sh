#!/bin/bash

# Script to run Streamlit app with macOS threading fix

echo "🚀 Starting Pneumonia Detection App..."

# Set environment variable to fix macOS threading issue
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Activate virtual environment
source venv/bin/activate

# Check if models exist
if [ ! -f "../models/cnn_best.h5" ] || [ ! -f "../models/resnet50_best.h5" ]; then
    echo "⚠️  WARNING: Models not found!"
    echo "Please train models on Kaggle first:"
    echo "  1. Upload notebooks/CNN.ipynb and notebooks/ResNet.ipynb to Kaggle"
    echo "  2. Enable GPU and run training"
    echo "  3. Download cnn_best.h5 and resnet50_best.h5"
    echo "  4. Place them in models/ folder"
    echo ""
    echo "App will run with limited functionality (no predictions)."
    echo ""
fi

# Run Streamlit
echo "Opening app at http://localhost:8501"
python -m streamlit run app.py
