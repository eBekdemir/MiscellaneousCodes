import matplotlib.pyplot as plt

def get_temps():
	with open('temperatures.csv', 'r', encoding='utf-8') as file:
		temps = file.readlines()
	return temps

csv = get_temps()

dates = []
temps = []

for i in range(1, len(csv)):
	d, t = csv[i].split(',')
	dates.append(d[1:-1])
	temps.append(float(t))

plt.plot(dates, temps, linewidth=0.5)
plt.xticks(('1981-01-01','1983-01-01','1985-01-01','1987-01-01','1989-01-01'), 
		   (1981, 1983, 1985, 1987, 1989))
plt.show()