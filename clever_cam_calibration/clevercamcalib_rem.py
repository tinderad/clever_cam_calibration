import numpy as np
import cv2
import glob
import yaml
import urllib.request

def set_camera_info(chessboard_size, square_size, images_topic, destination):
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


def get_undistorted_image(image, camera_info):
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


def calibrate(chessboard_size, square_size):
    camera = cv2.VideoCapture(0)
    print("Calibration started!")
    if chessboard_size is not None:
        size = list(map(int, chessboard_size.split("x")))
        if len(size) == 2:
            length = size[0]
            width = size[1]
        else:
            print("Incorrect chessboard_size")
            quit()
    else:
        print("Incorrect chessboard_size")
        quit()
    if square_size is None:
        print("Incorrect square_size")
        quit()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, square_size, 0.001)
    objp = np.zeros((length * width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:length, 0:width].T.reshape(-1, 2)
    objpoints = []
    imgpoints = []
    gray_old = None
    print("For help see ...")
    print("Commands:")
    print("help, catch (key: Enter), delete, restart, stop, finish")
    while True:
        command = raw_input()
        if command == "catch" or command == "":
            print("---")
            #image = camera.read()
            req = urllib.request.urlopen('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (length, width), None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
                gray_old = gray
                print("Image added, now " + str(len(objpoints)))
            else:
                print("Chessboard not found, now " + str(len(objpoints)))
        elif len(command.split()) == 1:
            if command == "help":
                print("Take pictures of a chessboard from different racourses by using command 'catch'.")
                print("You should take at least 10 pictures to finish calibration (having more gives you better accuracy).")
                print("Finish calibration by using command 'finish'.")
                print("Corrected coefficients will be stored in present directory as 'camera_info.yaml'")
            elif command == "delete":
                if len(objpoints)>0:
                    objpoints = objpoints[:-1]
                    imgpoints = imgpoints[:-1]
                    print("Deleted previous")
                else: print("Nothing to delete")
            elif command == "stop":
                print("Stopped")
                break
            elif command == "finish":
                if len(objpoints) >= 10:
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_old.shape[::-1], None,
                                                                       None)
                    file = open("\camera_info.yaml", "w")
                    file.write(
                        yaml.dump({"ret": ret, "matrix": mtx, "distortion": dist, "rvecs": rvecs, "tvecs": tvecs}))
                    print("Calibration successful")
                    quit()
                else:
                    print("Not enough images, now "+str(len(objpoints))+" (10 required)")
            elif command == "restart":
                print("chessboard size: "+str(chessboard_size)+" "+"square size: "+str(square_size))
                camera.release()
                calibrate(chessboard_size, square_size)
                break
        elif len(command.split()) == 2 and command.split()[0] == "help":
            command = command.split()[1]
            if command == "catch":
                print("Takes a picture from camera.")
                print("If there is a chessboard on the picture, the image will be stored")
            elif command == "delete":
                print("Deletes previous stored picture")
            elif command == "restart":
                print("Restarts a calibration script with new arguments")
                print("args: new_size new_square_size")
                print("Without these arguments script will be restarted with present arguments")
            elif command == "stop":
                print("Stops calibration (all data will be deleted)")
            elif command == "finish":
                print("Ends calibration:")
                print("If there are 10 photos or more, calibration coefficients will be saved in present directory as 'camera_info.yaml' ")
            else:
                print("unknown command")
        elif command.split()[0] == "restart":
            command = command.split()
            new_size = chessboard_size
            new_sq_size = square_size
            if len(command) == 2:
                new_size = command[1]
            elif len(command) == 3:
                new_size == command[1]
                new_sq_size == command[2]
            elif len(command) != 1:
                print("incorrect arguments for 'restart' command")
            camera.release()
            calibrate(new_size, new_sq_size)
            break
        else:
            print("Unknown command")
    camera.release()