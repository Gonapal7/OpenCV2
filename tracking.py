import math #импортируем библиотеку математических функций

class  DistTracker:
	def __init__(self): #    функция называется конструктор она создает пустой кортеж центральных точек и колво центральных точек 0
		self.center_points = {} #хранит параметры всех объектов, пересекающихся с данным
		self.id_count = 0#хранит число пересечений данного объекта с другими
 

	def update(self,object_rect): #в функцию постоянно передается массив координат всех прямоугольников(распознанных объектов) 
		objects_bbs_ids =[]#создание массива для уникальных объектов которые не пересекаются между собой

		for rect in object_rect: #цикл перебирает все объекты(rect - рассматриваемый объект) 
			x, y, w, h = rectww # лево ,верх, ширина,высота
			cx = (x+(x+w)) // 2#находим центр прямоугольника по координате Х*
			cy = (y+(y+h)) // 2#находим центр прямоугольника по координате У*


			same_object_detected = False# переменная содержит информацию о пересечении объектов
			for id, pt in self.center_points.items():#перебираем все центральные точки прямоугольников по id,pt
				dist =math.hypot(cx - pt[0],cy - pt[1])#вычисляем расстояние между объектами pt[0] это центральная координата прямоугольника по Х  а pt[1]- по У pt=point
 
				if dist < 25:#если расстояние меньше 25 пикселов то
					self.center_points[id] =(cx, cy)# заменяем у объекта с номером [id]  координаты на * 
					print(self.center_points)# выводим на экран кортеж координат и [id] всех объектов
					objects_bbs_ids.append([x, y, w, h, self.id_count]) # добавляем в массив значения(координаты и собственное колво пересечений объектов)объектов которые пересекаются с объектом (rect)  
					self.id_count += 1#увеличиваем колво объектов с которыми пересекается данный объект (rect)


			new_center_points = {}#кортеж новых центральных точек объекта(rect)

			for obj_bb_id in objects_bbs_ids:#для каждого объекта(cross)  пересекающихся с (rect)
				_, _, _, _, object_id = obj_bb_id#игнорируем x, y, w, h и в новую переменную object_id записываем колво пересечений объекта (cross) с другими
			center = self.center_points[object_id]#в новую переходную переменную center записываем 
			new_center_points[object_id] = center

			self.center_points = new_center_points.copy()#сохраняем число объектов, в переменную center_points объекта (rect)
			return objects_bbs_ids#возвращаем все объекты, пересекающиеся с (rect)

