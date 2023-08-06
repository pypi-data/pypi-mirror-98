import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def show(file_path):
  img = mpimg.imread(file_path)
  plt.imshow(img)
  plt.show()


