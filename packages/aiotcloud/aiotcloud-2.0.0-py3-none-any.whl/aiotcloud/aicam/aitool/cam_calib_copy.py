#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：esp_server.py
import cv2
import numpy as np
import threading

import cv2.aruco as aruco
font = cv2.FONT_HERSHEY_SIMPLEX #font

def detect(frame, camera_params,size=0.04):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,
                                                          aruco_dict,
                                                          parameters=parameters)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners,size, camera_params['mtx'], camera_params['dist'])
        # Estimate pose of each marker and return the values rvet and tvec---different
        # from camera coeficcients
        (rvec-tvec).any() # get rid of that nasty numpy value array error

#        aicam.drawAxis(frame, mtx, dist, rvec, tvec, 0.1) #Draw Axis
#        aicam.drawDetectedMarkers(frame, corners) #Draw A square around the markers
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, camera_params['mtx'], camera_params['dist'], rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)


    else:
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("frame",frame)

    key = cv2.waitKey(1)


def calibkd(queue,h,w):
    print("start calibkd")

    # # 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

    # # 获取标定板角点的位置
    objp = np.zeros((h * w, 3), np.float32)
    objp[:, :2] = np.mgrid[0:h, 0:w].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点

    len = 0

    while True:
        img = queue.get()
        while queue.qsize()>0:
            img = queue.get()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        size = gray.shape[::-1]
        ret, corners = cv2.findChessboardCorners(gray, (h, w), None)
        if ret:
            cv2.drawChessboardCorners(img, (h, w), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值

        cv2.imshow('calibkd', img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            print(type(corners2))
            if [corners2]:
                img_points.append(corners2)
            else:
                img_points.append(corners)
            cv2.waitKey(300)
            len += 1
        elif len > 5: 
            break

    # print(len(img_points))
    cv2.destroyAllWindows()

    # # 标定
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    print("ret:", ret)
    print("mtx:\n", mtx) # 内参数矩阵
    print("dist:\n", dist)  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    print("rvecs:\n", rvecs)  # 旋转向量  # 外参数
    print("tvecs:\n", tvecs ) # 平移向量  # 外参数
    cv2.destroyAllWindows()


def calib(queue,h=6,w=9):
    print("start calib")
    t = threading.Thread(target=calibkd, args=(queue,h,w))
    t.start()
