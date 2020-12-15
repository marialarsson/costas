import matplotlib.pyplot as plt

N = []
D = []
for n in range(5,15):
    file = open("datacd20_70/durations_"+str(n)+".txt","r")
    durations = [float(item) for item in file.readlines()]
    file.close()
    N.append(n)
    D.append(sum(durations) / len(durations) )

N2 = []
D2 = []
for n in range(5,15):
    file = open("datar/durations_"+str(n)+".txt","r")
    durations = [float(item) for item in file.readlines()]
    file.close()
    N2.append(n)
    D2.append(sum(durations) / len(durations) )

plt.plot(N2, D2, 'y')
plt.plot(N, D, 'k')
plt.axis([5, max(N2), 0, max([max(D),max(D2)])])
plt.xlabel('Size N of Costas Array')
plt.ylabel('Calculation time (s)')
plt.show()
