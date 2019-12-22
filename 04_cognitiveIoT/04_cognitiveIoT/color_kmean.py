import sys
import csv
import math
from time import sleep
import colorExtraction
import numpy as np
import cv2
import rect
from cv2 import *
from numpy import linalg as LA
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import PIL
# noinspection PyUnresolvedReferences
import subprocess

# noinspection PyUnresolvedReferences
import scipy
# noinspection PyUnresolvedReferences
from matplotlib import image as img
from matplotlib import colors as col
import mysql.connector
from mysql.connector import Error


count = 1
# initialize the camera
try:
    while 1:
        try:
            num = int(input('Input image:'))
            model_name = input('Input model name:')

        except ValueError:
            print("Not a number")
        image = cv2.imread(str(num) + '.jpg')
        #image = cv2.imread('/home/pi/Documents/programs/opencv-face-recognition/9.jpg')
        #model_name = input('Input model name:')
        imgage = (cv2.resize(image, (900, 569)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        orig = image.copy()
        # image = img.imread(image)
        print("shape" + str(image.shape))
        plt.show()
        # cv2.imshow("orig.jpg", orig)
        # print("org img")
        # print("wait key")
        # convert to grayscale and blur to smooth
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # apply Canny Edge Detection
        edged = cv2.Canny(blurred, 0, 50)
        edged = cv2.dilate(edged, None, iterations=1)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        r = []
        g = []
        b = []
        for line in image:
            for pixel in line:
                temp_r, temp_g, temp_b = pixel
                r.append(temp_r)
                g.append(temp_g)
                b.append(temp_b)

        # from mpl_toolkits.mplot3d import Axes3D
        # fig = plt.figure()
        # ax = Axes3D(fig)
        # ax.scatter(r, g, b)
        # plt.show()

        import pandas as pd

        df = pd.DataFrame({'red': r, 'blue': b, 'green': g})

        from scipy.cluster.vq import whiten

        df['scaled_red'] = whiten(df['red'])
        df['scaled_blue'] = whiten(df['blue'])
        df['scaled_green'] = whiten(df['green'])
        df.sample(n=10)

        from scipy.cluster.vq import kmeans

        cluster_centers, distortion = kmeans(df[['scaled_red', 'scaled_green', 'scaled_blue']], 2)
        print("cluster centers" + str(cluster_centers))

        colors = []
        # noinspection PyUnresolvedReferences
        from collections import Counter
        # noinspection PyUnresolvedReferences
        from skimage.color import rgb2lab, deltaE_cie76
        # noinspection PyUnresolvedReferences
        import os

        r_std, g_std, b_std = df[['red', 'green', 'blue']].std()
        for cluster_center in cluster_centers:
            scaled_r, scaled_g, scaled_b = cluster_center
            colors.append((
                scaled_r * r_std / 255,
                scaled_g * g_std / 255,
                scaled_b * b_std / 255
            ))
            # print(colors)

        hex_val = []
        for i in range(len(colors)):
            print("colors==================="+str(colors[i][0]))
            #print(col.to_hex([ colors[i][0], colors[i][1], colors[i][2]]))
            hex_val.append(col.to_hex([colors[i][0], colors[i][1], colors[i][2]]))
        print("-----------------------------"+str(hex_val))

        plt.imshow([colors])
        #plt.show()
        plt.close()
        # get approximate contour
        target = None
        for c in contours:
            p = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * p, True)
            # areaContour2 = cv2.contourArea(c)
            if len(approx) == 4 and cv2.contourArea(c) / (800 * 469) > 0.1:
                # print(str(areaContour2))
                target = approx
                print(cv2.contourArea(c))
                print(800 * 469)
                print(cv2.contourArea(c) / (800 * 469))
                break

        # mapping target point
        # ts to 800x800 quadrilateral3

        # scale A4 is 0.709402 (567.5214x800)
        if target is None:
            print("Object can not be detected")
            blank_image = np.zeros((800, 568, 3), np.uint8)
            #cv2.putText(blank_image, "Object can not be detected", \
                        #(45, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            try:
                while 1:  # Loop will run forever
                    with open('result.csv', 'a') as output:
                        print('Object not detected')
                        writer = csv.writer(output)
                        writer.writerow([count, model_name, 'Object can not be detected'])
                        count = count+1
                        # sleep(3)
                        break
            except ValueError:
                pass
            cv2.imshow("output.jpg", blank_image)
            cv2.waitKey(100)
            cv2.destroyAllWindows()
        else:
            wA4scale = 568
            approx = rect.rectify(target)
            pts2 = np.float32([[0, 0], [wA4scale, 0], [wA4scale, 800], [0, 800]])
            M = cv2.getPerspectiveTransform(approx, pts2)
            dst = cv2.warpPerspective(orig, M, (wA4scale, 800))

            cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
            realDst = dst.copy()
            dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

            tophatKenel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
            tophat = cv2.morphologyEx(dst, cv2.MORPH_TOPHAT, tophatKenel)

            # using thresholding on warped image to get scanned effect
            minThd = math.floor(8 + np.std(tophat))
            _, th_tophat = cv2.threshold(tophat, minThd, 255, cv2.THRESH_BINARY_INV)
            _, thOtsu = cv2.threshold(dst, 0, 255, cv2.THRESH_OTSU)

            ellipseKenel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            th_final = cv2.bitwise_not(th_tophat) + cv2.bitwise_not(thOtsu)
            imagem = cv2.morphologyEx(th_final, cv2.MORPH_OPEN, ellipseKenel)
            imagem = cv2.erode(imagem, None, iterations=1)

            contours, hierarchy = cv2.findContours(imagem, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            check_detect = 0
            idcontour = 0
            for c in contours:
                areaContour = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                areaRect = w * h
                aspectAre = areaRect / (568 * 800)
                if areaContour / areaRect > 0.1 and (
                        x != 0 and y != 0 and (x + w - 1) != 567 and (y + h - 1) != 799) and aspectAre > 0.005 \
                        and hierarchy[0][idcontour][3] == -1:
                    roi = realDst[y:y + h, x:x + w]
                    color_set = colorExtraction.clustering(roi)
                    rect1 = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect1)
                    box = np.int0(box)
                    w = LA.norm(box[0] - box[1])
                    h = LA.norm(box[0] - box[3])
                    realW = w * (21.0 / 568)
                    realH = h * (29.7 / 800)

                    # Color Extaction
                    color_hex = []
                    primary_color=''
                    width=''
                    height=''

                    for k in range(0, len(color_set)):
                        colorTmp = roi.copy()
                        b, g, r = color_set[k]
                        # print('#{:02x}{:02x}{:02x}'.format( int(r), int(g), int(b) ))
                        #print("k value: ",str(k))
                        if str(k) == '0':
                            print("Primary Color: "+str('#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))))
                            primary_color= primary_color + str('#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)))
                        color_hex.append('#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)))

                        # hex_val.append(col.to_hex([ colors[i][0], colors[i][1], colors[i][2]]))

                        cv2.rectangle(realDst, (box[2][0] + (30 * k) - 50, box[2][1] - 55), \
                                      (box[2][0] + 30 + (30 * k) - 50, box[2][1] - 18), \
                                      (int(round(b)), int(round(g)), int(round(r))), -1)
                    #print("color hex==============="+str(color_hex))

                    cv2.drawContours(realDst, [box], 0, (255, 0, 255), 2)
                    cv2.putText(realDst, \
                                str("{0:.2f}".format(round(realW, 2))) + " x " + str(
                                    "{0:.2f}".format(round(realH, 2))) + " cm", \
                                (box[2][0], box[2][1] - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)
                    
                    try:
                        while 1:  # Loop will run forever
                            with open('result.csv', 'a') as output:
                                # print(str(count) + ' ' + str(model_name) + ' ' + (
                                #     "{0:.2f}".format(round(realW, 2))) + " x " + str(
                                #     "{0:.2f}".format(round(realH, 2))) + " cm", )
                                print("width: "+str("{0:.2f}".format(round(realW, 2))))
                                width = width + str("{0:.2f}".format(round(realW, 2)))
                                print("Height: "+str("{0:.2f}".format(round(realH, 2))))
                                height =height + str("{0:.2f}".format(round(realH, 2)))
                                writer = csv.writer(output)
                                writer.writerow([count, model_name, realW, realH, color_hex])
                                #sleep(3)
                                break
                    except ValueError:
                        pass
                    check_detect = 1
                    ################################## Select the master data
                    master_Height=''
                    master_Width=''
                    master_color=''
                    try:
                        connection = mysql.connector.connect(host='43.255.154.94',database='ESI_HEALTHCARE',user='praveen',password='Esiadmin@2019')
                        if connection.is_connected():
                            db_Info = connection.get_server_info()
                            print("Connected to MySQL database... MySQL Server version on ",db_Info)
                            cursor = connection.cursor()
                            cursor.execute("SELECT * FROM ESI_HEALTHCARE.master_QC_Data;")
                            record = cursor.fetchall()
                            print("\nPrinting each laptop record")
                            for row in record:
                                print("ModelName = ", row[1])
                                print("Height = ", row[2])
                                master_Height=master_Height+row[2]
                                print("Width = ", row[3])
                                master_Width=master_Width+row[3]
                                print("Color = ", row[4])
                                master_color=master_color+row[4]
                            print ("Your connected to - ", record)
                    except Error as e :
                        pass
                    finally:
                        #closing database connection.
                        if(connection.is_connected()):
                            cursor.close()
                            connection.close()
                            print("MySQL connection is closed")
                    ################################## Insert the data in database
                    QC_status=''
                    try:
                        connection = mysql.connector.connect(host='43.255.154.94',database='ESI_HEALTHCARE',user='praveen',password='Esiadmin@2019')
                        if connection.is_connected():
                            db_Info = connection.get_server_info()
                            print("Connected to MySQL database... MySQL Server version on ",db_Info)
                            cursor = connection.cursor()
                            print("height: "+str(height))
                            print("width: "+str(width))
                            print("primary_color: "+str(primary_color))
                            if master_Height == height and master_Width == width and master_color == primary_color:
                                print("Product verified")
                                QC_status=QC_status+ 'pass'   
                            print("QC_status: "+str(QC_status))                            
                            cursor.execute("INSERT INTO `ESI_HEALTHCARE`.`qc_Check_Data` (`MODEL_NAME`, `QC_NAME`, `DIMENTION_HEIGHT`, `DIMENTION_WIDTH`, `ORIGINAL_COLOR`, `COLOR_1`, `QC_STATUS`) VALUES ('QC_1002', '', '158.2', '76.5', '#15161e', '#15161e','pass');")
                            record = cursor.fetchall()
                            print ("Your connected to - ", record)
                    except Error as e :
                        pass
                    finally:
                        #closing database connection.
                        if(connection.is_connected()):
                            cursor.close()
                            connection.close()
                            print("MySQL connection is closed")
                idcontour = idcontour + 1
            if check_detect == 0:
                cv2.putText(realDst, "Object can not be detected", \
                            (45, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                try:
                    while 1:  # Loop will run forever
                        with open('result.csv', 'a') as output:
                            print('Object not detected')
                            writer = csv.writer(output)
                            writer.writerow([count, model_name, 'Object can not be detected'])
                            sleep(3)
                            break
                except ValueError:
                    pass

            cv2.imshow("output.jpg", realDst)

            cv2.imwrite("pic_result" + str(count) + ".jpg", realDst)
            count = count + 1
            cv2.waitKey(10000)
            cv2.destroyAllWindows()
except KeyboardInterrupt:
    pass
