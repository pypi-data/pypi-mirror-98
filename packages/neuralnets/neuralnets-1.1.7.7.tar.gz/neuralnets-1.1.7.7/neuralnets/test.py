
import numpy as np
import matplotlib.pyplot as plt

n = 24
a = 1
d = 1e-2

loss = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i < j:
            d = np.abs(i - j)
            loss[i, j] = np.log(n / (i + d))**a * d

loss = loss + loss.T
loss = loss / np.sum(loss)

f = plt.imshow(loss)
plt.colorbar(f)
plt.show()
