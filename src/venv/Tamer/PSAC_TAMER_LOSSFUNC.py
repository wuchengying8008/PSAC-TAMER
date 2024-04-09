import matplotlib.pyplot as plt
import numpy as np
class PSAC_LOSSFUNC():
def calculate_euclidean_distance(point, centroid):
    return np.sum((point - centroid) ** 2)

def calculate_sse(data, centroids, labels):
    sse = 0
    for i in range(len(data)):
        sse += calculate_euclidean_distance(data[i], centroids[labels[i]])
    return sse

#textdata
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
centroids = np.array([[2, 3], [7, 8]])
labels = np.array([0, 0, 1, 1, 1])  

sse = calculate_sse(data, centroids, labels)
print(f"SSE: {sse}")



plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', label='Data Points')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', color='red', s=200, label='Centroids')


plt.title('Data Points and Centroids')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')


plt.legend()

# 显示图形
plt.show()

