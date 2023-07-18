import keyboard, time

class Output_menu(object):
# хранит в себе матрицу, которая выводится внизу под игровой областью.
# можно изменять построчно
    __str_count = 0
    coefficients = []
    __hp_icon = '💖'
    __hp_capacity_icon = '🖤'
    __water_icon = '💧'
    __water_capacity_icon = '🥛'
    __buff = []
    __stop_frame = []
    __workshop_menu_matrix = ['                        ',
                              '  WORKSHOP MENU         ',
                              '                        ',
                             f'  1. Maximum HP:           ',
                             f'  2. Water capacity:          ',
                             f'  3. Max speed:           ',
                              '                        ',
                             f'  Score:                ',
                              '                        ',
                              '                        ']
    __selected_el = 0
    # __con_matrix = __buff[:]
    '''
    # __con_matrix = [' ',
    #                 '  HELICOPTER STATUS:',
    #                 ' ',
    #                 '  💧💧',
    #                 '  💖💖💖',
    #                 ' '
    #                 '  FPS: ',
    #                 ' ',
    #                 '  Score ',
    #                 '  Len fire list ',
    #                 ' ']'''


    def __init__(self, buff = ['                        ',
                               '  HELICOPTER STATUS:    ',
                               '                        ',
                               '                        ',
                               '                        ',
                               '                        ',
                               '                        ',
                               '                        ',
                               '                        ',
                               '                        '],
                 stop_frame = ['                        ',
                    '                            ',
                    '  Score: ',
                    '                        ',
                    '                        ',
                    '                        ',
                    '                        ',
                    '                        ',
                    '                        ',
                    '                        ']):
        self.clear_buff()
        self.__buff = buff
        self.__stop_frame = stop_frame
        self.__con_matrix = self.__buff[:]


    def get_matrix(self) -> list:
        return self.__con_matrix
    

    def clear_buff(self) -> None:
        self.__con_matrix = self.__buff[:]
        self.__str_count = len(self.__con_matrix)


    def put_console_on(self, any_map) -> None:
        any_map.add_console_lines(self.__con_matrix)
    
    
    def update_game_info(self, any_player, game_logic, fps) -> None:
        self.__con_matrix = self.__buff[:]
        self.__con_matrix[3] = str('  ' +
                                    (self.__water_icon * any_player.get_water()) +
                                    (self.__water_capacity_icon * (any_player.get_water_capacity() - any_player.get_water()))+ '                        ') 
        self.__con_matrix[4] = str('  ' +
                                    (self.__hp_icon * any_player.get_hp()) +
                                    (self.__hp_capacity_icon * (any_player.get_hp_capacity() - any_player.get_hp()))+ '                        ')        
        self.__con_matrix[6] = '  FPS: ' + str(fps) + '                        '
        self.__con_matrix[8] = '  Score ' + str(game_logic.score) + '                        '
        self.__con_matrix[9] = '  Fire amount ' + str(game_logic.get_fire_amount()) + '                        '
        
        
    def put_str(self, string: str, pos: int) -> None:
        if pos < len(self.__con_matrix):
            self.__con_matrix[pos] = str(string)
            
            
    def get_pause_frame(self, score) -> list:
        res = self.__stop_frame[:]
        res[1] = '  PAUSE                    '
        res[2] = f'  Score: {score}'
        return res
    
    
    def get_over_frame(self, score) -> list:
        res = self.__stop_frame[:]
        res[1] = '  GAME OVER                 '
        res[2] = f'  Score: {score}'
        return res
    
    __hp_price = 100
    __water_price = 100
    __speed_price = 100
    def show_workshop_menu(self, player, map, game_handler):
        self.__con_matrix = ['                        ',
                             '  WORKSHOP MENU         ',
                             '                        ',
                            f'  1. Maximum HP: {self.__hp_icon} x {player.get_hp_capacity()}                   ',
                            f'  2. Water capacity: {self.__water_icon} x {player.get_water_capacity()}                   ',
                            f'  3. Max speed: {round(player.get_speed(), 1)}                   ',
                             '                        ',
                            f'  Score: {game_handler.score}        ',
                             '  [1/2/3]?              ',
                             '                        ']
        menu_event_list = [[1, f' | + 1 = -{self.__hp_price} score', player.up_hp_capacity],
                           [2, f' | + 1 = -{self.__water_price} score', player.up_water_capacity],
                           [3, f' | + 0.1 = -{self.__speed_price} score', player.up_speed],
                           [4, '                   '],
                           [5, '                   '],
                           [6, '                   '],
                           [7, '                   '],
                           [8, '                   '],
                           [9, '                   '],
                           [0, '                   '],
                           ]
            
        for event in menu_event_list:
            if keyboard.is_pressed(str(event[0])):
                self.__selected_el = event[0]
            if self.__selected_el == event[0] and event[0] < 4:
                self.__con_matrix[2 + event[0]] = self.__con_matrix[2 + event[0]][:len(self.__con_matrix[2 + event[0]])-19] + event[1]

            if self.__selected_el != 0:
                self.__con_matrix[8] = '  Upgrade [y/n]?       '
                
        if keyboard.is_pressed('y'):
            time.sleep(0.2)
            if len(menu_event_list[self.__selected_el-1]) > 2:
                menu_event_list[self.__selected_el-1][2]()
                
            if self.__selected_el == 1:
                game_handler.score -= self.__hp_price
                self.__hp_price *= 1.5
            elif self.__selected_el == 2:
                game_handler.score -= self.__water_price
                self.__water_price *= 1.5
            elif self.__selected_el == 3:
                game_handler.score -= self.__speed_price
                self.__speed_price *= 1.5
                
            
        self.put_console_on(map)