import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def show(file_path, grid=False):
  img = mpimg.imread(file_path)

  plt.grid(True)
  plt.imshow(grid)
  plt.show()


