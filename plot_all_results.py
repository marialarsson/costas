import matplotlib.pyplot as plt
import math

N5 = [12,13,14,15,16]
N8 = [12,13,14,15,16,17,18,19]

DT = [0.02, 0.09, 0.38, 1.4, 9.1, 78, 438, 720] # table 3. Tree search heuristic C

DLa = [0.20,0.44,1.13,2.7,6.7,5.3,12,17] # table 8. Local search combined with init
DLb = [1.1,2.5,10,72,306] # tabu3

plt.plot(N8, DT, 'darkorange', label='Tree Search heuristic C')
plt.plot(N8, DLa, 'y', linestyle='-.', label='Local Search N-1 based init')
plt.plot(N5, DLb, 'dodgerblue', linestyle='-.', label='Local Search with Tabu 3')

plt.axis([12, 19, 0, 750])
plt.xlabel('Size N of Costas Array')
plt.ylabel('Calculation time (s)')
plt.legend()
plt.show()
