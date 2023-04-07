import sys

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

dir_path = '../data/img/KR_6277908244/'
temp_path = 'C:\\Users\\bitcamp\\Desktop\\teamzz\\TeamProject\\app\\services\\data\\labels\\'


def img_resize():
    for i in range(0, 108):
        img = Image.open(f'{dir_path}{i}.png')

        img_resize = img.resize((512, 512))
        img_resize.save(f'{dir_path}{i}.png')
    print('resize 완료!')


def red_fillter(num): # num < 108
    img_rgb = cv2.imread(f'{dir_path}{num}.png', 3)
    # print(img_rgb.shape)
    img_rgb = cv2.medianBlur(img_rgb, 3)
    lower_red = np.array([0, 20, 100])
    upper_red = np.array([100, 100, 255])
    dst = cv2.inRange(img_rgb, lower_red, upper_red)
    height, width, _ = img_rgb.shape
    contours_minimap = np.copy(img_rgb)
    contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    # print(hierarchy)
    for c in contours:
        (x, y), r = cv2.minEnclosingCircle(c)  # find circle enclosing the contour\
        center = (int(x), int(y))
        radius = int(r)
        x, y = int(x) - radius, int(y) - radius
        w = radius * 2
        h = radius * 2

        # some checks to make sure the circle size is big enough to be a champion icon
        if r > 20 and r < 30 and x >= 0 and x + w < width and y >= 0 and y + h < height:
            cv2.circle(contours_minimap, center, radius, (0, 255, 0), 2)

            c_x = max(x - 0, 0)
            c_w = min(x + w + 0, width)
            c_y = max(y - 0, 0)
            c_h = min(y + h + 0, height)
            c = dst[c_y:c_h, c_x:c_w]
            print(center)

    cv2.imshow('src', img_rgb)
    cv2.imshow('contours_minimap', contours_minimap)
    cv2.imshow('dst', dst)
    cv2.waitKey()

    cv2.destroyAllWindows()


def blue_fillter(num):  # num < 108
    img_rgb = cv2.imread(f'{dir_path}{num}.png')
    # print(img_rgb.shape)
    img_rgb = cv2.medianBlur(img_rgb, 3)
    lower_blue = np.array([100, 30, 0])
    upper_blue = np.array([255, 150, 60])
    dst = cv2.inRange(img_rgb, lower_blue, upper_blue)
    height, width, _ = img_rgb.shape
    contours_minimap = np.copy(img_rgb)
    contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    # print(hierarchy)
    for c in contours:
        (x, y), r = cv2.minEnclosingCircle(c)  # find circle enclosing the contour\
        center = (int(x), int(y))
        radius = int(r)
        x, y = int(x) - radius, int(y) - radius
        w = radius * 2
        h = radius * 2

        # some checks to make sure the circle size is big enough to be a champion icon
        if r > 20 and r < 30 and x >= 0 and x + w < width and y >= 0 and y + h < height:
            cv2.circle(contours_minimap, center, radius, (0, 255, 0), 2)

            c_x = max(x - 0, 0)
            c_w = min(x + w + 0, width)
            c_y = max(y - 0, 0)
            c_h = min(y + h + 0, height)
            c = dst[c_y:c_h, c_x:c_w]
            print(center)

    cv2.imshow('src', img_rgb)
    cv2.imshow('contours_minimap', contours_minimap)
    cv2.imshow('dst', dst)
    cv2.waitKey()

    cv2.destroyAllWindows()


def match_template(num, template): # num < 108   512 * 512
    # 이미지 경로
    img_path = f'{dir_path}{num}.png'

    # template 경로
    template_path = f'{temp_path}{template}.png'

    # 이미지와 템플릿 불러오기
    img = cv2.imread(img_path)
    template = cv2.imread(template_path)

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 매칭 결과에서 가장 높은 값을 찾음
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 템플릿이 매칭된 위치에 사각형을 그리기
    w, h = template.shape[:-1]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

    # 결과 이미지 출력
    cv2.imshow('result', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def canny(num):  # num < 108
    img_rgb = cv2.imread(f'{dir_path}{num}.png', 3)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    edge1 = cv2.Canny(np.array(img_gray),  50, 300)
    edge2 = cv2.Canny(np.array(img_gray), 150, 500)
    edge3 = cv2.Canny(np.array(img_gray), 200, 600)
    plt.subplot(221), plt.imshow(img_gray, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(222), plt.imshow(edge1, cmap='gray')
    plt.title('Edge Image(50, 300)'), plt.xticks([]), plt.yticks([])
    plt.subplot(223), plt.imshow(edge2, cmap='gray')
    plt.title('Edge Image(150, 500)'), plt.xticks([]), plt.yticks([])
    plt.subplot(224), plt.imshow(edge3, cmap='gray')
    plt.title('Edge Image(200, 600)'), plt.xticks([]), plt.yticks([])

    plt.show()


if __name__ == '__main__':
    # img_resize()
    red_fillter('1') # 1, 70
    blue_fillter('1') # 1, 70
    match_template('15', '파란원')
    canny('5')
    # img_rgb = cv2.imread('../img/KR_6277908244/1.png', 3)
    # print(img_rgb.shape)
    # ward = cv2.imread(r'C:\Users\bitcamp\django-react\DjangoServer\team\labels\빨강와드.png')
    # img_rgb = cv2.medianBlur(img_rgb, 3)
    #
    # # inRange 함수 이용하여 색으로 뽑기 BGR
    # src_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    # lower_blue = np.array([110, 20, 0])
    # upper_blue = np.array([255, 150, 70])
    # lower_red = np.array([0, 20, 100])
    # upper_red = np.array([100, 100, 255])
    # dst1 = cv2.inRange(img_rgb, lower_blue, upper_blue)
    # dst2 = cv2.inRange(img_rgb, lower_red, upper_red)
    # kernel = np.ones((5, 5), np.uint8)
    # height, width, _ = img_rgb.shape
    # contours_minimap = np.copy(img_rgb)
    # contours, hierarchy = cv2.findContours(dst2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    # print(hierarchy)
    # for c in contours:
    #     (x, y), r = cv2.minEnclosingCircle(c)  # find circle enclosing the contour\
    #     center = (int(x), int(y))
    #     radius = int(r)
    #     x, y = int(x) - radius, int(y) - radius
    #     w = radius * 2
    #     h = radius * 2
    #
    #     # some checks to make sure the circle size is big enough to be a champion icon
    #     if r > 20 and r < 30 and x >= 0 and x + w < width and y >= 0 and y + h < height:
    #         cv2.circle(contours_minimap, center, radius, (0, 255, 0), 2)
    #
    #         c_x = max(x - 0, 0)
    #         c_w = min(x + w + 0, width)
    #         c_y = max(y - 0, 0)
    #         c_h = min(y + h + 0, height)
    #         c = dst1[c_y:c_h, c_x:c_w]
    #         print(center)
    #
    #
    # cv2.imshow('src', img_rgb)
    # cv2.imshow('dst1', dst1)
    # cv2.imshow('contours_minimap', contours_minimap)
    # cv2.imshow('dst2', dst2)
    # cv2.waitKey()
    #
    # cv2.destroyAllWindows()

