import random


class Landscape_Generation(object):
# набор методов для генерации статичных динамичных объектов ландшафта
    __size_x = 10
    __size_y = 10
    __water_icon = None
    __forest_icon = None
    __mountain_icon = None
    __fire_icon = None
    __ground_icon = None
    water_density = .01
    forest_density = 30
    
    
    def __init__(self, size_x, size_y, water, tree, mountain, fire, ground) -> None:
        self.__size_x = size_x
        self.__size_y = size_y
        self.__water_icon = water
        self.__forest_icon = tree
        self.__mountain_icon = mountain
        self.__fire_icon = fire
        self.__ground_icon = ground
        
        
    def get_size_x(self) -> int:
        return self.__size_x


    def get_size_y(self) -> int:
        return self.__size_y
    
    
    def get_water_icon(self) -> str:
        return self.__water_icon


    def get_forest_icon(self) -> str:
        return self.__forest_icon


    def get_mountain_icon(self) -> str:
        return self.__mountain_icon


    def get_fire_icon(self) -> str:
        return self.__fire_icon


    def get_ground_icon(self) -> str:
        return self.__ground_icon


    def put_landscape_to(self, any_map):    
        self.__water_generation(any_map)
        self.__water_generation(any_map)
        self.__forest_generation(any_map)
        self.__mountain_generation(any_map)


    def random_cell(self) -> list:
        return [random.randint(1, self.__size_x - 2),
                random.randint(1, self.__size_y - 2)]
        

    def __water_generation(self, map):
        # берем стартовую точку
        start_cell = self.random_cell()
        # добавляем ее на карту
        map.put_object_icon(self.__water_icon, start_cell[0], start_cell[1])
        # основной цикл генерации воды. в range() высчитываем коэфициент заполнения
        for i in range(int((map.get_size_x() * map.get_size_y())/self.water_density)):
            move_list = [[-1,1],[0,1],[1,0],[0,-1]] # список направлений движения
            get_direction = move_list[random.randint(0,3)] # рандомно выбираем движение
            # двигаем начальную позицию по  рандомно заданному направлению
            next_pnt = [start_cell[0] + get_direction[0], start_cell[1] + get_direction[1]]
            # проверяем, не выходит ли итератор за пределы карты
            if next_pnt[0] >= map.get_size_x() or next_pnt[1] >= map.get_size_y():
                break
            if next_pnt[0] < 0 or next_pnt[1] < 0:
                break
            # добавляем текстурку на карту, если ни одно из условий не сработало
            map.put_object_icon(self.__water_icon, next_pnt[0], next_pnt[1])
            # перезаписываем стартовую позицию
            start_cell = next_pnt[:]


    def __forest_generation(self, map):
        presets_list = [[[0,0],[-1,-1],[0,1],[0,-1],[-1,0],[1,0]],
                        [[-1,-1],[0,-1],[-1,0],[0,0],[1,0],[1,1]],
                        [[0,0],[1,0],[-1,0],[-1,1],[-1,2],[-1,4],[-2,1],[-2,2],[-2,3],[-3,2]]]
        
        # геренация новых пресетов и добавление их в список актуальных
        new_presets_list = []
        for preset in presets_list:
            new_preset = []
            for coords in preset:
                new_preset.append([coords[1], coords[0]])
            new_presets_list.append(new_preset)

        for preset in new_presets_list:
            presets_list.append(preset)
            

        count = 0
        while count < int((map.get_size_x() * map.get_size_y())/self.forest_density):
            versions = len(presets_list)
            next_cell = self.random_cell()
            if map.get_matrix()[next_cell[1]][next_cell[0]] != self.__water_icon:
                current_preset = presets_list[count % versions]
                for coord in current_preset:
                    map.put_object_icon(self.__forest_icon, next_cell[0] + coord[0],
                                             next_cell[1] + coord[1])
                count +=1

        
    def __mountain_generation(self, map): # рисуем прямоугольную рамку
        for cell__addr in range(map.get_size_y()):
            map.put_object_icon(self.__mountain_icon, 0 , cell__addr)
            map.put_object_icon(self.__mountain_icon, map.get_size_x()-1, cell__addr)

        for cell__addr in range(map.get_size_x()):
            map.put_object_icon(self.__mountain_icon, cell__addr, 0 )
            map.put_object_icon(self.__mountain_icon, cell__addr, map.get_size_y()-1)
