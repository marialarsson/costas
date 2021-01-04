import matplotlib.pyplot as plt
import math

N = []
D = []
for n in range(5,19):
    file = open("data_h_dctr/durations_"+str(n)+".txt","r")
    durations = [float(item) for item in file.readlines()]
    file.close()
    N.append(n)
    D.append(sum(durations) / len(durations) )
N2 = []
D2 = []
for n in range(5,19):
    file = open("data_h_rand/durations_"+str(n)+".txt","r")
    durations = [float(item) for item in file.readlines()]
    file.close()
    N2.append(n)
    D2.append(sum(durations) / len(durations))

plt.plot(N2, D2, 'y')
plt.plot(N, D, 'k')
plt.axis([5, max(N), 0, max([max(D),max(D2)])])
plt.xlabel('Size N of Costas Array')
plt.ylabel('Calculation time (s)')
plt.show()
