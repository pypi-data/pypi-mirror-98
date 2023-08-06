import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from data import image_samples

def load_samples():
  image_samples.load()

def read(file_path):
  mpimg.imread(file_path)

def show(img):
  plt.imshow(img)


