import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import pi, inf




# Iterating through all the coins and drawing a circle on top
# of the original image showing the detected circles
for i in all_circles_rounded[0, :]:
    
    # This first circle is the border of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), i[2], (0, 255, 0), 5)
    # This is the center of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), 2, (255, 0, 0), 3)

    [width, length, size_pixel] = Scale_Image(img_orig, i[2], coin_type)

    cv2.putText(img_orig, f'Width {width} mm', (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    cv2.putText(img_orig, f'Length {length} mm', (550, 1950), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    print( f'Width: {width} mm, Length: {length} mm, 1 pixel is {size_pixel} mm')

# Showing the original image with the drawn circles on it
plt.imshow(img_orig)
plt.show()
