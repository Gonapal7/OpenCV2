import cv2
capture = cv2.VideoCapture(0)  # берем видеопоток с камеры 0й
while True:
	ret, main = capture.read() #сохраняем в main очередной кадр видеопотока
	
	x = 100
	y = 200
	w = 50
	h = 50
	
	cv2.rectangle(main,(x,y),(x+w,y+h),(0,0,255),2)#рисует прямоуг в потоке по заданным координатам
	
	cv2.imshow("main",main) #вывод обычного и
	
	key = cv2.waitKey(30) 
	if key & 0xFF == ord('q'): # если нажата клавиша 'q'  прерываем бесконечный цикл
		break

cv2.destroyAllWindows()

