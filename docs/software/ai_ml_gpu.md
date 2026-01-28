# Training AI/ML Models on GPUs

This guide covers training artificial intelligence and machine learning models on NMTHPC's {{nmthpc_gpu_type}} GPU nodes.

## GPU Hardware

NMTHPC features:

- **{{nmthpc_total_gpu_nodes}}** GPU nodes with **{{nmthpc_gpu_type}}** GPUs
- High-bandwidth GPU memory
- Optimized for deep learning and AI workloads
- Support for mixed precision training (FP16, BF16, TF32)

## Setting Up Your Environment

### PyTorch Environment

**Create PyTorch environment**:
```bash
$ module load anaconda3
$ conda create -n pytorch python=3.11
$ conda activate pytorch
$ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

**Verify GPU support**:
```bash
$ python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
$ python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

### TensorFlow Environment

**Create TensorFlow environment**:
```bash
$ conda create -n tensorflow python=3.11
$ conda activate tensorflow
$ pip install tensorflow[and-cuda]
```

**Verify**:
```bash
$ python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## Basic GPU Training

### PyTorch GPU Training

**Simple training script** (`train_pytorch.py`):
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Check GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Simple model
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# Create model and move to GPU
model = SimpleNet().to(device)

# Training setup
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
model.train()
for epoch in range(10):
    for batch_data, batch_labels in train_loader:
        # Move data to GPU
        data = batch_data.to(device)
        labels = batch_labels.to(device)

        # Forward pass
        outputs = model(data)
        loss = criterion(outputs, labels)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), 'model.pth')
```

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --job-name=pytorch_train
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=12:00:00
#SBATCH --output=train_%j.out

module load anaconda3
conda activate pytorch

python train_pytorch.py
```

### TensorFlow GPU Training

```python
import tensorflow as tf

# Check GPU
print("GPUs available:", tf.config.list_physical_devices('GPU'))

# Load data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255
x_test = x_test.reshape(-1, 784).astype('float32') / 255

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    x_train, y_train,
    batch_size=128,
    epochs=10,
    validation_split=0.1,
    verbose=1
)

# Save
model.save('model.keras')
```

## Advanced Techniques

### Mixed Precision Training

**PyTorch Automatic Mixed Precision**:
```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters())
scaler = GradScaler()

for epoch in range(epochs):
    for data, target in dataloader:
        data, target = data.cuda(), target.cuda()

        optimizer.zero_grad()

        # Automatic mixed precision
        with autocast():
            output = model(data)
            loss = criterion(output, target)

        # Scaled backward pass
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
```

**Benefits on H100**:
- 2-3x faster training
- Reduced memory usage
- Minimal accuracy loss

### Multi-GPU Training

**PyTorch DataParallel**:
```python
import torch
import torch.nn as nn

model = MyModel()

# Use all available GPUs
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)

model = model.cuda()

# Training loop remains the same
for data, target in dataloader:
    data, target = data.cuda(), target.cuda()
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

**SLURM script for multi-GPU**:
```bash
#!/bin/bash
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00

module load anaconda3
conda activate pytorch

python train_multi_gpu.py
```

### PyTorch DistributedDataParallel

**For better multi-GPU performance**:
```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_ddp():
    dist.init_process_group("nccl")
    rank = dist.get_rank()
    torch.cuda.set_device(rank)
    return rank

def main():
    rank = setup_ddp()

    model = MyModel().to(rank)
    model = DDP(model, device_ids=[rank])

    # Training loop
    for data, target in dataloader:
        data, target = data.to(rank), target.to(rank)
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    dist.destroy_process_group()

if __name__ == '__main__':
    main()
```

## Optimizing GPU Training

### Data Loading

**Efficient DataLoader**:
```python
from torch.utils.data import DataLoader

dataloader = DataLoader(
    dataset,
    batch_size=64,
    num_workers=8,  # Match --cpus-per-task
    pin_memory=True,  # Faster GPU transfer
    prefetch_factor=2,  # Prefetch batches
    persistent_workers=True  # Keep workers alive
)
```

