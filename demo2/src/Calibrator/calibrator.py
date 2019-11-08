from cv2 import aruco
import cv2
import numpy as np
from picamera import PiCamera
import time
from os import listdir, unlink
from os.path import isfile, join

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
folder = 'calib'
width = 800
height = 600

board_x = 9
board_y = 7
board = aruco.CharucoBoard_create(board_x, board_y, 1, 0.8, aruco_dict)

px_in = 300
imboard = board.draw((board_x*px_in, board_y*px_in))

reset = input("Reset files? Type 'yes' to reset. ")

if reset == 'yes':
    cv2.imwrite("board.tiff", imboard)

    #camera.exposure_mode = 'off'

    for f in listdir(folder):
        try:
            os.unlink(join(folder, f))
        except Exception as e:
            print(e)

    camera = PiCamera()
    camera.resolution = (width, height)

    # camera.start_preview()
    for i in range(20):
        input("Capture #{}".format(i+1))
        camera.capture(join(folder, '{}.png'.format(time.time())))
    # camera.stop_preview()

def read_chessboards(images):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners,allIds,imsize

def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    f = 3.6
    sx = 3.76
    sy = 2.74
    print("CAMERA CALIBRATION")

    fx = 254#(f*imsize[0])/(sx*2)
    fy = 181.356#(f*imsize[1])/(sy*2)
    f = max(imsize[0], imsize[1])
    cameraMatrixInit = np.array([[ f,    0., imsize[0]/2.],
                                 [    0., f, imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

files = [join(folder, f) for f in listdir(folder)]

result = calibrate_camera(*read_chessboards(files))
mat = result[1]
dist = result[2]

np.save('mat{}x{}'.format(width, height), mat)
np.save('dist{}x{}'.format(width, height), dist)
