from game_object import Game_Object
import random

class Game_logic(object):
# совокупность методов, счетчиков, списков объектов для выполнения 
# игровой логики и хранения промежуточнорго состояния игровых объектов
    __fire_icon = '🔥'
    __cloud_icon = '💭'
    __map = None
    __clouds_list = []
    __fire_list = []
    __max_fire_len_list = 20
    __fire_count_coef = 0.5
    water_density = .01
    forest_density = 30
    score = 100
    
    
    def __init__(self, map, cloud_icon, score = 100, max_fire_len_list = 20,
                 fire_count_coef = 0.5, water_density = .01, forest_density = 30,
                 fire_list = [], clouds_list = []):
        self.__map = map
        self.__fire_icon = map.generator.get_fire_icon()
        self.__forest_icon = map.generator.get_forest_icon()
        self.__ground_icon = map.generator.get_ground_icon()
        self.__cloud_icon = cloud_icon
        self.score = score
        self.__max_fire_len_list = max_fire_len_list
        self.__fire_count_coef = fire_count_coef
        self.water_density = water_density
        self.forest_density = forest_density
        self.__clouds_list = clouds_list
        self.__fire_list = fire_list
        
        
    def get_fire_amount(self) -> int:
        return len(self.__fire_list)
    
    
    def generate_clouds(self):
        any_cloud = Game_Object(self.__map.get_size_x(),
                                self.__map.get_size_y(),
                                self.__cloud_icon,
                                self.__map.get_size_x(),
                                random.randint(1, self.__map.get_size_y() - 2),
                                1)
        self.__clouds_list.append(any_cloud)

        del_list = []
        for index in range(len(self.__clouds_list)):
            if self.__clouds_list[index].get_x() <= 1:
                del_list.append(index)

        for index in del_list:
            del self.__clouds_list[index]


    def put_clouds(self) -> None:
            for cloud in self.__clouds_list:
                self.__map.put_game_object(cloud)


    def move_clouds(self) -> None:
            for cloud in self.__clouds_list:
                cloud.move_x(cloud.get_x()-1)
    
    
    def generate_tree(self):
        can_gen = False
        rand_cell = self.__map.generator.random_cell()
        rand_x, rand_y = rand_cell[0], rand_cell[1]
        coords = [[-1,-1], [0,-1], [1,-1],
                  [-1, 0], [0, 0], [1, 0],
                  [-1, 1], [0, 1], [1, 1]]
        for coord in coords:
            if self.__map.cell_in_cash_is('tree', rand_x + coord[0], rand_y + coord[1]):
                can_gen = True

        if can_gen and not self.__map.cell_in_cash_is('water', rand_x, rand_y):
            self.__map.put_object_icon(self.__forest_icon, rand_cell[0], rand_cell[1])
            self.__map.put_pix_to_cash(self.__forest_icon, rand_cell[0], rand_cell[1])


    def generate_fire(self):
        if len(self.__fire_list) < self.__max_fire_len_list:
            rand_cell = self.__map.generator.random_cell()
            rand_x, rand_y = rand_cell[0], rand_cell[1]

            if self.__map.cell_in_cash_is('tree', rand_x, rand_y):
                self.__map.put_object_icon(self.__fire_icon, rand_x, rand_y)
                self.__map.put_pix_to_cash(self.__fire_icon, rand_x, rand_y)
                tick = random.randint(8000 * self.__fire_count_coef, 12000 * self.__fire_count_coef)
                self.__fire_list.append([rand_x, rand_y, tick])


    def update_fire_ticks(self): # обновление счетчика жизни пожаров
        for index in range(len(self.__fire_list)):
            if self.__fire_list[index][2] > 0:
                self.__fire_list[index][2] -= 1


    def burn_trees(self):
        # в цикле пробегаемся по всем созданным пожарам в списке пожаров
        for index in range(len(self.__fire_list)):
            tick = self.__fire_list[index][2]
            fire_x, fire_y = self.__fire_list[index][0], self.__fire_list[index][1]
            # Проверяем счетчик жизни. Почему то удалялась еще и вода, поэтому добавил проверку на то
            # не обозначена ли в кеше целевая клетка как вода.
            
            coords = [[-1,-1], [0,-1], [1,-1],
                  [-1, 0], [0, 0], [1, 0],
                  [-1, 1], [0, 1], [1, 1]]
            
            if tick <= 1 and not self.__map.cell_in_cash_is('water', fire_x, fire_y): # 
                # Если проверка пройдена, то меняем текстуру огня в клетке на матрице для вывода и в кешируемой матрице
                # на тектсуру земли и добавляем огонек в лист для последующего удаления из списка акуальных пожаров
                for coord in coords:
                    if self.__map.cell_in_cash_is('tree', fire_x + coord[0], fire_y + coord[1]):
                        self.__map.put_object_icon(self.__ground_icon, fire_x + coord[0], fire_y + coord[1])
                        self.__map.put_pix_to_cash(self.__ground_icon, fire_x + coord[0], fire_y + coord[1])
                
                
                self.__map.put_object_icon(self.__ground_icon, fire_x, fire_y)
                self.__map.put_pix_to_cash(self.__ground_icon, fire_x, fire_y)
                
                del self.__fire_list[index]
                self.score -= 20
                break


    def put_out_fire_by(self, any_player):
        for fire_index in range(len(self.__fire_list)):
            check_x = self.__fire_list[fire_index][0]
            check_y = self.__fire_list[fire_index][1]
            
            if any_player.is_in_pos(self.__fire_list[fire_index][:2]) and any_player.get_water() > 0:
                self.__fire_list.pop(fire_index)
                any_player.update_water(any_player.get_water()-1)
                self.__map.put_object_icon(self.__forest_icon, check_x, check_y)
                self.__map.put_pix_to_cash(self.__forest_icon, check_x, check_y)
                self.score += 10
                break
            
            
    def clouds_collision(self, any_player):
        for cloud_index in range(len(self.__clouds_list)):
            if self.__clouds_list[cloud_index].is_in_pos(any_player.get_pos()):
                any_player.get_gamage()
                del self.__clouds_list[cloud_index]
                break
            
            
    def export_data(self):
        cloud_data_list = []
        for cloud in self.__clouds_list:
            cloud_data_list.append(cloud.export_data())
        return {
            'clouds_list': cloud_data_list,
            'fire_list': self.__fire_list,
            'max_fire_len_list': self.__max_fire_len_list,
            'fire_count_coef': self.__fire_count_coef,
            'water_density': self.water_density,
            'forest_density': self.forest_density,
            'score': self.score
        }
        
        
    def import_data(self, gh_data) -> None:
        self.score = gh_data['score']
        self.__max_fire_len_list = gh_data['max_fire_len_list']
        self.__fire_count_coef = gh_data['fire_count_coef']
        self.water_density = gh_data['water_density']
        self.forest_density = gh_data['forest_density']
        self.__fire_list = gh_data['fire_list']
        self.__clouds_list = []
        
        for cloud_data in gh_data['clouds_list']:
            cloud = Game_Object(icon= self.__cloud_icon)
            cloud.import_data(cloud_data)
            self.__clouds_list.append(cloud)
            
        
        
    def get_cloud_list(self) -> list:
        return self.__clouds_list




class Event_handler(object):
# обработчик событий игровой логики
    __func_list = [[]]
    
    
    def __init__(self, func_list):
        self.__func_list = func_list    

    
    def run(self, count, periodicity, predicate = True):
        if int(count) % int(periodicity) == 0 and predicate:
            for item in self.__func_list:
                    func = item[0]
                    args = item[1:]
                    func(*args)
    
