---


---

<h1 id="использование-для-aruco">Использование для ArUco</h1>
<p>Чтобы применить параметры калибровки к системе ArUco-навигации, требуется перенести калибровочный .yaml файл на Raspberry Pi Клевера и инициализировать его.</p>
<blockquote>
<p>Не забудьте подключиться к WiFI Клевера</p>
</blockquote>
<p>Для передачи файла используется протокол SFTP. В данном примере используется программа WinSCP.</p>
<p>Подключимся к Raspberry Pi по SFTP.</p>
<blockquote>
<p>Пароль: <em><strong>raspberry</strong></em></p>
</blockquote>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/wcp1.png?raw=true" alt="enter image description here"></p>
<p>Нажимаем “Войти”. Переходим в <em><strong>/home/pi/catkin_ws/src/clever/clever/camera_info/</strong></em> и копируем туда калибровочный .yaml файл.</p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/wcp2.jpg?raw=true" alt="enter image description here"></p>
<p>Теперь мы должны выбрать этот файл в конфигурации ArUco. Для этого используется связь по протоколу SSH. В данном примере используется программа PuTTY.</p>
<p>Подключимся к Raspberry Pi по SSH.</p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/pty1.jpg?raw=true" alt="enter image description here"></p>
<p>Войдем под логином <em><strong>pi</strong></em> и паролем <em><strong>raspberry</strong></em>, перейдем в директорию <em><strong>/home/pi/catkin_ws/src/clever/clever/launch</strong></em> и начнем редактировать конфигурацию <em><strong>main_camera.launch</strong></em></p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/pty2.jpg?raw=true" alt="enter image description here"></p>
<p>В строке <em><strong>camera node</strong></em> заменим параметр <em><strong>camera_info</strong></em> на <em><strong>camera_info.yaml</strong></em></p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/pty3.jpg?raw=true" alt="enter image description here"></p>
<blockquote>
<p>Не забудьте изменить разрешение камеры.</p>
</blockquote>