### Batch Size Tuning

**Find optimal batch size**:
```python
def find_max_batch_size(model, input_shape):
    batch_size = 1
    while True:
        try:
            # Try doubling batch size
            batch_size *= 2
            dummy_input = torch.randn(batch_size, *input_shape).cuda()
            output = model(dummy_input)
            loss = output.sum()
            loss.backward()
            torch.cuda.empty_cache()
        except RuntimeError:  # OOM
            batch_size //= 2
            break
    return batch_size
```

### Memory Management

**Clear GPU cache**:
```python
import torch

torch.cuda.empty_cache()
```

**Monitor GPU memory**:
```python
print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"Reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
```

**Gradient checkpointing** (trade compute for memory):
```python
from torch.utils.checkpoint import checkpoint

def forward_with_checkpoint(self, x):
    return checkpoint(self.layer, x)
```

## Common Deep Learning Tasks

### Image Classification (ResNet)

```python
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# Load pre-trained model
model = models.resnet50(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model = model.cuda()

# Data loading
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_dataset = ImageFolder('train/', transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, num_workers=8)

# Training
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
criterion = torch.nn.CrossEntropyLoss()

for epoch in range(epochs):
    for images, labels in train_loader:
        images, labels = images.cuda(), labels.cuda()
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### Natural Language Processing (Transformers)

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    fp16=True,  # Mixed precision
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

## Monitoring and Debugging

### TensorBoard Integration

**PyTorch with TensorBoard**:
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

for epoch in range(epochs):
    # Training
    for i, (data, target) in enumerate(dataloader):
        # ... training code ...

        # Log metrics
        writer.add_scalar('Loss/train', loss.item(), epoch * len(dataloader) + i)
        writer.add_scalar('Accuracy/train', accuracy, epoch * len(dataloader) + i)

    # Log model graph (once)
    if epoch == 0:
        writer.add_graph(model, data)

writer.close()
```

**View TensorBoard** (requires SSH tunnel):
```bash
$ tensorboard --logdir=runs
```

### Profiling GPU Code

```python
from torch.profiler import profile, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True
) as prof:
    model(inputs)

print(prof.key_averages().table(sort_by="cuda_time_total"))
```

## Complete Training Example

**train_complete.py**:
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.cuda.amp import autocast, GradScaler
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train(model, train_loader, val_loader, epochs=10):
    device = torch.device('cuda')
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    scaler = GradScaler()

    best_val_acc = 0

    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()

            with autocast():
                output = model(data)
                loss = criterion(output, target)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            train_loss += loss.item()

        # Validation
        model.eval()
        correct = 0
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                pred = output.argmax(dim=1)
                correct += pred.eq(target).sum().item()

        val_acc = correct / len(val_loader.dataset)

        logger.info(f"Epoch {epoch+1}: Loss={train_loss/len(train_loader):.4f}, Val Acc={val_acc:.4f}")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')

if __name__ == '__main__':
    # Your model, data loaders
    model = YourModel()
    train_loader = DataLoader(...)
    val_loader = DataLoader(...)

    train(model, train_loader, val_loader, epochs=50)
```

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --job-name=dl_training
#SBATCH --output=train_%j.out
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=you@nmt.edu

set -e

echo "Job started at $(date)"
nvidia-smi

module load anaconda3
conda activate pytorch

python train_complete.py

echo "Job completed at $(date)"
```

## Best Practices

1. **Start small**: Test with small dataset/model first
2. **Monitor GPU usage**: Use `nvidia-smi` during training
3. **Use mixed precision**: 2-3x speedup on H100
4. **Optimize data loading**: Match num_workers to CPUs
5. **Save checkpoints**: Regularly save model state
6. **Log metrics**: Track training progress
7. **Validate regularly**: Catch overfitting early

## Additional Resources

- [Running Jobs on GPU Nodes](../using_nmthpc/gpu_jobs.md)
- [Anaconda](anaconda.md)
- [Python and Jupyter Notebooks](python_jupyter.md)

## Questions?

For GPU training questions, contact <hpc-support@nmt.edu>.
