---


---

<h1 id="калибровка-камеры">Калибровка камеры</h1>
<h1 id="введение">Введение</h1>
<p>Компьютерное зрение получает все более широкое распространение. Зачастую, алгоритмы компьютерного зрения работают неточно, получая искаженное изображение с камеры.<br>
(Картинка)<br>
На данном изображении мы видим, что прямая линия на изображении отображается как кривая. Наш мозг понимает, что эта линия в реальности не скруглена, но компьютер подобными навыками не обладает. Поэтому какой-либо алгоритм компьютерного зрения будет воспринимать информацию с этой картинки неправильно. Для устранения подобных искажений камера, получающая изображения, должна быть откалибрована в соответствии со своими особенностями.</p>
<h1 id="установка-скрипта">Установка скрипта</h1>
<p>Для начала, необходимо установить необходимые библиотеки:</p>
<pre class=" language-python"><code class="prism  language-python">pip install numpy  
pip install opencv<span class="token operator">-</span>python  
pip install glob  
pip install pyyaml  
pip install urllib<span class="token punctuation">.</span>request
</code></pre>
<p>Затем скачиваем скрипт из репозитория:</p>
<pre><code>git clone https://github.com/tinderad/clever_cam_calibration.git
</code></pre>
<p>Переходим в скачанную папку и устанавливаем скрипт:</p>
<pre><code>cd clever_cam_calibration
sudo python setup.py build
sudo python setup.py install
</code></pre>
<p>Если вы используете Windows, тогда скачайте архив из <a href="https://github.com/tinderad/clever_cam_calibration/archive/master.zip">репозитория</a>, распакуйте его и установите:</p>
<pre><code>cd path\to\archive\clever_cam_calibration\
python setup.py build
python setup.py install
</code></pre>
<blockquote>
<p>path\to\archive - путь до распакованного архива</p>
</blockquote>
<h1 id="подготовка-к-калибровке">Подготовка к калибровке</h1>
<p>Вам необходимо подготовить калибровочную мишень. Она представляет собой «шахматную доску». Файл можно взять <a href="https://www.oreilly.com/library/view/learning-opencv-3/9781491937983/assets/lcv3_ac01.png">отсюда</a>.<br>
Наклейте распечатанную мишень на любую твердую поверхность.<br>
(Фото)<br>
Посчитайте количество пересечений в длину и в ширину доски, измерьте размер клетки (в мм).<br>
(Фото)<br>
Включите Клевер и подключитесь к его Wi-fi.</p>
<blockquote>
<p>Перейдите на 192.168.11.1:8080 и проверьте, получает ли компьютер изображения из топика image_raw</p>
</blockquote>
<h1 id="калибровка">Калибровка</h1>
<p>Запустите скрипт <strong><em>calibrate_cam</em></strong>:</p>
<p><strong>Windows:</strong></p>
<pre><code>path\to\python\Scripts\calibrate_cam.exe
</code></pre>
<blockquote>
<p>path\to\python - путь до директории python</p>
</blockquote>
<p><strong>Linux:</strong></p>
<pre class=" language-python"><code class="prism  language-python"><span class="token operator">&gt;</span>calibrate_cam
</code></pre>
<p>Задайте параметры доски:</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token operator">&gt;</span>calibrate_cam
Chessboard width<span class="token punctuation">:</span>  <span class="token comment"># Перекрестий в ширину</span>
Chessboard height<span class="token punctuation">:</span>  <span class="token comment"># Перекрестий в длину</span>
Square size<span class="token punctuation">:</span>  <span class="token comment"># Длина ребра клетки (в мм)</span>
Saving mode <span class="token punctuation">(</span>YES <span class="token operator">-</span> on<span class="token punctuation">)</span><span class="token punctuation">:</span>  <span class="token comment"># Режим сохранения</span>
</code></pre>
<blockquote>
<p>Режим сохранения: если включен, то все полученные фотографии будут сохраняться в нынешней директории.</p>
</blockquote>
<p>Скрипт начнет свою работу:</p>
<pre><code>...
Calibration started!
For help see ...
Commands:
help, catch (key: Enter), delete, restart, stop, finish
</code></pre>
<p>Чтобы откалибровать камеру, вам требуется сделать как минимум 25 фото шахматной доски с различных ракурсов. Чтобы сделать фото, введите команду <strong><em>catch</em></strong>  или нажмите клавишу Enter.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token operator">&gt;</span>catch
</code></pre>
<p>Программа будет информировать вас о состоянии калибровки.</p>
<pre><code>...
Chessboard not found, now 0 (25 required)
&gt;  # Enter
---
Image added, now 1 (25 required)
</code></pre>
<blockquote>
<p>Вместо того, чтобы каждый раз вводить команду <strong><em>catch</em></strong>, Вы можете просто нажимать клавишу <strong><em>Enter</em></strong> (вводить пустую строку)</p>
</blockquote>
<p>После того, как будет набрано достаточное количество изображений, введите команду <strong><em>finish</em></strong>.</p>
<pre><code>...
&gt;finish
Calibration successful!
</code></pre>
<p><strong>Калибровка по существующим изображениям:</strong></p>
<p>Если же у вас уже есть изображения, то вы можете откалибровать камеру по ним при помощи скрипта <strong><em>calibrate_cam_ex</em></strong></p>
<pre><code>&gt;calibrate_cam_ex
</code></pre>
<p>Указываем характеристики мишени, а так же путь до папки с изображениями:</p>
<pre class=" language-python"><code class="prism  language-python">Chessboard width<span class="token punctuation">:</span>  <span class="token comment"># Перекрестий в ширину</span>
Chessboard height<span class="token punctuation">:</span>  <span class="token comment"># Перекрестий в длину</span>
Square size<span class="token punctuation">:</span>  <span class="token comment"># Длина ребра клетки (в мм)</span>
Path<span class="token punctuation">:</span>  <span class="token comment"># Путь до папки с изображениями</span>
</code></pre>
<p>В остальном этот скрипт работает аналогично <strong><em>calibrate_cam</em></strong></p>
<p>Программа обработает все полученные фотографии, и создаст файл <strong><em>camera_info</em><strong><strong><em>.</em></strong></strong><em>yaml</em></strong> в нынешней директории. При помощи этого файла можно будет выравнивать искажения на изображениях, полученных с этой камеры.</p>
<blockquote>
<p>Если вы поменяете разрешение получаемого изображения, вам нужно будет снова калибровать камеру.</p>
</blockquote>
<h1 id="исправление-искажений">Исправление искажений</h1>
<p>За получение исправленного изображения отвечает функция <strong><em>get_undistorted_image(cv2_image, camera_info)</em></strong>:</p>
<ul>
<li><strong><em>cv2_image</em></strong>: Закодированное в массив cv2 изображение</li>
<li><strong><em>camera</em><strong><strong><em>­</em>_</strong></strong><em>info</em></strong>: Путь до файла калибровки</li>
</ul>
<p>Функция возвращает массив cv2, в котором закодировано исправленное изображение</p>
<blockquote>
<p>Если вы используете fisheye-камеру, поставляемую вместе с Клевером, то для обработки изображений разрешением 320x240 или 640x480 вы можете использовать уже существующие параметры калибровки. Для этого в качестве аргумента camera_info  передайте параметры <strong><em>clever_cam_calibration.clevercamcalib.CLEVER_FISHEYE_CAM_320</em></strong> или <strong><em>clever_cam_calibration.clevercamcalib.CLEVER_FISHEYE_CAM_640</em></strong> соответственно.</p>
</blockquote>
<h1 id="пример-использования">Пример использования:</h1>
<p><strong>Обработка потока изображений с камеры</strong>.</p>
<p>Данная программа получает изображения с камеры и выводит их на экран в исправленном виде при существующем файле калибровки.</p>
<pre class=" language-py"><code class="prism  language-py"><span class="token keyword">import</span> clever_cam_calibration<span class="token punctuation">.</span>clevercamcalib <span class="token keyword">as</span> ccc  
<span class="token keyword">import</span> cv2  
  
