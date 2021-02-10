import cv2
import numpy as np

def nothing(x):
    pass
    #print(x)

def make_color_wheel_image(img_width, img_height):
    # source: https://stackoverflow.com/questions/65609247/create-color-wheel-pattern-image-in-python
    """
    Creates a color wheel based image of given width and height
    Args:
        img_width (int):
        img_height (int):

    Returns:
        opencv image (numpy array): color wheel based image
    """
    hue = np.fromfunction(lambda i, j: (np.arctan2(i-img_height/2, img_width/2-j) + np.pi)*(180/np.pi)/2,
                          (img_height, img_width), dtype=np.float)
    saturation = np.ones((img_height, img_width)) * 255
    value = np.ones((img_height, img_width)) * 255
    hsl = np.dstack((hue, saturation, value))
    color_map = cv2.cvtColor(np.array(hsl, dtype=np.uint8), cv2.COLOR_HSV2BGR)
    return color_map

def HSV_trackbar(value_name, trackbar_name, start_val):
    cv2.createTrackbar(f'{value_name} HUE', trackbar_name, min(start_val,180), 180, nothing)
    cv2.createTrackbar(f'{value_name} SAT', trackbar_name, start_val, 255, nothing)
    cv2.createTrackbar(f'{value_name} VAL', trackbar_name, start_val, 255, nothing)

def read_HSV_trackbar(value_name, trackbar_name):
    h = cv2.getTrackbarPos(f'{value_name} HUE', trackbar_name)
    s = cv2.getTrackbarPos(f'{value_name} SAT', trackbar_name)
    v = cv2.getTrackbarPos(f'{value_name} VAL', trackbar_name)
    return np.array([h,s,v])
    


def filter_with_trackbar(img):
    #img = cv2.imread(image_path)
    #img = cv2.resize(img, (960, 540))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_colorwheel = make_color_wheel_image(200, 200)
    img_colorwheel_hsv = cv2.cvtColor(img_colorwheel, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('image')
    cv2.namedWindow('colorwheel')
    HSV_trackbar('LOW1', 'colorwheel', 0)
    HSV_trackbar('HIGH1', 'colorwheel', 255)
    HSV_trackbar('LOW2', 'colorwheel', 255)
    HSV_trackbar('HIGH2', 'colorwheel', 255)
    HSV_trackbar('LOW3', 'colorwheel', 255)
    HSV_trackbar('HIGH3', 'colorwheel', 255)
    switch = '0 : NO SAVE\n 1 : SAVE'
    cv2.createTrackbar(switch, 'colorwheel', 0, 1, nothing)
    
    while(1):
        save = cv2.getTrackbarPos(switch, 'colorwheel')

        lower_hsv_1 = read_HSV_trackbar('LOW1', 'colorwheel')
        higher_hsv_1 = read_HSV_trackbar('HIGH1', 'colorwheel')
        mask1 = cv2.inRange(img_hsv, lower_hsv_1, higher_hsv_1)
        lower_hsv_2 = read_HSV_trackbar('LOW2', 'colorwheel')
        higher_hsv_2 = read_HSV_trackbar('HIGH2', 'colorwheel')
        mask2 = cv2.inRange(img_hsv, lower_hsv_2, higher_hsv_2)
        lower_hsv_3 = read_HSV_trackbar('LOW3', 'colorwheel')
        higher_hsv_3 = read_HSV_trackbar('HIGH3', 'colorwheel')
        mask3 = cv2.inRange(img_hsv, lower_hsv_3, higher_hsv_3)
        mask = mask1 | mask2 | mask3
        bitwise_and = cv2.bitwise_and(img, img, mask=mask)
        mask_cw1 = cv2.inRange(img_colorwheel_hsv, lower_hsv_1, higher_hsv_1)
        mask_cw2 = cv2.inRange(img_colorwheel_hsv, lower_hsv_2, higher_hsv_2)
        mask_cw3 = cv2.inRange(img_colorwheel_hsv, lower_hsv_3, higher_hsv_3)
        mask_cw = mask_cw1 | mask_cw2 | mask_cw3
        img_colorwheel_masked = cv2.bitwise_and(img_colorwheel, img_colorwheel, mask=mask_cw)
        resized = cv2.resize(bitwise_and, (960, 540))
        binary = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        _,binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY)
        binary = cv2.resize(binary, (480, 270))

        cv2.imshow("binary", binary)
        cv2.imshow("image", resized)
        cv2.imshow("colorwheel", img_colorwheel_masked)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            if save:
                blue_img = np.zeros((1080,1920,3), np.uint8)
                red_img = np.zeros((1080,1920,3), np.uint8)
                green_img = np.zeros((1080,1920,3), np.uint8)
                blue_img[:] = (255,0,0)
                green_img[:] = (0,255,0)
                red_img[:] = (0,0,255)
                blue_part = cv2.bitwise_and(blue_img, blue_img, mask=mask1)
                green_part = cv2.bitwise_and(green_img, green_img, mask=mask2)
                red_part = cv2.bitwise_and(red_img, red_img, mask=mask3)
                result = blue_part+green_part+red_part

                cv2.destroyAllWindows()
                return result
            break

        

    cv2.destroyAllWindows()

def main():
    #sample_code()
    rgb = np.random.randint(255, size=(900,800,3),dtype=np.uint8)
    img = filter_with_trackbar(rgb)




if __name__ == '__main__':
    main()
