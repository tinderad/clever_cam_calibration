<h1 id="введение">Введение</h1>
<p>Компьютерное зрение получает все более широкое распространение. Зачастую, алгоритмы компьютерного зрения работают неточно, получая искаженное изображение с камеры, что особенно характерно для fisheye-камер.<br>
</p><p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/img1.jpg?raw=true" alt="asd"></p>
<blockquote>
<p>Изображение "скруглено" ближе к краям.</p>
</blockquote>
Какой-либо алгоритм компьютерного зрения будет воспринимать информацию с этой картинки неправильно. Для устранения подобных искажений камера, получающая изображения, должна быть откалибрована в соответствии со своими особенностями.
<h1 id="установка-скрипта">Установка скрипта</h1>
<p>Для начала, необходимо установить необходимые библиотеки:</p>
<pre class="  language-python"><code class="prism  language-python">pip install numpy  
pip install opencv<span class="token operator">-</span>python  
pip install glob  
pip install pyyaml  
pip install urllib<span class="token punctuation">.</span>request
</code></pre>
<p>Затем скачиваем скрипт из репозитория:</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token function">git</span> clone https://github.com/tinderad/clever_cam_calibration.git
</code></pre>
<p>Переходим в скачанную папку и устанавливаем скрипт:</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token function">cd</span> clever_cam_calibration
<span class="token function">sudo</span> python setup.py build
<span class="token function">sudo</span> python setup.py <span class="token function">install</span>
</code></pre>
<p>Если вы используете Windows, тогда скачайте архив из <a href="https://github.com/tinderad/clever_cam_calibration/archive/master.zip">репозитория</a>, распакуйте его и установите:</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token function">cd</span> path\to\archive\clever_cam_calibration\
python setup.py build
python setup.py <span class="token function">install</span>
</code></pre>
<blockquote>
<p>path\to\archive - путь до распакованного архива.</p>
</blockquote>
<h1 id="подготовка-к-калибровке">Подготовка к калибровке</h1>
<p>Вам необходимо подготовить калибровочную мишень. Она представляет собой «шахматную доску». Файл можно взять <a href="https://www.oreilly.com/library/view/learning-opencv-3/9781491937983/assets/lcv3_ac01.png">отсюда</a>.<br>
Наклейте распечатанную мишень на любую твердую поверхность.
Посчитайте количество пересечений в длину и в ширину доски, измерьте размер клетки (в мм).
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/chessboard.jpg?raw=true" alt="asd"></p>
Включите Клевер и подключитесь к его Wi-fi.</p>
<blockquote>
<p>Перейдите на 192.168.11.1:8080 и проверьте, получает ли компьютер изображения из топика image_raw.</p>
</blockquote>
<h1 id="калибровка">Калибровка</h1>
<p>Запустите скрипт <strong><em>calibrate_cam</em></strong>:</p>
<p><strong>Windows:</strong></p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token operator">&gt;</span>path\to\python\Scripts\calibrate_cam.exe
</code></pre>
<blockquote>
<p>path\to\python - путь до директории python</p>
</blockquote>
<p><strong>Linux:</strong></p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token operator">&gt;</span>calibrate_cam
</code></pre>
<p>Задайте параметры доски:</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token operator">&gt;</span>calibrate_cam
Chessboard width:  <span class="token comment"># Перекрестий в ширину</span>
Chessboard height:  <span class="token comment"># Перекрестий в длину</span>
Square size:  <span class="token comment"># Длина ребра клетки (в мм)</span>
Saving mode <span class="token punctuation">(</span>YES - on<span class="token punctuation">)</span>:  <span class="token comment"># Режим сохранения</span>
</code></pre>
<blockquote>
<p>Режим сохранения: если включен, то все полученные фотографии будут сохраняться в нынешней директории.</p>
</blockquote>
<p>Скрипт начнет свою работу:</p>
<pre><code>...
Calibration started!
Commands:
help, catch (key: Enter), delete, restart, stop, finish
</code></pre>
<p>Чтобы откалибровать камеру, вам требуется сделать как минимум 25 фото шахматной доски с различных ракурсов.</p>
</p><p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/calibration.jpg?raw=true" alt="asd"></p>
Чтобы сделать фото, введите команду <strong><em>catch</em></strong>.</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token operator">&gt;</span>catch
</code></pre>
<p>Программа будет информировать вас о состоянии калибровки.</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token punctuation">..</span>.
Chessboard not found, now 0 <span class="token punctuation">(</span>25 required<span class="token punctuation">)</span>
<span class="token operator">&gt;</span>  <span class="token comment"># Enter</span>
---
Image added, now 1 <span class="token punctuation">(</span>25 required<span class="token punctuation">)</span>
</code></pre>
<blockquote>
<p>Вместо того, чтобы каждый раз вводить команду <strong><em>catch</em></strong>, Вы можете просто нажимать клавишу <strong><em>Enter</em></strong> (вводить пустую строку).</p>
</blockquote>
<p>После того, как будет набрано достаточное количество изображений, введите команду <strong><em>finish</em></strong>.</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token punctuation">..</span>.
<span class="token operator">&gt;</span>finish
Calibration successful<span class="token operator">!</span>
</code></pre>
<p><strong>Калибровка по существующим изображениям:</strong></p>
<p>Если же у вас уже есть изображения, то вы можете откалибровать камеру по ним при помощи скрипта <strong><em>calibrate_cam_ex</em></strong>.</p>
<pre class="  language-bash"><code class="prism  language-bash"><span class="token operator">&gt;</span>calibrate_cam_ex
</code></pre>
<p>Указываем характеристики мишени, а так же путь до папки с изображениями:</p>
<pre class="  language-bash"><code class="prism  language-bash">Chessboard width:  <span class="token comment"># Перекрестий в ширину</span>
Chessboard height:  <span class="token comment"># Перекрестий в длину</span>
Square size:  <span class="token comment"># Длина ребра клетки (в мм)</span>
Path:  <span class="token comment"># Путь до папки с изображениями</span>
</code></pre>
<p>В остальном этот скрипт работает аналогично <strong><em>calibrate_cam</em></strong>.</p>
<p>Программа обработает все полученные фотографии, и создаст файл <strong><em>camera_info</em><strong><strong><em>.</em></strong></strong><em>yaml</em></strong> в нынешней директории. При помощи этого файла можно будет выравнивать искажения на изображениях, полученных с этой камеры.</p>
<blockquote>
<p>Если вы поменяете разрешение получаемого изображения, вам нужно будет снова калибровать камеру.</p>
</blockquote>
<h1 id="исправление-искажений">Исправление искажений</h1>
<p>За получение исправленного изображения отвечает функция <strong><em>get_undistorted_image(cv2_image, camera_info)</em></strong>:</p>
<ul>
<li><strong><em>cv2_image</em></strong>: Закодированное в массив cv2 изображение.</li>
<li><strong><em>camera</em><strong><strong><em>­</em>_</strong></strong><em>info</em></strong>: Путь до файла калибровки.</li>
</ul>
<p>Функция возвращает массив cv2, в котором закодировано исправленное изображение.</p>
<blockquote>
<p>Если вы используете fisheye-камеру, поставляемую вместе с Клевером, то для обработки изображений разрешением 320x240 или 640x480 вы можете использовать уже существующие параметры калибровки. Для этого в качестве аргумента <strong><em>camera_info</em></strong>  передайте параметры <strong><em>clever_cam_calibration.clevercamcalib.CLEVER_FISHEYE_CAM_320</em></strong> или <strong><em>clever_cam_calibration.clevercamcalib.CLEVER_FISHEYE_CAM_640</em></strong> соответственно.</p>
</blockquote>
<h1 id="примеры-работы">Примеры работы:</h1>
<p>Изначальные изображения:</p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/img1.jpg?raw=true" alt="asd"></p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/img2.jpg?raw=true" alt="asd"></p>
<p>Иcправленные изображения:</p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/calibresult.jpg?raw=true" alt="asd"></p>
<p><img src="https://github.com/tinderad/clever_cam_calibration/blob/master/assets/calibresult1.jpg?raw=true" alt="asd"></p>
<h1 id="пример-использования">Пример использования:</h1>
<p><strong>Обработка потока изображений с камеры</strong>.</p>
<p>Данная программа получает изображения с камеры Клевера и выводит их на экран в исправленном виде, используя существующий калибровочный файл.</p>
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
</code></pre><br>
</p><h1 id="использование-для-aruco">Использование для ArUco</h1>
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


