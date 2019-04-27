import cv2
import numpy
import pytesseract


# point = [930,410]  # 一
# point = [700,420] # 的
# point = [320,1320] # 中
# point = [580,1320] # 国
point = [330,775] # 在
# point = [580,775] # 不


image_row = cv2.imread('/Users/zhengjiayu/DjangoProject/bishe/tool/static/word.png')

sp = image_row.shape
rows, cols, = image_row.shape[0:2]
# image_resize = cv2.resize(image_row,(int(cols/4),int(rows/4)))
# cv2.imshow("image_resize", image_resize)
row1 = point[1]
col1 = point[0]



print(row1,col1)
# image = image_row[650:900,200:700]
image_cut = image_row[row1-80:row1+80,col1-80:col1+80]
# image_cut = image_resize[row1-20:row1+20,col1-20:col1+90]
cv2.imshow("image_cut", image_cut)
cv2.imwrite("/Users/zhengjiayu/DjangoProject/bishe/tool/static/zai.png",image_cut)
# image_resize_cut = cv2.resize(image_cut,(int(40),int(40)))
# cv2.imshow("image_resize_cut", image_resize_cut)
# print(image)

# image_erode = cv2.erode(image, None, iterations=5)
# cv2.imshow("erode", image_erode)

# img_gray = cv2.cvtColor(image_cut, cv2.COLOR_BGR2GRAY)
#
# _, img_bin = cv2.threshold(img_gray, 180, 255,
#                                cv2.THRESH_OTSU)
# # img_bin = cv2.bitwise_not(img_bin)
# cv2.imshow("img_bin", img_bin)
# print(img_bin)

code = pytesseract.image_to_string(image_cut, lang='chi_sim')
print(code)
# code_row = pytesseract.image_to_string(image_resize, lang='chi_sim')
# print(code_row)
cv2.waitKey(0)