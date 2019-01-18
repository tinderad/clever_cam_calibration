import numpy as np
import cv2
import glob
import yaml
import urllib.request

CLEVER_FISHEYE_CAM_320 = "fisheye_cam_320.yaml"
CLEVER_FISHEYE_CAM_640 = "fisheye_cam_640.yaml"


def set_camera_info(chessboard_size, square_size, images):
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
    images = glob.glob(str(images) + '*.jpg')
    if len(images) < 25:
        print("Error: not enough images (25 required), found: ", len(images))
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

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None,
                                                       None, None, None, cv2.CALIB_RATIONAL_MODEL)
    matrix = []
    for i in mtx:
        for x in i: matrix.append(x)
    distortion = dist[0]
    data = {"camera_matrix": {"data": matrix}, "distortion_coefficients": {"data": distortion}}
    file = open("camera_info.yaml", "w")
    file.write(yaml.dump(data))
    print("Calibration successful")
    quit()


def get_undistorted_image(cv2_image, camera_info):
    file = yaml.load(open(camera_info))
    mtx = file['camera_matrix']["data"]
    matrix = np.array([[mtx[0], mtx[1], mtx[2]], [mtx[3], mtx[4], mtx[5]], [mtx[6], mtx[7], mtx[8]]])
    print(matrix)
    distortions = np.array(file['distortion_coefficients']["data"])
    print(distortions)
    h, w = cv2_image.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(matrix, distortions, (w, h), 1, (w, h))
    dst = cv2.undistort(cv2_image, matrix, distortions, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst


def calibrate(chessboard_size, square_size, saving_mode=False):
    print("Calibration started!")
    length, width = chessboard_size
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, square_size, 0.001)
    objp = np.zeros((length * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:length].T.reshape(-1, 2)
    objpoints = []
    imgpoints = []
    gray_old = None
    i = 0
    print("For help see ...")
    print("Commands:")
    print("help, catch (key: Enter), delete, restart, stop, finish")
    while True:
        command = input()
        if command == "catch" or command == "":
            print("---")
            req = urllib.request.urlopen('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (width, length), None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                gray_old = gray
                cv2.drawChessboardCorners(gray, (length, width), corners2, ret)
                cv2.imshow("corners", gray)
                imgpoints.append(corners2)
                if saving_mode:
                    cv2.imwrite("photo" + str(i) + ".jpg", gray)
                    i += 1
                print("Image added, now " + str(len(objpoints)))
            else:
                print("Chessboard not found, now " + str(len(objpoints)))
        elif len(command.split()) == 1:
            if command == "help":
                print("Take pictures of a chessboard from different points of view by using command 'catch'.")
                print(
                    "You should take at least 25 pictures to finish calibration (adding more gives you better accuracy).")
                print("Finish calibration by using command 'finish'.")
                print("Corrected coefficients will be stored in present directory as 'camera_info.yaml'")
            elif command == "delete":
                if len(objpoints) > 0:
                    objpoints = objpoints[:-1]
                    imgpoints = imgpoints[:-1]
                    print("Deleted previous")
                else:
                    print("Nothing to delete")
            elif command == "stop":
                print("Stopped")
                break
            elif command == "finish":
                if len(objpoints) >= 25:
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_old.shape[::-1], None,
                                                                       None, None, None, cv2.CALIB_RATIONAL_MODEL)
                    matrix = []
                    for i in mtx:
                        for x in i: matrix.append(x)
                    distortion = dist[0]
                    data = {"camera_matrix": {"data": matrix}, "distortion_coefficients": {"data": distortion}}
                    file = open("camera_info.yaml", "w")
                    file.write(yaml.dump(data))
                    print("Calibration successful")
                    quit()
                else:
                    print("Not enough images, now " + str(len(objpoints)) + " (25 required)")
            elif command == "restart":
                calibrate(chessboard_size, square_size, saving_mode)
                break
        elif len(command.split()) == 2 and command.split()[0] == "help":
            command = command.split()[1]
            if command == "catch":
                print("Takes a picture from camera.")
                print("If there is a chessboard on the picture, the image will be stored")
            elif command == "delete":
                print("Deletes previous stored picture")
            elif command == "restart":
                print("Restarts a calibration script")
            elif command == "stop":
                print("Stops calibration (all data will be deleted)")
            elif command == "finish":
                print("Ends calibration:")
                print(
                    "If there are 25 photos or more, calibration coefficients will be saved in present directory as 'camera_info.yaml' ")
            else:
                print("Unknown command")
        else:
            print("Unknown command")
    cv2.destroyAllWindows()


def calibrate_command():
    ch_width = int(input("Chessboard width: "))
    ch_height = int(input("Chessboard height: "))
    sq_size = int(input("Square size: "))
    s_mod = input("Saving mode (YES - on): ")
    print("---")
    calibrate((ch_width, ch_height), sq_size, s_mod == "YES")


def calibrate_ex_command():
    ch_width = int(input("Chessboard width: "))
    ch_height = int(input("Chessboard height: "))
    sq_size = int(input("Square size: "))
    path = input("path")
    print("---")
    set_camera_info((ch_width, ch_height), sq_size, path)
