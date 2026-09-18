import torch

# requires_grad=True tells PyTorch: "track operations on this tensor,
# I'll want gradients w.r.t. it later"
w = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)

x = torch.tensor(3.0)   # input data — we don't need gradients w.r.t. inputs

# A tiny "model": y = w * x + b
y = w * x + b
print("y =", y.item())   # 2*3 + 1 = 7

# Pretend y should have been 10 — define a loss (squared error)
target = torch.tensor(10.0)
loss = (y - target) ** 2
print("loss =", loss.item())   # (7-10)^2 = 9

# backward() walks the computation graph and computes d(loss)/d(w), d(loss)/d(b)
loss.backward()

print("\nd(loss)/dw =", w.grad.item())   # gradient tells us which way to move w
print("d(loss)/db =", b.grad.item())

# Manually verify: loss = (w*x + b - target)^2
# d(loss)/dw = 2*(w*x+b-target)*x = 2*(7-10)*3 = -18
# d(loss)/db = 2*(w*x+b-target)   = 2*(7-10)   = -6

# --- Gradient descent step ---
# Nudge w and b in the *opposite* direction of the gradient to reduce loss
lr = 0.01  # learning rate: how big a step to take
with torch.no_grad():   # don't track this update itself as part of the graph
    w -= lr * w.grad
    b -= lr * b.grad

print("\nafter one step: w =", w.item(), " b =", b.item())

# Recompute loss with updated w, b to confirm it went down
new_y = w * x + b
new_loss = (new_y - target) ** 2
print("new loss =", new_loss.item(), " (should be < 9)")
