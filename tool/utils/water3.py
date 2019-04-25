# import cv2
# import numpy
# from scipy.ndimage import label
# import matplotlib.pyplot as plt
#
# def segment_on_dt(a, img):
#     border = cv2.dilate(img, None, iterations=4)
#     border = border - cv2.erode(border, None)
#     dt = cv2.distanceTransform(img, 2, 3)
#     # 用plt查看图片，可以看出来具体变化
#     plt.figure("距离场图片")
#     plt.imshow(dt,cmap ='gray')
#     plt.show()
#     dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(numpy.uint8)
#     _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)
#     lbl, ncc = label(dt)
#     lbl = lbl * (255 / (ncc + 1))
#     lbl[border == 255] = 255
#     lbl = lbl.astype(numpy.int32)
#     cv2.watershed(a, lbl)
#     lbl[lbl == -1] = 0
#     lbl = lbl.astype(numpy.uint8)
#     return 255 - lbl
#
# # 读进来的图片要求是 白底黑字
# img = cv2.imread("./origin17.jpg")
# # 重置图片大小，在后续的操作中，一些操作的范围是写死的，
# # 改不了了，如果图片大小不一样，操作得到的结果会不理想
# img = cv2.resize(img,(150,150))
# imgo = img.copy()
# imgo = cv2.cvtColor(imgo, cv2.COLOR_BGR2GRAY)
# imgo = cv2.bitwise_not(imgo) # 黑底白字
# cv2.imshow("传进来的图片", imgo)
#
# # 将汉字进行膨胀操作,这个膨胀迭代的次数，再程序中写死了
# # 要求我们拍的照片最终的大小在150*150左右，其中图片中的字，要求占大部分
# img = cv2.erode(img,None,iterations = 7)
#
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _, img_bin = cv2.threshold(img_gray, 0, 255,
#         cv2.THRESH_OTSU)
# img_bin = cv2.bitwise_not(img_bin)
# # 上面这个img_bin是黑底白字，而且是经过膨胀过的
#
# img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN,numpy.ones((3, 3), dtype=int))
#
# # img 3通道的膨胀后的白底黑字   img_bin 单通道的膨胀后的黑底白字
# result = segment_on_dt(img, img_bin)
# # 这个result图片 黑底，其他像素的每一块代表一个字
# # 即有多少种不同于0和255的像素值，就有多少块区域
# cv2.imshow("分水岭后的图片", result)
#
# ############## 把根据传入的点所在的点的像素，把区域截出来 ################
# tmp = result.copy()
#
# pixelset = []
# for i in range(tmp.shape[0]):
#     for ii in range(tmp.shape[1]):
#         if (tmp[i][ii] in pixelset) != True:
#             pixelset.append(tmp[i][ii])
# # 像素0一定在处理结果里面，255不一定
# pixelset.remove(0)
# if 255 in pixelset:
#     pixelset.remove(255)
# # 假设该点所在的像素值等于pixelset[0]
# for i in range(tmp.shape[0]):
#     for ii in range(tmp.shape[1]):
#         if tmp[i][ii]==pixelset[0] or tmp[i][ii]==0:
#             pass
#         else:
#             imgo[i][ii] = 0
#
# rer, imgo = cv2.threshold(imgo, 130, 255, cv2.THRESH_BINARY)
# imgo = cv2.bitwise_not(imgo)
# cv2.imshow("final.jpg", imgo)
# cv2.waitKey(0)
# ##########################################################################
