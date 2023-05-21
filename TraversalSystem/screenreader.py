import os
import pytesseract
import cv2
import pyscreenshot as ImageGrab

pytesseract.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"


def text_in_box(x1, y1, x2, y2, skipProcess=False):
    #try:
    #    os.remove("ss.png")
    #    os.remove("ss_processed.png")
    #except FileNotFoundError:
    #    print("File doesn't exist")

    im = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    im.save("ss.png")

    tessImage = cv2.imread("ss.png")
    tessImage = cv2.cvtColor(tessImage, cv2.COLOR_BGR2GRAY)

    if not skipProcess:
        tessImage = cv2.threshold(tessImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        scale_percent = 150  # percent of original size
        width = int(tessImage.shape[1] * scale_percent / 100)
        height = int(tessImage.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        tessImage = cv2.resize(tessImage, dim, interpolation=cv2.INTER_AREA)

    cv2.imwrite("ss_processed.png", tessImage)

    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(tessImage, config=custom_config)


def time_until_jump(width_ratio, height_ratio, left_offs, top_offs):
    x1 = int(1497 * width_ratio + left_offs)
    y1 = int(1007 * height_ratio + top_offs)
    x2 = int(1555 * width_ratio + left_offs)
    y2 = int(1027 * height_ratio + top_offs)

    #print(left_offs, top_offs)
    #print("res:"+str(x2 - x1) + "x" + str(y2 - y1))

    #print("x1:" + str(x1))
    #print("y1:" + str(y1))
    #print("x2:" + str(x2))
    #print("y2:" + str(y2))
    return text_in_box(x1,y1,x2,y2,True)
