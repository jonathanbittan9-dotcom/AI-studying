import torch

# Creating tensors — several ways
a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])   # from a nested list
b = torch.zeros(2, 3)                         # 2x3 of zeros
c = torch.rand(2, 3)                          # 2x3 random uniform [0,1)

print("a =\n", a)
print("a.shape:", a.shape)     # torch.Size([2, 2])
print("a.dtype:", a.dtype)     # torch.float32

print("\nb (zeros) =\n", b)
print("c (random) =\n", c)

# Tensors behave like NumPy arrays for math
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([10.0, 20.0, 30.0])
print("\nx + y =", x + y)
print("x * y (elementwise) =", x * y)
print("x.sum() =", x.sum())
print("x.mean() =", x.mean())

# Matrix multiplication — this is what neural nets do constantly
m1 = torch.rand(2, 3)
m2 = torch.rand(3, 4)
result = m1 @ m2   # or torch.matmul(m1, m2)
print("\nm1 @ m2 shape:", result.shape)  # (2, 4)

# Reshaping
flat = torch.arange(12)              # [0, 1, ..., 11]
grid = flat.reshape(3, 4)
print("\nflat:", flat)
print("reshaped to 3x4:\n", grid)

# Indexing/slicing works like NumPy
print("\ngrid[0]:", grid[0])         # first row
print("grid[:, 1]:", grid[:, 1])     # second column