camera <span class="token operator">=</span> cv2<span class="token punctuation">.</span>VideoCapture<span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span>  
<span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>  
    return_value<span class="token punctuation">,</span> image <span class="token operator">=</span> camera<span class="token punctuation">.</span>read<span class="token punctuation">(</span><span class="token punctuation">)</span>  
    gray <span class="token operator">=</span> cv2<span class="token punctuation">.</span>cvtColor<span class="token punctuation">(</span>image<span class="token punctuation">,</span> cv2<span class="token punctuation">.</span>COLOR_BGR2GRAY<span class="token punctuation">)</span>  
    undistorted_img <span class="token operator">=</span> ccc<span class="token punctuation">.</span>get_undistorted_image<span class="token punctuation">(</span>gray<span class="token punctuation">,</span> <span class="token string">"camera_info.yaml"</span><span class="token punctuation">)</span>  
    cv2<span class="token punctuation">.</span>imshow<span class="token punctuation">(</span><span class="token string">"undistort"</span><span class="token punctuation">,</span> undistorted_img<span class="token punctuation">)</span>  
    cv2<span class="token punctuation">.</span>waitKey<span class="token punctuation">(</span><span class="token number">33</span><span class="token punctuation">)</span>  
cv2<span class="token punctuation">.</span>destroyAllWindows<span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre>
