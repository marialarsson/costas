import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math

N = [12,13,14,15,16]

D0 = [0.03, 0.09, 0.39, 2.40, 10.3] # table 1. Tree Search baseline
D1 = [0.10, 0.33, 1.50, 4.40, 25.67] # table 2. Tree search heuristic A
D2 = [0.07, 0.53, 1.43, 5.97, 26.8] # table 2. Tree search heuristic B
D3 = [0.02, 0.09, 0.38, 1.40, 9.1]

plt.plot(N, D0, 'r', label='Tree Search (TS) baseline')
plt.plot(N, D1, 'g', label='TS heuristic A')
plt.plot(N, D2, 'b', label='TS heuristic B')
plt.plot(N, D3, 'darkorange', label='TS heuristic C')

DALL = D0+D1+D2+D3

plt.axis([12, 16, 0, max(DALL)])
plt.xlabel('Size N of Costas Array')
plt.ylabel('Calculation time (s)')
plt.legend()
plt.show()
