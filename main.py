import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 100)
y = np.sin(x)

fig = plt.figure(figsize = (90, 5))
plt.plot(x, y)
plt.grid(True) 
plt.show()
