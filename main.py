# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from gui import Ui_form
import sys
import cv2
from webcrawler import *

class mywindow(QtWidgets.QWidget,Ui_form):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    # 定义槽函数
    def showtext(self):
        info = self.textedit1.text()
        array = data.values[0::, 0::]
        self.label1.setText(f'''豆瓣排名第{array[int(info)-1, 1]}名的电影\n\n片名：{array[int(info)-1, 2]}\n\n{array[int(info)-1, 3]}\n\n信息：{array[int(info)-1, 4]}\n\n评分：{array[int(info)-1, 5]}\n\n评价人数：{array[int(info)-1, 6]}\n\n经典评论：{array[int(info)-1, 7]}''')

    def showpicture(self):
        info = self.textedit1.text()
        name = data.values[int(info)-1, 1]
        png = QtGui.QPixmap('douban250/movieposter/'+f'{name}'+'.jpg').scaled(self.label2.width(), self.label2.height())
        self.label2.setPixmap(png)

    def blur(self):
        info = self.textedit1.text()
        name = data.values[int(info)-1, 1]
        img = cv2.imread('douban250/movieposter/' + f'{name}' + '.jpg', cv2.IMREAD_COLOR)
        newImg = cv2.GaussianBlur(img,(7,7),3)
        # cv2.imshow('newImg', newImg)
        # BGR => RGB 文件格式
        shrink = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
        # cv 图片转换成 qt图片
        qt_img = QtGui.QImage(shrink.data,  # 数据源
                              shrink.shape[1],  # 宽度
                              shrink.shape[0],  # 高度
                              shrink.shape[1] * 3,  # 行字节数
                              QtGui.QImage.Format_RGB888)
        # label 控件显示图片
        self.label3.setPixmap(QtGui.QPixmap.fromImage(qt_img).scaled(self.label2.width(), self.label2.height()))

    def gray(self):
        info = self.textedit1.text()
        name = data.values[int(info)-1, 1]
        img = cv2.imread('douban250/movieposter/' + f'{name}' + '.jpg', cv2.IMREAD_GRAYSCALE)
        # BGR => RGB 文件格式
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv 图片转换成 qt图片
        qt_img = QtGui.QImage(shrink.data,  # 数据源
                              shrink.shape[1],  # 宽度
                              shrink.shape[0],  # 高度
                              shrink.shape[1] * 3,  # 行字节数
                              QtGui.QImage.Format_RGB888)
        # label 控件显示图片
        self.label3.setPixmap(QtGui.QPixmap.fromImage(qt_img).scaled(self.label2.width(), self.label2.height()))

    def edge(self):
        info = self.textedit1.text()
        name = data.values[int(info)-1, 1]
        img = cv2.imread('douban250/movieposter/'+f'{name}'+'.jpg', cv2.IMREAD_GRAYSCALE)
        # 33表示二值化的程度，越大阈值越高，必须是奇数，参见CSDN《opencv-python图形图像处理入门基础知识》
        newImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 33, 5)
        # cv2.imshow('newImg', newImg)
        # BGR => RGB 文件格式
        shrink = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
        # cv 图片转换成 qt图片
        qt_img = QtGui.QImage(shrink.data,  # 数据源
                                  shrink.shape[1],  # 宽度
                                  shrink.shape[0],  # 高度
                                  shrink.shape[1] * 3,  # 行字节数
                                  QtGui.QImage.Format_RGB888)
        # label 控件显示图片
        self.label3.setPixmap(QtGui.QPixmap.fromImage(qt_img).scaled(self.label2.width(), self.label2.height()))

data = pd.read_csv('douban250/movie.csv')
app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.show()
sys.exit(app.exec_())