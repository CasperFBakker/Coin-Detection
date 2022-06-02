import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

#=========================================
def moving_r_window(Image, RadiusWindow, minRadius=0, maxRadius=5):
    coin = 1
    timeout = time.time() + 15
    while np.size(coin) != 3:
        coin = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 120, param1=50, param2=30, 
                                        minRadius=minRadius, maxRadius=maxRadius)
        [minRadius, maxRadius] = [minRadius + RadiusWindow, maxRadius + RadiusWindow]
        if time.time() > timeout: # Set timer of 15s, to prevent endless loop
            raise Exception("Cannot distinguish the coin from image."  
                             "Recommended: change kernel size of median blur.") from None
            break

    return coin


#=========================================
def Scale_Image(Image, r_coin, coin_type):
        
    dia_coin_pix = r_coin * 2 
    coin_dia_mm = coin_bank[coin_type]
    size_pixel = coin_dia_mm / dia_coin_pix # pixel size in mm
    [height, width, _] = np.shape(Image)
    height *= size_pixel
    width *= size_pixel

    return height, width, size_pixel


#=========================================
def show_coin(Image, Coin_Position, Coin_Type):
    cv2.circle(Image, (y_coin, x_coin), r_coin, (0, 255, 0), 3) # draw edge of coin
    cv2.circle(Image, (y_coin, x_coin), 2, (255, 255, 255), 3) # draw center of coin

    [height, width, size_pixel] = Scale_Image(Image, r_coin, coin_type) # find scale of image (in mm)

    cv2.putText(Image, f'Heigth {height} mm', (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    cv2.putText(Image, f'Width {width} mm', (550, 1950), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    print( f'Heigth: {height} mm, Width: {width} mm, 1 pixel is {size_pixel} mm')

    plt.imshow(Image)
    plt.show()

    return height, width, size_pixel

def remove_coin(Image):

    # if x_coin =< 0.5*width_image?
    #     -x_coin, else +x_coin
    crop_image = image[x:w, y:h]
    return

#=============== main ====================

if __name__ == '__main__':
    
    Visualize = True
    image = 'image8.jpg'
    ks_blur = 11 # kernel size for medianBlur, it must be odd and greater than 1 (Recommended: 5, 11)
    coin_type = '50_Cent'
    coin_bank = {"2_Euro": 25.75, "1_Euro": 23.25, "50_Cent": 24.25,
                "20_Cent": 22.25, "10_Cent": 19.75, "5_Cent": 21.25}


    img = cv2.imread(image, cv2.IMREAD_COLOR) # Read the image 
    img_og = img.copy() # Make copy of image
    img_og = cv2.cvtColor(img_og, cv2.COLOR_BGR2RGB) # Converting the image to RGB pattern (default = BGR)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Grayscale image
    img = cv2.medianBlur(img, ks_blur) # Blur image 

    find_coin = moving_r_window(img, RadiusWindow=10)   # find the coin in image
    find_coin = np.reshape(find_coin, (1,3))            # remove unused dimension
    pos_coin_rounded = np.uint16(np.around(find_coin))  # rounded position
    [y_coin, x_coin, r_coin]= pos_coin_rounded[0,:] # position of coin and radius of coin (in pixels)

  
    if Visualize == True:
        show_coin(img_og, pos_coin_rounded, coin_type)
    else:
        [height, width, size_pixel] = Scale_Image(img_og, r_coin, coin_type)

