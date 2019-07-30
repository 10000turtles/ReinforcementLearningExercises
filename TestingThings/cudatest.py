import numpy as np
import time
from numba import cuda
import math


@cuda.jit
def my_kernel(ar):
  # Thread id in a 1D block
  pos = cuda.grid(2)
  if pos[0] < ar.shape[0] and pos[1] < ar.shape[1]:  # Check array boundaries
    for i in range(ar.shape[1]):
      ar[pos[0]][i] += 1


N = 10000

ar = np.array([[1.0 for i in range(N)]for j in range(N)])
threadsperblock = 256
blockspergrid = math.ceil(ar.shape[0] / threadsperblock)
start = time.time()
my_kernel[blockspergrid, threadsperblock](ar)
end1 = time.time() - start
print(ar)

ar = np.array([[1.0 for i in range(N)]for j in range(N)])
start = time.time()
ar += 1
end2 = time.time() - start
print(ar)

print("VectorAddFast took % s seconds" % end1)
print("VectorAddSlow took % s seconds" % end2)
# N = 1100
# A = [[1 for j in range(N)] for i in range(N)]
# B = [[1 for j in range(N)] for i in range(N)]
# C = [[0 for j in range(N)] for i in range(N)]

# start = time.time()
# C = fast_matmul(A, B, C)
# vector_add_time_fast = time.time() - start

# start = time.time()
# D = np.matmul(A, B)
# vector_add_time_slow = time.time() - start

# print("C[:5] = " + str(C[: 5]))
# print("C[-5:] = " + str(C[-5:]))
# print("D[:5] = " + str(D[: 5]))
# print("D[-5:] = " + str(D[-5:]))
# print("VectorAddFast took % sseconds" % vector_add_time_fast)
# print("VectorAddSlow took % sseconds" % vector_add_time_slow)
