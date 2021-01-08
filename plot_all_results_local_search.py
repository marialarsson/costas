import matplotlib.pyplot as plt
import math

N5 = [12,13,14,15,16]
N4 = [12,13,14,15]

D4 = [0.67, 3.5, 19, 84, 198] # table 4. Local search baseline
D5 = [1.06, 6.72, 28.51, 312.82] # table 5. Local search restart A
D6 = [1.17, 3.39, 14.31, 81.85] # table 5. Local search restart B
D7 = [1.1, 2.5, 10, 72] # table 6. Local search swap 3
D8 = [0.68, 3.25, 11.77, 98.27] # table 6. Local search swap N/3
D9 = [0.20, 0.44, 1.13, 2.7, 6.7] # table 7. Local search initialization
D10 =[0.32, 0.77, 1.9,  3.7, 7.3] # table 8. TI


plt.plot(N5, D4, 'r', linestyle='-.', label='Local Search (LS) baseline')
plt.plot(N4, D5, 'forestgreen', linestyle='-.', label='LS restart policy A')
plt.plot(N4, D6, 'lime', linestyle='-.', label='LS restart policy B')
plt.plot(N4, D7, 'dodgerblue', linestyle='-.', label='LS Tabu list 3')
plt.plot(N4, D8, 'navy', linestyle='-.', label='LS Tabu list N/3')
plt.plot(N5, D9, 'y', linestyle='-.', label='LS N-1 based initiation')
plt.plot(N5, D10, 'magenta', linestyle='-.', label='LS Combo Tabu and N-1 init')

DALL = D4+D5+D6+D7+D8+D9+D10

plt.axis([12, 16, 0, 60])
plt.xlabel('Size N of Costas Array')
plt.ylabel('Calculation time (s)')
plt.legend()
plt.show()
