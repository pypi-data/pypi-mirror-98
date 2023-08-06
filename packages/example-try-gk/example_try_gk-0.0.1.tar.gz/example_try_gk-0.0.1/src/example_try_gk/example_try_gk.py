from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
#plt.ion()
fig = plt.figure()
ax = fig.gca(projection='3d')
def drawing(x):
    print("hello")
    plt.cla()
    X = np.arange(-5, 5, 0.01)
    Y = np.arange(-5, 5, 0.01)
    X, Y = np.meshgrid(X, Y)
    Z = x * X ** 2 + x * Y ** 2
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.contourf(X, Y, Z, zdir='z', offset=-2)
    # 设置图像z轴的显示范围，x、y轴设置方式相同
    ax.set_zlim(0, 100)
    plt.pause(0.0000000001)
    plt.ioff()
    plt.show()

