#简化版
# 1. 造数据：y = 3x + 2，再加高斯噪声
import torch
torch.manual_seed(0)

N, D_in = 100, 1          # 样本数、特征维度
true_w, true_b = 3.0, 2.0

X = torch.randn(N, D_in)                       # 形状 (100,1)
noise = torch.randn(N, D_in) * 0.5
y = true_w * X + true_b + noise                # 形状 (100,1)

# 2. 定义可学习参数
w = torch.randn(1, 1, requires_grad=True)      # 形状 (1,1)
b = torch.zeros(1, requires_grad=True)         # 形状 (1)

# 3. 训练超参数
lr = 0.05
n_epochs = 200

# 4. 训练循环
for epoch in range(n_epochs + 1):
    # 前向：线性模型
    y_pred = X @ w + b                         # (100,1)@(1,1)+(1) → (100,1)

    # 损失：MSE
    loss = torch.mean((y_pred - y) ** 2)

    # 反向：清零梯度 → 反向传播 → 参数更新
    loss.backward()
    with torch.no_grad():                      # 手动 SGD
        w -= lr * w.grad
        b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()

    # 打印
    if epoch % 40 == 0:
        print(f'epoch {epoch:3d} | loss {loss.item():.4f} | '
              f'w={w.item():.3f} b={b.item():.3f}')

# 5. 结果对比
print('\nGround truth: w=3.000 b=2.000')
print(f'Learned     : w={w.item():.3f} b={b.item():.3f}')

#完整版
import torch, torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# 1. 构造多元线性数据：y = w^T·x + b + ε，维度 D=5
torch.manual_seed(7)
N, D_in = 800, 5
true_w = torch.arange(1, D_in+1, dtype=torch.float32)  # [1,2,3,4,5]
true_b = torch.tensor(7.0)

X = torch.randn(N, D_in)                    # (800,5)
noise = torch.randn(N) * 0.6
y = X @ true_w + true_b + noise             # (800,)

# 2. 封装成 Dataset / DataLoader
batch_size = 64
dataset = TensorDataset(X, y)
loader  = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 3. 定义模型 = 一个 Linear 层
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = nn.Linear(D_in, 1).to(device)

# 4. 损失与优化器
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

# 5. 训练
epochs = 150
for epoch in range(1, epochs+1):
    epoch_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)

        pred = model(xb).squeeze()          # 前向
        loss = criterion(pred, yb)          # 计算损失

        optimizer.zero_grad()               # 清零梯度
        loss.backward()                     # 反向
        optimizer.step()                    # 更新

        epoch_loss += loss.item() * xb.size(0)
    epoch_loss /= N

    if epoch % 30 == 0 or epoch == 1:
        print(f'Epoch {epoch:3d} | loss {epoch_loss:.4f}')

# 6. 查看学到的参数
learned_w, learned_b = model.weight.data.squeeze().cpu(), model.bias.data.cpu()
print('\nTrue w :', true_w.numpy())
print('Learned w :', learned_w.numpy())
print('True b :', true_b.item())
print('Learned b :', learned_b.item())