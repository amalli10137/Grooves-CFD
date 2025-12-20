import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

x1 = np.array([9, 8, 5, 1, 9, 8, 7, 3, 5, 9, 1, 5])
x2 = np.array([43, 98, 73, 48, 51, 5, 71, 92, 37, 42, 63, 20])
y = np.array([0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0])

X = np.column_stack((x1, x2))
model = LogisticRegression(C=1e6, solver='lbfgs', max_iter=1000)
model.fit(X, y)
b0 = model.intercept_[0]
b1, b2 = model.coef_[0]

print("Estimated coefficients (maximum likelihood estimators):")
print(f"b0 = {b0:.6f}")
print(f"b1 = {b1:.6f}")
print(f"b2 = {b2:.6f}")

plt.figure()
mask0 = (y == 0)
plt.scatter(x1[mask0], x2[mask0], marker='o', label='y=0')
mask1 = (y == 1)
plt.scatter(x1[mask1], x2[mask1], marker='^', label='y=1')
x1_vals = np.linspace(0, 10, 100)
x2_vals = -b0 / b2 - (b1 / b2) * x1_vals
plt.plot(x1_vals, x2_vals, label='Line')
plt.xlim(0, 10)
plt.ylim(0, 100)
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()
plt.title('Logistic Regression: Data and seperation line')
plt.show()