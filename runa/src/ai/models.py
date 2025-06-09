"""
Neural network model definitions for the Runa programming language.

This module provides the functionality to create and manage neural network models
using TensorFlow and PyTorch backends.
"""

import os
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import importlib.util

# Check if TensorFlow is available
tf_available = importlib.util.find_spec("tensorflow") is not None
if tf_available:
    import tensorflow as tf

# Check if PyTorch is available
torch_available = importlib.util.find_spec("torch") is not None
if torch_available:
    import torch
    import torch.nn as nn


class ModelBackendError(Exception):
    """Exception raised when a required model backend is not available."""
    pass


def check_tensorflow_available():
    """Check if TensorFlow is available, raise an error if not."""
    if not tf_available:
        raise ModelBackendError(
            "TensorFlow is not installed. Please install TensorFlow to use "
            "TensorFlow-based neural network models in Runa."
        )


def check_pytorch_available():
    """Check if PyTorch is available, raise an error if not."""
    if not torch_available:
        raise ModelBackendError(
            "PyTorch is not installed. Please install PyTorch to use "
            "PyTorch-based neural network models in Runa."
        )


def create_tensorflow_model(
    model_def: Dict[str, Any]
) -> 'tf.keras.Model':
    """
    Create a TensorFlow model from a Runa model definition.
    
    Args:
        model_def: A dictionary containing the model definition
        
    Returns:
        A TensorFlow Keras model
        
    Raises:
        ModelBackendError: If TensorFlow is not installed
    """
    check_tensorflow_available()
    
    # Extract model configuration
    input_shape = model_def.get("input_shape", (224, 224, 3))
    filters = model_def.get("filters", 32)
    double_filters = model_def.get("double_filters", True)
    use_residual = model_def.get("use_residual", False)
    num_classes = model_def.get("num_classes", 1000)
    activation = model_def.get("activation", "softmax")
    
    # Create model
    inputs = tf.keras.layers.Input(shape=input_shape)
    x = inputs
    
    # Initial convolution layer
    x = tf.keras.layers.Conv2D(filters, (3, 3), padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    
    # Downsample blocks
    num_blocks = 4
    for i in range(num_blocks):
        res = x
        current_filters = filters * (2 ** i if double_filters else 1)
        
        # Convolution block
        x = tf.keras.layers.Conv2D(current_filters, (3, 3), padding="same")(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)
        x = tf.keras.layers.Conv2D(current_filters, (3, 3), padding="same")(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        # Add residual connection if specified
        if use_residual:
            if res.shape[-1] != current_filters:
                res = tf.keras.layers.Conv2D(current_filters, (1, 1))(res)
            x = tf.keras.layers.Add()([x, res])
        
        x = tf.keras.layers.Activation("relu")(x)
        
        # Downsample except for the last block
        if i < num_blocks - 1:
            x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    # Global pooling and output layer
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(num_classes)(x)
    outputs = tf.keras.layers.Activation(activation)(x)
    
    model = tf.keras.Model(inputs, outputs)
    return model


def create_pytorch_model(
    model_def: Dict[str, Any]
) -> 'nn.Module':
    """
    Create a PyTorch model from a Runa model definition.
    
    Args:
        model_def: A dictionary containing the model definition
        
    Returns:
        A PyTorch nn.Module
        
    Raises:
        ModelBackendError: If PyTorch is not installed
    """
    check_pytorch_available()
    
    class RunaModel(nn.Module):
        def __init__(
            self,
            input_shape: Tuple[int, ...],
            filters: int,
            double_filters: bool,
            use_residual: bool,
            num_classes: int,
            activation: str
        ):
            super().__init__()
            
            self.input_shape = input_shape
            self.use_residual = use_residual
            self.activation_name = activation
            
            # Initial convolution layer
            self.initial_conv = nn.Sequential(
                nn.Conv2d(input_shape[0], filters, kernel_size=3, padding=1),
                nn.BatchNorm2d(filters),
                nn.ReLU()
            )
            
            # Downsample blocks
            self.blocks = nn.ModuleList()
            self.downsamples = nn.ModuleList()
            self.shortcuts = nn.ModuleList()
            
            num_blocks = 4
            in_channels = filters
            
            for i in range(num_blocks):
                current_filters = filters * (2 ** i if double_filters else 1)
                
                # Conv block
                block = nn.Sequential(
                    nn.Conv2d(in_channels, current_filters, kernel_size=3, padding=1),
                    nn.BatchNorm2d(current_filters),
                    nn.ReLU(),
                    nn.Conv2d(current_filters, current_filters, kernel_size=3, padding=1),
                    nn.BatchNorm2d(current_filters)
                )
                self.blocks.append(block)
                
                # Shortcut connection if needed
                if use_residual and in_channels != current_filters:
                    shortcut = nn.Conv2d(in_channels, current_filters, kernel_size=1)
                else:
                    shortcut = nn.Identity()
                self.shortcuts.append(shortcut)
                
                # Downsample except for the last block
                if i < num_blocks - 1:
                    self.downsamples.append(nn.MaxPool2d(kernel_size=2))
                else:
                    self.downsamples.append(nn.Identity())
                
                in_channels = current_filters
            
            # Global pooling and output layer
            self.global_pool = nn.AdaptiveAvgPool2d(1)
            self.classifier = nn.Linear(in_channels, num_classes)
            
            # Set activation function
            if activation == "softmax":
                self.activation = nn.Softmax(dim=1)
            elif activation == "sigmoid":
                self.activation = nn.Sigmoid()
            else:
                self.activation = nn.Identity()
        
        def forward(self, x):
            # Initial convolution
            x = self.initial_conv(x)
            
            # Process blocks with residual connections
            for i, (block, shortcut, downsample) in enumerate(
                zip(self.blocks, self.shortcuts, self.downsamples)
            ):
                residual = shortcut(x)
                x = block(x)
                
                if self.use_residual:
                    x = x + residual
                
                x = nn.functional.relu(x)
                x = downsample(x)
            
            # Global pooling and classification
            x = self.global_pool(x)
            x = x.view(x.size(0), -1)
            x = self.classifier(x)
            x = self.activation(x)
            
            return x
    
    # Extract model configuration
    input_shape = model_def.get("input_shape", (3, 224, 224))  # PyTorch uses channels-first
    filters = model_def.get("filters", 32)
    double_filters = model_def.get("double_filters", True)
    use_residual = model_def.get("use_residual", False)
    num_classes = model_def.get("num_classes", 1000)
    activation = model_def.get("activation", "softmax")
    
    # Create and return model
    model = RunaModel(
        input_shape=input_shape,
        filters=filters,
        double_filters=double_filters,
        use_residual=use_residual,
        num_classes=num_classes,
        activation=activation
    )
    
    return model


def save_model(
    model: Union['tf.keras.Model', 'nn.Module'],
    path: str,
    model_format: str = "auto"
) -> None:
    """
    Save a neural network model to disk.
    
    Args:
        model: The model to save (TensorFlow or PyTorch)
        path: The path to save the model to
        model_format: The format to save the model in ('tf', 'pytorch', or 'auto')
        
    Raises:
        ModelBackendError: If the required backend is not installed
        ValueError: If the model format is not supported
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    # Determine model type
    if model_format == "auto":
        if tf_available and isinstance(model, tf.keras.Model):
            model_format = "tf"
        elif torch_available and isinstance(model, nn.Module):
            model_format = "pytorch"
        else:
            raise ValueError("Could not automatically determine model format")
    
    # Save model based on format
    if model_format == "tf":
        check_tensorflow_available()
        model.save(path)
    elif model_format == "pytorch":
        check_pytorch_available()
        
        # Save the model weights
        torch.save(model.state_dict(), path)
        
        # Extract and save the model architecture
        model_dir = os.path.dirname(path)
        model_name = os.path.basename(path).split('.')[0]
        architecture_path = os.path.join(model_dir, f"{model_name}_architecture.json")
        
        # Extract model architecture parameters
        architecture = {
            "input_shape": getattr(model, "input_shape", (3, 224, 224)),
            "filters": getattr(model, "filters", 32),
            "double_filters": True,
            "use_residual": getattr(model, "use_residual", False),
            "num_classes": model.classifier.out_features if hasattr(model, "classifier") else 1000,
            "activation": getattr(model, "activation_name", "softmax")
        }
        
        # Save the architecture as JSON
        with open(architecture_path, 'w') as f:
            json.dump(architecture, f, indent=4)
    else:
        raise ValueError(f"Unsupported model format: {model_format}")


def load_model(
    path: str,
    model_format: str = "auto"
) -> Union['tf.keras.Model', 'nn.Module']:
    """
    Load a neural network model from disk.
    
    Args:
        path: The path to load the model from
        model_format: The format of the model ('tf', 'pytorch', or 'auto')
        
    Returns:
        The loaded model
        
    Raises:
        ModelBackendError: If the required backend is not installed
        ValueError: If the model format is not supported
        FileNotFoundError: If the model file doesn't exist
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    
    # Auto-detect model format if not specified
    if model_format == "auto":
        if os.path.isdir(path) or path.endswith(".h5") or path.endswith(".keras"):
            model_format = "tf"
        elif path.endswith(".pt") or path.endswith(".pth"):
            model_format = "pytorch"
        else:
            raise ValueError("Could not automatically determine model format")
    
    # Load model based on format
    if model_format == "tf":
        check_tensorflow_available()
        return tf.keras.models.load_model(path)
    elif model_format == "pytorch":
        check_pytorch_available()
        
        # Check for the architecture file
        model_dir = os.path.dirname(path)
        model_name = os.path.basename(path).split('.')[0]
        architecture_path = os.path.join(model_dir, f"{model_name}_architecture.json")
        
        if not os.path.exists(architecture_path):
            raise FileNotFoundError(
                f"PyTorch model architecture file not found: {architecture_path}. "
                "When saving a PyTorch model, ensure to save the architecture too."
            )
        
        # Load the architecture
        with open(architecture_path, 'r') as f:
            architecture = json.load(f)
        
        # Create the model based on the architecture
        model = create_pytorch_model(architecture)
        
        # Load the model weights
        model.load_state_dict(torch.load(path))
        model.eval()
        
        return model
    else:
        raise ValueError(f"Unsupported model format: {model_format}") 