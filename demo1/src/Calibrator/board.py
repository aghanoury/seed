from cv2 import aruco
import cv2

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

board_x = 9
board_y = 7
board = aruco.CharucoBoard_create(board_x, board_y, 1, 0.8, aruco_dict)

px_in = 300
imboard = board.draw((board_x*px_in, board_y*px_in))
cv2.imwrite("board.tiff", imboard)