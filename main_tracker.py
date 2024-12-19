import cv2

capture = cv2.VideoCapture(0)  # берем видеопоток с камеры 0й
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("width %d, height %d"%(width,height))
#tracker = DistTracker()  #создем обьект-tracker  для определения расстояния между обьектами



shadows = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40,detectShadows = True)
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=60,detectShadows = False) #запоминаем фон для вычитания из кадра с пороговым изначением 40
while True:
	ret, main = capture.read() #сохраняем в main очередной кадр видеопотока
	#height, width, _ = main.shape # получаем ширину и высоту кадра

	frame = main#[1280:720, 500:800] #вырезаем из кадра определенную область 340:720, 500:800

	mask = object_detector.apply(frame) # вычитаем из выбранной области фон 
	mask_with_shadows = shadows.apply(frame)
	_, mask = cv2.threshold(mask, 180, 255,cv2.THRESH_BINARY) # получаем ч/б изображение с п.з. 40 ;thresh_tozero/binary/binary_inv/TRUNC;retr_EXTERNAL/LIST/CCOMP(+)/TREE(+)/FLOODFILL
	#_, mask = cv2.threshold(mask, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE,cv2.THRESH_TOZERO)
	detections = [] # создаем пустой массив распознанных обьектов
	
	contours,hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_NONE)
	#print(hierarchy)# hierarchy показывает параметры каждого существующего контура
	#cv2.CONTOURS_MATCH_I2#формула для расчета 
	
	x_cen=0
	y_cen=0
	contours_num=0
	for contour in contours: # перебираем контуры всех обьектов
		area = cv2.contourArea(contour) #сохраняем число точек контура
		if area >900:  # игнорируем обьекты до 700 пикселей включительно
			x, y, w, h, = cv2.boundingRect(contour)# получаем границу движущегося обьекта 
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)#рисует прямоуг в видеопотоке по заданным координатам
			cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),1)#рисует прямоуг в чб видеопотоке
			
			x_cen=x_cen+x+int(w/2)
			y_cen=y_cen+y+int(h/2)
			contours_num=contours_num+1
			whitepixels=cv2.countNonZero(mask)#считаем белые пиксели
			
			detections.append([x, y, w, h]) #добавляем параметры контура в массив
			
	if  contours_num>0 and x_cen>0 and y_cen>0:
		x_cen=x_cen/contours_num
		y_cen=y_cen/contours_num
		cv2.circle(frame,(int(x_cen),int(y_cen)),7,(0,0,255),-1)
		cv2.circle(mask,(int(x_cen),int(y_cen)),6,(255,255,255),-1)
		
	
	
	cv2.imshow("mask_no_shadows",mask)# вывод ч/б видеопотока с  движущимися обьектами в окно mask
	cv2.imshow("frame",frame) #вывод обычного изображения
	#cv2.imshow("shadows",mask_with_shadows)#вывод чб потока с функцией теней
	#print(whitepixels)
	#print(detections)
	
	key = cv2.waitKey(30) 
	if key & 0xFF == ord('q'): # если нажата клавиша 'q'  прерываем бесконечный цикл
		break

cv2.destroyAllWindows()




