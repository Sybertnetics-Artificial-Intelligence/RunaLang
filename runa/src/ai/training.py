"""
Training utilities for neural network models in the Runa programming language.

This module provides functionality for training and evaluating neural network models
using TensorFlow and PyTorch backends.
"""

import os
import json
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
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
    from torch.utils.data import DataLoader, Dataset

from .models import ModelBackendError, check_tensorflow_available, check_pytorch_available


def configure_training(
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Configure the training process based on the provided configuration.
    
    Args:
        config: A dictionary containing the training configuration
    
    Returns:
        A dictionary with the processed training configuration
    """
    # Set default values for common training parameters
    defaults = {
        "batch_size": 32,
        "learning_rate": 0.001,
        "optimizer": "adam",
        "epochs": 10,
        "validation_split": 0.2,
        "early_stopping": True,
        "early_stopping_patience": 5,
        "model_checkpoint": True,
        "augmentation": None,
    }
    
    # Merge defaults with provided config
    for key, value in defaults.items():
        if key not in config:
            config[key] = value
    
    return config


def _prepare_tensorflow_dataset(
    dataset_path: str,
    config: Dict[str, Any]
) -> Tuple['tf.data.Dataset', 'tf.data.Dataset']:
    """
    Prepare a TensorFlow dataset for training.
    
    Args:
        dataset_path: Path to the dataset
        config: Training configuration
    
    Returns:
        A tuple of (train_dataset, validation_dataset)
    
    Raises:
        ModelBackendError: If TensorFlow is not installed
        ValueError: If the dataset format is not supported
    """
    check_tensorflow_available()
    
    batch_size = config.get("batch_size", 32)
    validation_split = config.get("validation_split", 0.2)
    augmentation = config.get("augmentation", None)
    
    # Check if the dataset is a directory (for image datasets)
    if os.path.isdir(dataset_path):
        # Image dataset - use image_dataset_from_directory
        train_dataset = tf.keras.utils.image_dataset_from_directory(
            dataset_path,
            validation_split=validation_split,
            subset="training",
            seed=42,
            batch_size=batch_size,
        )
        
        validation_dataset = tf.keras.utils.image_dataset_from_directory(
            dataset_path,
            validation_split=validation_split,
            subset="validation",
            seed=42,
            batch_size=batch_size,
        )
        
        # Configure dataset for performance
        AUTOTUNE = tf.data.AUTOTUNE
        train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)
        
        # Apply data augmentation if specified
        if augmentation:
            data_augmentation = tf.keras.Sequential([
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomRotation(0.2),
                tf.keras.layers.RandomZoom(0.2),
            ])
            
            train_dataset = train_dataset.map(
                lambda x, y: (data_augmentation(x, training=True), y),
                num_parallel_calls=AUTOTUNE
            )
    
    # Other dataset formats could be added here (CSV, JSON, etc.)
    else:
        raise ValueError(f"Unsupported dataset format: {dataset_path}")
    
    return train_dataset, validation_dataset


def _prepare_pytorch_dataset(
    dataset_path: str,
    config: Dict[str, Any]
) -> Tuple[DataLoader, DataLoader]:
    """
    Prepare a PyTorch dataset for training.
    
    Args:
        dataset_path: Path to the dataset
        config: Training configuration
    
    Returns:
        A tuple of (train_loader, validation_loader)
    
    Raises:
        ModelBackendError: If PyTorch is not installed
        ValueError: If the dataset format is not supported
    """
    check_pytorch_available()
    
    batch_size = config.get("batch_size", 32)
    validation_split = config.get("validation_split", 0.2)
    augmentation = config.get("augmentation", None)
    
    # For image datasets (directory of images)
    if os.path.isdir(dataset_path):
        from torchvision import datasets, transforms
        
        # Define transforms
        transform_list = [
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ]
        
        # Add augmentation if specified
        if augmentation:
            augmentation_transforms = [
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(20),
                transforms.RandomResizedCrop(224, scale=(0.8, 1.0))
            ]
            train_transform = transforms.Compose(augmentation_transforms + transform_list)
        else:
            train_transform = transforms.Compose(transform_list)
        
        # Validation transforms (no augmentation)
        val_transform = transforms.Compose(transform_list)
        
        # Load the dataset
        full_dataset = datasets.ImageFolder(dataset_path, transform=train_transform)
        
        # Split into train and validation
        dataset_size = len(full_dataset)
        val_size = int(validation_split * dataset_size)
        train_size = dataset_size - val_size
        
        # Use random_split to create train and validation datasets
        train_dataset, val_dataset = torch.utils.data.random_split(
            full_dataset, [train_size, val_size]
        )
        
        # Update validation dataset transform
        val_dataset.dataset = datasets.ImageFolder(dataset_path, transform=val_transform)
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size,
            shuffle=False,
            num_workers=4,
            pin_memory=True
        )
        
        return train_loader, val_loader
    
    # For CSV datasets
    elif dataset_path.endswith('.csv'):
        import pandas as pd
        import numpy as np
        
        class CSVDataset(Dataset):
            def __init__(self, file_path, transform=None):
                self.data = pd.read_csv(file_path)
                self.transform = transform
                
                # Assume last column is target by default
                self.features = self.data.iloc[:, :-1].values.astype(np.float32)
                self.targets = self.data.iloc[:, -1].values.astype(np.int64)
            
            def __len__(self):
                return len(self.data)
            
            def __getitem__(self, idx):
                x = self.features[idx]
                y = self.targets[idx]
                
                if self.transform:
                    x = self.transform(x)
                
                return x, y
        
        # Create full dataset
        full_dataset = CSVDataset(dataset_path)
        
        # Split into train and validation
        dataset_size = len(full_dataset)
        val_size = int(validation_split * dataset_size)
        train_size = dataset_size - val_size
        
        train_dataset, val_dataset = torch.utils.data.random_split(
            full_dataset, [train_size, val_size]
        )
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size,
            shuffle=True
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size,
            shuffle=False
        )
        
        return train_loader, val_loader
    
    # For NPZ/numpy datasets
    elif dataset_path.endswith('.npz'):
        class NumpyDataset(Dataset):
            def __init__(self, file_path, transform=None):
                data = np.load(file_path)
                self.features = data['features'].astype(np.float32)
                self.targets = data['targets'].astype(np.int64)
                self.transform = transform
            
            def __len__(self):
                return len(self.features)
            
            def __getitem__(self, idx):
                x = self.features[idx]
                y = self.targets[idx]
                
                if self.transform:
                    x = torch.from_numpy(x)
                    x = self.transform(x)
                else:
                    x = torch.from_numpy(x)
                
                return x, torch.tensor(y)
        
        # Create full dataset
        full_dataset = NumpyDataset(dataset_path)
        
        # Split into train and validation
        dataset_size = len(full_dataset)
        val_size = int(validation_split * dataset_size)
        train_size = dataset_size - val_size
        
        train_dataset, val_dataset = torch.utils.data.random_split(
            full_dataset, [train_size, val_size]
        )
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size,
            shuffle=True
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size,
            shuffle=False
        )
        
        return train_loader, val_loader
    
    else:
        raise ValueError(f"Unsupported dataset format: {dataset_path}")


def train_model(
    model: Union['tf.keras.Model', 'nn.Module'],
    dataset_path: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Train a neural network model.
    
    Args:
        model: The model to train (TensorFlow or PyTorch)
        dataset_path: Path to the dataset
        config: Training configuration
    
    Returns:
        A dictionary containing training history and metrics
    
    Raises:
        ModelBackendError: If the required backend is not installed
        ValueError: If the model or dataset format is not supported
    """
    # Configure training parameters
    config = configure_training(config)
    
    # Determine model type
    if tf_available and isinstance(model, tf.keras.Model):
        return _train_tensorflow_model(model, dataset_path, config)
    elif torch_available and isinstance(model, nn.Module):
        return _train_pytorch_model(model, dataset_path, config)
    else:
        raise ValueError("Unsupported model type")


def _train_tensorflow_model(
    model: 'tf.keras.Model',
    dataset_path: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Train a TensorFlow model.
    
    Args:
        model: The TensorFlow model to train
        dataset_path: Path to the dataset
        config: Training configuration
    
    Returns:
        A dictionary containing training history and metrics
    """
    check_tensorflow_available()
    
    # Extract training parameters
    epochs = config.get("epochs", 10)
    learning_rate = config.get("learning_rate", 0.001)
    optimizer_name = config.get("optimizer", "adam")
    early_stopping = config.get("early_stopping", True)
    early_stopping_patience = config.get("early_stopping_patience", 5)
    model_checkpoint = config.get("model_checkpoint", True)
    save_path = config.get("save_path", "model_checkpoints")
    
    # Create optimizer
    if optimizer_name.lower() == "adam":
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    elif optimizer_name.lower() == "sgd":
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    elif optimizer_name.lower() == "rmsprop":
        optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
    else:
        raise ValueError(f"Unsupported optimizer: {optimizer_name}")
    
    # Compile the model
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    # Prepare dataset
    train_dataset, validation_dataset = _prepare_tensorflow_dataset(dataset_path, config)
    
    # Prepare callbacks
    callbacks = []
    
    if early_stopping:
        callbacks.append(tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=early_stopping_patience,
            restore_best_weights=True
        ))
    
    if model_checkpoint:
        os.makedirs(save_path, exist_ok=True)
        callbacks.append(tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(save_path, "model_{epoch:02d}_{val_accuracy:.4f}.h5"),
            monitor="val_accuracy",
            save_best_only=True
        ))
    
    # Train the model
    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=epochs,
        callbacks=callbacks
    )
    
    # Evaluate the model
    evaluation = model.evaluate(validation_dataset)
    
    # Return training results
    return {
        "history": history.history,
        "evaluation": {
            "loss": evaluation[0],
            "accuracy": evaluation[1]
        }
    }


def _train_pytorch_model(
    model: 'nn.Module',
    dataset_path: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Train a PyTorch model.
    
    Args:
        model: The PyTorch model to train
        dataset_path: Path to the dataset
        config: Training configuration
    
    Returns:
        A dictionary containing training history and metrics
    
    Raises:
        ModelBackendError: If PyTorch is not installed
        ValueError: If the dataset format is not supported
    """
    check_pytorch_available()
    
    # Prepare dataset
    train_loader, val_loader = _prepare_pytorch_dataset(dataset_path, config)
    
    # Extract training parameters
    epochs = config.get("epochs", 10)
    learning_rate = config.get("learning_rate", 0.001)
    optimizer_name = config.get("optimizer", "adam")
    early_stopping = config.get("early_stopping", True)
    early_stopping_patience = config.get("early_stopping_patience", 5)
    model_checkpoint = config.get("model_checkpoint", True)
    
    # Configure optimizer
    if optimizer_name.lower() == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    elif optimizer_name.lower() == "sgd":
        momentum = config.get("momentum", 0.9)
        optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)
    elif optimizer_name.lower() == "adamw":
        weight_decay = config.get("weight_decay", 0.01)
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    else:
        raise ValueError(f"Unsupported optimizer: {optimizer_name}")
    
    # Configure loss function based on task (classification by default)
    task = config.get("task", "classification")
    if task == "classification":
        if config.get("num_classes", 0) > 1:  # Multi-class
            criterion = nn.CrossEntropyLoss()
        else:  # Binary classification
            criterion = nn.BCEWithLogitsLoss()
    elif task == "regression":
        criterion = nn.MSELoss()
    else:
        raise ValueError(f"Unsupported task: {task}")
    
    # Learning rate scheduler
    scheduler = None
    if config.get("lr_scheduler", False):
        scheduler_type = config.get("scheduler_type", "reduce_on_plateau")
        if scheduler_type == "reduce_on_plateau":
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, 
                mode='min', 
                factor=0.5, 
                patience=3
            )
        elif scheduler_type == "cosine_annealing":
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer,
                T_max=epochs
            )
    
    # Initialize variables for early stopping and checkpointing
    best_val_loss = float('inf')
    patience_counter = 0
    checkpoint_path = None
    
    if model_checkpoint:
        checkpoint_dir = config.get("checkpoint_dir", "./checkpoints")
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint_path = os.path.join(checkpoint_dir, "best_model.pt")
    
    # Training history
    history = {
        "train_loss": [],
        "val_loss": [],
        "train_acc": [],
        "val_acc": []
    }
    
    # Move model to GPU if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Training loop
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            
            # Adjust targets shape for binary classification if needed
            if task == "classification" and config.get("num_classes", 0) == 1:
                targets = targets.float().unsqueeze(1)
            
            # Calculate loss
            loss = criterion(outputs, targets)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Update statistics
            train_loss += loss.item() * inputs.size(0)
            
            # Calculate accuracy for classification tasks
            if task == "classification":
                if config.get("num_classes", 0) > 1:  # Multi-class
                    _, predicted = torch.max(outputs, 1)
                    train_correct += (predicted == targets).sum().item()
                else:  # Binary classification
                    predicted = (torch.sigmoid(outputs) > 0.5).float()
                    train_correct += (predicted == targets).sum().item()
                train_total += targets.size(0)
        
        # Calculate average training loss and accuracy
        train_loss = train_loss / len(train_loader.dataset)
        train_acc = train_correct / train_total if train_total > 0 else 0
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                
                # Forward pass
                outputs = model(inputs)
                
                # Adjust targets shape for binary classification if needed
                if task == "classification" and config.get("num_classes", 0) == 1:
                    targets = targets.float().unsqueeze(1)
                
                # Calculate loss
                loss = criterion(outputs, targets)
                
                # Update statistics
                val_loss += loss.item() * inputs.size(0)
                
                # Calculate accuracy for classification tasks
                if task == "classification":
                    if config.get("num_classes", 0) > 1:  # Multi-class
                        _, predicted = torch.max(outputs, 1)
                        val_correct += (predicted == targets).sum().item()
                    else:  # Binary classification
                        predicted = (torch.sigmoid(outputs) > 0.5).float()
                        val_correct += (predicted == targets).sum().item()
                    val_total += targets.size(0)
        
        # Calculate average validation loss and accuracy
        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_correct / val_total if val_total > 0 else 0
        
        # Update learning rate scheduler if defined
        if scheduler:
            if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                scheduler.step(val_loss)
            else:
                scheduler.step()
        
        # Record history
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)
        
        # Model checkpointing
        if model_checkpoint and val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), checkpoint_path)
            
            # Also save the architecture for later loading
            model_dir = os.path.dirname(checkpoint_path)
            model_name = os.path.basename(checkpoint_path).split('.')[0]
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
        
        # Early stopping
        if early_stopping:
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
                
            if patience_counter >= early_stopping_patience:
                print(f"Early stopping at epoch {epoch+1}")
                break
    
    # Load best model if checkpointing was used
    if model_checkpoint:
        model.load_state_dict(torch.load(checkpoint_path))
    
    return {
        "history": history,
        "best_val_loss": best_val_loss,
        "epochs_trained": epoch + 1
    }


