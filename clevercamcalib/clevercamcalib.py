import numpy as np
import cv2
import glob
import yaml


def calibrate(chessboard_size, square_size, images_topic, destination):
    if chessboard_size is not None:
        chessboard_size = list(map(int, chessboard_size.split("x")))
        if len(chessboard_size) == 2:
            length = chessboard_size[0]
            width = chessboard_size[1]
        else:
            print("Incorrect chessboard_size")
            quit()
    else:
        print("Incorrect chessboard_size")
        quit()
    if square_size is None:
        print("Incorrect square chessboard_size")
        quit()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, square_size, 0.001)
    objp = np.zeros((length * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:length, 0:width].T.reshape(-1, 2)
    objpoints = []
    imgpoints = []
    images = glob.glob(str(images_topic) + '*.jpg')
    if len(images) < 10:
        print("Error: not enough images (10 required), found: ", len(images))
        quit()
    print("Starting calibration...")
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (length, width), None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
    if objpoints == [] or imgpoints == []:
        print("Error: Chessboard not found")
        quit()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savetxt("matrix.txt", (mtx[0][0], mtx[0][2], mtx[1][1], mtx[1][2], mtx[2][2]), fmt='%s')
    np.savetxt("distortion.txt", dist, fmt='%s')
    print("Calibration successful")
    file = open(destination + "\camera_info.yaml", "w")
    file.write(yaml.dump({"ret": ret, "matrix": mtx, "distortion": dist, "rvecs": rvecs, "tvecs": tvecs}))


def undistort(image, camera_info):
    img = cv2.imread(image)
    file = yaml.load(open(camera_info))
    matrix = file['matrix']
    distortions = file['distortion']
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(matrix, distortions, (w, h), 1, (w, h))
    dst = cv2.undistort(img, matrix, distortions, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst

