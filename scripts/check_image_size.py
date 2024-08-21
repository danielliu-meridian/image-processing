# from ..image_utils import get_images_dimensions

import cv2
def get_images_dimensions(image_path):
  """
  Returns the dimensions of the images

  Parameters:
  image_path (str) : the path to image file

  Returns:
  tuple (width, height, channels) for color image
  Or (width, height, 1) for grayscale image
  """

  image = cv2.imread(image_path)

  if image is None:
    raise ValueError(f"Image not found at {image_path}")
  
  dimensions = image.shape

  if len(dimensions) == 3:
    return dimensions
  else:
    return (dimensions[1], dimensions[0], 1)

def main():
  image_path = "./images/my_own_image.png"

  dimensions = get_images_dimensions(image_path)

  if len(dimensions) == 3:
    print(f"the dimensions of the colar image (width, height, channel) is {dimensions}")
  else:
    print(f"the dimensions of the grayscale image (width, height, 1) is {dimensions}")

if __name__ == "__main__":
  main()