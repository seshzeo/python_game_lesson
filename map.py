import copy, random
from game_object import Game_Object
from my_console import Output_menu

# random.seed(1)
# генерацию можно вынести отдельно

class Map(object):

    __size_x = 10
    __size_y = 10
    __console_size = 10
    __map_matrix = []
    __cash_map_matrix = []
    __console_matrix = []
    __cash_console_matrix = []
    __ground_icon = '🟩'
    __water_icon = '🟦'
    __forest_icon = '🌲'
    __mountain_icon = '🟫'
    __fire_icon = '🔥'


    def __init__(self,
                 generator
                ) -> None:
        self.generator = generator
        self.__size_x = generator.get_size_x()
        self.__size_y = generator.get_size_y()
        self.__ground_icon = generator.get_ground_icon()
        self.__water_icon = generator.get_water_icon()
        self.__forest_icon = generator.get_forest_icon()
        self.__mountain_icon = generator.get_mountain_icon()
        self.__fire_icon = generator.get_fire_icon()
        self.__map_matrix = [[self.__ground_icon for x in range(self.__size_x)] for y in range(self.__size_y)]
        self.__console_matrix = [[self.__mountain_icon for x in range(self.__size_x)] for y in range(self.__console_size)]
        generator.put_landscape_to(self)
        self.__console_generation()
        self.__cash_map_matrix = copy.deepcopy(self.__map_matrix)
        self.__cash_console_matrix = copy.deepcopy(self.__console_matrix)
        

    def get_matrix(self) -> list:
        return self.__map_matrix + self.__console_matrix
    

    '''
    # def get_matrix(self) -> list:
        # res = []
        # for i in self.__map_matrix:
            # res.append(str(''.join(i)))
        # res.append(' ')
        # return res


    # def add_line(self, any_matrix):
    #     for str in any_matrix:
    #         self.__map_matrix.append(str)


    # def print_map(self) -> None:
    #     for i in self.__map_matrix:
    #         print(*i, sep='')

'''  
    def add_console_lines(self, menu_matrix, index = 0):
        for line in menu_matrix:
            self.__console_matrix[index] = list(line)
            index +=1
          

    def put_game_object(self, game_object) -> None: # добавляет обьект на карту, но не кэширует
        if game_object.get_status():
            self.put_object_icon(game_object.get_icon(),
                                     game_object.get_x(), game_object.get_y())


    def put_object_icon(self, icon, x, y) -> None:
        # if isinstance(x, int) and isinstance(y, int):
            if x < self.__size_x and y < self.__size_y and x >= 0 and y >= 0:
                self.__map_matrix[int(y)][int(x)] = icon

    
    def put_pix_to_cash(self, icon, x, y) -> None:
        if x < self.__size_x and y < self.__size_y and x >= 0 and y >= 0:
                    self.__cash_map_matrix[int(y)][int(x)] = icon    
        
    
    def get_size_x(self) -> int:
        return self.__size_x
    
    
    def get_size_y(self) -> int:
        return self.__size_y
    

    def get_console_size(self) -> int:
        return self.__console_size
    

    def clamp(self, current, min, max):
        if current > max:
            return max
        if current < min:
            return min
        return current
    
    
    def clear_map(self) -> None: # должен вызываться каждую итерацию после отрисовки
        # очищаем выводимую карту от временных обьектов путем перезаписывания выводимой матрицы закэшированной
        # в бесконечном цикле игры
        self.__map_matrix = copy.deepcopy(self.__cash_map_matrix)
        self.__console_matrix = copy.deepcopy(self.__cash_console_matrix)

    def __console_generation(self):
        self.__console_matrix = [[' ' for x in range(self.__size_x)] for y in range(self.__console_size)]


    def set_console_pix(self, icon, x, y):
        if y < self.__size_x and x < self.__console_size:
            self.__console_matrix[x][y] = icon


    def cell_in_cash_is(self, key, x, y) -> bool: # keys 'water', 'tree', 'fire', 'tree'
            icon_dict = {'water': self.__water_icon,
                         'tree': self.__forest_icon,
                         'fire': self.__fire_icon,
                         'tree': self.__forest_icon}
            return (self.__cash_map_matrix[int(y)][int(x)] == icon_dict[key])
        
        
    def export_data(self, content_map = True) -> dict:
        if content_map:
            return {
            'size_x' : self.__size_x,
            'size_y' : self.__size_y,
            # 'console_size' : self.__console_size,
            'cash_map_matrix' : self.__cash_map_matrix,
            }
        return {
            'size_x' : self.__size_x,
            'size_y' : self.__size_y,
            }
        
        
    def import_data(self, mp_data) -> None:
        self.__size_x = mp_data['size_x']
        self.__size_y = mp_data['size_y']
        self.__cash_map_matrix = mp_data['cash_map_matrix']
        