def evaluate_model(
    model: Union['tf.keras.Model', 'nn.Module'],
    dataset_path: str,
    config: Dict[str, Any] = None
) -> Dict[str, float]:
    """
    Evaluate a neural network model on a dataset.
    
    Args:
        model: The model to evaluate (TensorFlow or PyTorch)
        dataset_path: Path to the dataset
        config: Evaluation configuration
    
    Returns:
        A dictionary containing evaluation metrics
    
    Raises:
        ModelBackendError: If the required backend is not installed
        ValueError: If the model or dataset format is not supported
    """
    if config is None:
        config = {}
    
    # Determine model type
    if tf_available and isinstance(model, tf.keras.Model):
        return _evaluate_tensorflow_model(model, dataset_path, config)
    elif torch_available and isinstance(model, nn.Module):
        return _evaluate_pytorch_model(model, dataset_path, config)
    else:
        raise ValueError("Unsupported model type")


def _evaluate_tensorflow_model(
    model: 'tf.keras.Model',
    dataset_path: str,
    config: Dict[str, Any]
) -> Dict[str, float]:
    """Evaluate a TensorFlow model."""
    check_tensorflow_available()
    
    # Prepare dataset (reuse from training function)
    _, test_dataset = _prepare_tensorflow_dataset(dataset_path, config)
    
    # Evaluate the model
    results = model.evaluate(test_dataset, verbose=0)
    
    # Extract metrics
    metrics = {}
    if isinstance(results, list):
        for i, metric_name in enumerate(model.metrics_names):
            metrics[metric_name] = float(results[i])
    else:
        # If only loss is returned
        metrics['loss'] = float(results)
    
    return metrics


