import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import pi, inf

def moving_r_window(Image, RadiusWindow):
    all_circles = 1
    minRadius_i = 0 
    maxRadius_i = 5
    
    while np.size(all_circles) != 3:
        all_circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 120, param1=50, param2=30, 
                                        minRadius=minRadius_i, maxRadius=maxRadius_i)
        minRadius_i += RadiusWindow
        maxRadius_i += RadiusWindow

    return all_circles

def Window_Calc(Image, r_coin, coin_type):
    
    if coin_type == '2e':
        coin_dia_mm = 25.75
    elif coin_type == '1e':
        coin_dia_mm = 23.25    
    elif coin_type == '50c':
        coin_dia_mm = 24.25
    elif coin_type == '20c':
        coin_dia_mm = 22.25
    elif coin_type == '10c':
        coin_dia_mm = 19.75
    elif coin_type == '5c':
        coin_dia_mm = 21.25    
    else:
        print('Error')
    
    dia_coin_pix = r_coin * 2
    size_pixel = coin_dia_mm / dia_coin_pix # pixel size in mm
    [Width, Length, _] = np.shape(Image)
    Width *= size_pixel
    Length *= size_pixel

    return Width, Length




img = cv2.imread('image8.jpg', cv2.IMREAD_COLOR) # Read the image 
img_orig = img.copy() # Copy the original image so we can show the detected circles later
img_orig = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB) # # Converting the image to RGB pattern (default = BRG)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
plt.rcParams['figure.figsize'] = (16, 9) # Setting the size of the plot image to 16x9 proportion

img = cv2.medianBlur(img, 11) # blur image 

all_circles = moving_r_window(img, 10)

all_circles_rounded = np.uint16(np.around(all_circles)) # Evenly round the numbers received from HoughCircles and converts them to 16 bits unsigned integer type

coins_info = list()
count = 1
# Iterating through all the coins and drawing a circle on top
# of the original image showing the detected circles
for i in all_circles_rounded[0, :]:
    # This first circle is the border of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), i[2], (0, 255, 0), 5)
    # This is the center of the detected circle
    cv2.circle(img_orig, (i[0], i[1]), 2, (255, 0, 0), 3)
    [width, length] = Window_Calc(img_orig, i[2], '50c')
    cv2.putText(img_orig, f'Width {width} mm', (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    cv2.putText(img_orig, f'Length {length} mm', (550, 1950), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    print(width, length)

# Showing the original image with the drawn circles on it

plt.imshow(img_orig)
plt.show()


