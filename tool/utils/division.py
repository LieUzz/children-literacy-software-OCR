import cv2
import numpy
from scipy.ndimage import label
import pytesseract
from PIL import Image


# 可以打印矩阵，数据不会省略
# numpy.set_printoptions(threshold=numpy.inf)

def segment_on_dt(a, img):
    # 传入的图片是黑底白字
    # dilate 放大黑   erode 放大白
    # border = cv2.dilate(img, None, iterations=4)
    # tmp =  cv2.erode(border, None, iterations=1)
    # 获得的边界 中间一圈像素值为0的
    # border = border - tmp
    border = cv2.dilate(img, None, iterations=4)

    border = border - cv2.erode(border, None)
    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(numpy.uint8)

    # cv2.imshow("binary image", dt)
    _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)

    lbl, ncc = label(dt)
    lbl = lbl * (255 / (ncc + 1))
    # Completing the markers now.
    lbl[border == 255] = 255

    lbl = lbl.astype(numpy.int32)
    cv2.watershed(a, lbl)

    lbl[lbl == -1] = 0
    lbl = lbl.astype(numpy.uint8)
    return 255 - lbl

def cut(image,point_x,point_y):
    y = point_y
    x = point_x
    print(image.shape)
    image_cut = image[y - 100:y + 100, x - 100:x + 100]

    return image_cut



def my_division(img, imgo):
    point = [100,100]
    # 不能这个操作，tesseract识别不了
    # rer, imgo = cv2.threshold(imgo, 200, 255, cv2.THRESH_BINARY)

    # print('my point',point)
    print('in')
    # imgo = cv2.cvtColor(imgo, cv2.COLOR_BGR2GRAY)
    imgo = cv2.bitwise_not(imgo)  # 黑底白字
    # imgo = cv2.bitwise_not(imgo)
    print('imgo_COLOR_BGR2GRAY')
    # cv2.imshow("binary image", imgo)


    # 将汉字进行膨胀操作
    img = cv2.erode(img, None, iterations=15)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_bin = cv2.threshold(img_gray, 0, 255,
                               cv2.THRESH_OTSU)
    img_bin = cv2.bitwise_not(img_bin)

    # cv2.imshow("binary image", img_bin)
    # 上面这个img_bin是黑底白字，而且是经过膨胀过的
    # cv2.imwrite("res0.png", img_bin)
    # 去噪消白点
    # cv2.imshow("res1.png", img_bin)
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN,
                               numpy.ones((3, 3), dtype=int))
    # cv2.imshow("binary image", img_bin)

    result = segment_on_dt(img, img_bin)
    # image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    # image.show()

    # 这个result图片 黑底，其他像素的每一块代表一个字
    # 即有多少种不同于0和255的像素值，就有多少块区域
    # cv2.imshow("res2.png", result)
    # cv2.imwrite("./res2.png", result)

    tmp = result.copy()
    pixelset = []
    for i in range(tmp.shape[0]):
        for ii in range(tmp.shape[1]):
            if (tmp[i][ii] in pixelset) != True:
                pixelset.append(tmp[i][ii])
    # 像素0一定在处理结果里面，255不一定
    pixelset.remove(0)
    print("in point",point)
    if 255 in pixelset:
        pixelset.remove(255)
    print("pixel set: ", pixelset)

    ############## 把根据传入的点所在的点的像素，把区域截出来 ################
    point_pixel = tmp[point[0]][point[1]]
    print("my point position: ",point_pixel)
    if point_pixel not in pixelset:
        print("ERROR! The point not in the right area!")

    # 假设该点所在的像素值等于pixelset[0]
    for i in range(tmp.shape[0]):
        for ii in range(tmp.shape[1]):
            if tmp[i][ii] == point_pixel or tmp[i][ii] == 0:
                pass
            else:
                imgo[i][ii] = 0

    # 用来调整大小
    # imgo = cv2.resize(imgo, (64,64))
    rer, imgo = cv2.threshold(imgo, 130, 255, cv2.THRESH_BINARY)
    imgo = cv2.bitwise_not(imgo)
    image = Image.fromarray(cv2.cvtColor(imgo, cv2.COLOR_BGR2RGB))
    image.show()

    return imgo
    ##########################################################################


if __name__ == '__main__':
    # 白底黑字
    img = cv2.imread("/Users/zhengjiayu/DjangoProject/bishe/tool/utils/origin4.png")
    # imgo[img origin]用来最后做掩模操作，需要原图
    imgo = cv2.imread("/Users/zhengjiayu/DjangoProject/bishe/tool/utils/origin4.png", 0)
    # _, imgo = cv2.threshold(imgo, 190, 255, cv2.THRESH_BINARY)
    # cv2.imshow("binary image", imgo)
    # 假设这个点是point[25,25], 二维数组
    point = [240, 310]
    result = my_division(img, imgo)
    cv2.imshow("binary image", result)
    code = pytesseract.image_to_string(result, lang='chi_sim')
    print(code)
    cv2.waitKey(0)