def _evaluate_pytorch_model(
    model: 'nn.Module',
    dataset_path: str,
    config: Dict[str, Any]
) -> Dict[str, float]:
    """Evaluate a PyTorch model."""
    check_pytorch_available()
    
    # Prepare dataset
    batch_size = config.get("batch_size", 32)
    
    # Get data loader (only need validation/test loader)
    _, test_loader = _prepare_pytorch_dataset(dataset_path, config)
    
    # Configure loss function based on task (classification by default)
    task = config.get("task", "classification")
    if task == "classification":
        if config.get("num_classes", 0) > 1:  # Multi-class
            criterion = nn.CrossEntropyLoss()
        else:  # Binary classification
            criterion = nn.BCEWithLogitsLoss()
    elif task == "regression":
        criterion = nn.MSELoss()
    else:
        raise ValueError(f"Unsupported task: {task}")
    
    # Move model to GPU if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Evaluation mode
    model.eval()
    
    # Initialize metrics
    test_loss = 0.0
    correct = 0
    total = 0
    
    # Evaluation loop
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Forward pass
            outputs = model(inputs)
            
            # Adjust targets shape for binary classification if needed
            if task == "classification" and config.get("num_classes", 0) == 1:
                targets = targets.float().unsqueeze(1)
            
            # Calculate loss
            loss = criterion(outputs, targets)
            test_loss += loss.item() * inputs.size(0)
            
            # Calculate accuracy for classification tasks
            if task == "classification":
                if config.get("num_classes", 0) > 1:  # Multi-class
                    _, predicted = torch.max(outputs, 1)
                    correct += (predicted == targets).sum().item()
                else:  # Binary classification
                    predicted = (torch.sigmoid(outputs) > 0.5).float()
                    correct += (predicted == targets).sum().item()
                total += targets.size(0)
    
    # Calculate final metrics
    metrics = {}
    metrics['loss'] = test_loss / len(test_loader.dataset)
    
    if task == "classification":
        metrics['accuracy'] = correct / total if total > 0 else 0
        
        # Additional metrics for binary classification
        if config.get("num_classes", 0) <= 1 and config.get("detailed_metrics", False):
            # Compute precision, recall, F1 score
            true_positives = 0
            false_positives = 0
            false_negatives = 0
            
            with torch.no_grad():
                for inputs, targets in test_loader:
                    inputs, targets = inputs.to(device), targets.to(device)
                    
                    if task == "classification" and config.get("num_classes", 0) == 1:
                        targets = targets.float().unsqueeze(1)
                    
                    outputs = model(inputs)
                    predicted = (torch.sigmoid(outputs) > 0.5).float()
                    
                    true_positives += ((predicted == 1) & (targets == 1)).sum().item()
                    false_positives += ((predicted == 1) & (targets == 0)).sum().item()
                    false_negatives += ((predicted == 0) & (targets == 1)).sum().item()
            
            # Calculate precision and recall
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            
            # Calculate F1 score
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics['precision'] = precision
            metrics['recall'] = recall
            metrics['f1_score'] = f1
    
    return metrics 