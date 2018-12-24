import cv2

a = input()
i = 1
camera = cv2.VideoCapture(0)
while a != "finish":
    return_value, image = camera.read()
    cv2.imwrite('photo'+str(i)+'.jpg', image)
    i+=1
    a = input()
del(camera)
