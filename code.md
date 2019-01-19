---


---

<pre><code>import clevercamcalib.clevercamcalib as ccc  
import cv2  
import urllib.request  
import numpy as np  
while True:  
    req = urllib.request.urlopen('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')  
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)  
    image = cv2.imdecode(arr, -1)  
    undistorted_img = ccc.get_undistorted_image(image, ccc.CLEVER_FISHEYE_CAM_640)  
    cv2.imshow("undistort", undistorted_img)  
    cv2.waitKey(33)  
cv2.destroyAllWindows()
</code></pre>

