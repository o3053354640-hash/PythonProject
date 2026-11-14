import os
import sys

if len(sys.prefix) == 2 and sys.prefix[1] == ":":
    python_root = os.path.dirname(sys.executable)
    if python_root:
        sys.prefix = python_root
        sys.exec_prefix = python_root

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(7)

# 构造数据
N, D_in = 800, 5
true_w = torch.arange(1, D_in + 1, dtype=torch.float32)
true_b = 7.0

X = torch.randn(N, D_in)
noise = torch.randn(N) * 0.6
y = X @ true_w + true_b + noise

# 数据集和 DataLoader
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# 模型固定在 CPU
device = torch.device("cpu")
model = nn.Linear(D_in, 1).to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

# 训练
epochs = 150

for epoch in range(1, epochs + 1):
    epoch_loss = 0.0

    for xb, yb in loader:
        xb = xb.to(device)
        yb = yb.to(device)

        pred = model(xb).squeeze(-1)
        loss = criterion(pred, yb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item() * xb.size(0)

    epoch_loss /= N

    if epoch % 30 == 0 or epoch == 1:
        print(f"Epoch {epoch:3d} | loss {epoch_loss:.4f}")

# 查看结果
learned_w = model.weight.detach().squeeze(0)
learned_b = model.bias.detach()

print("\nTrue w    :", true_w.numpy())
print("Learned w :", learned_w.numpy())
print("True b    :", true_b)
print("Learned b :", learned_b.item())