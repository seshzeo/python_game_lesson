from game_object import Game_Object
import keyboard

class Player(Game_Object):
    __speed = 1
    __hp = 3
    __water = 2
    __hp_capacity = 3
    __water_capacity = 10
    __count_x = 0
    __count_y = 0
    __icon_damage = '⚡️'
    __icon = '*'
    __damaged_pos = [0, 0]


    def __init__(self, max_x, max_y, icon = '*', x = 1, y = 1, step = 0, speed = 1, hp = 3, water = 5, activity = True,
                 hp_capacity = 3, water_capacity = 5) -> None:
        super().__init__(max_x, max_y, icon, x, y, step, activity)
        self.__speed = speed
        self.__icon = icon
        self.__hp = hp
        self.__hp_capacity = hp_capacity
        self.__water = water
        self.__water_capacity = water_capacity

    # с помощью счетчика count_x и _y специально ограничиваю скорость вертолета
    # иначе летает слишком быстро
    def change_pos_x(self, step_x) -> None:
        self.__count_x += 1
        if self.__count_x == int(10/self.__speed): 
            self.__count_x = 0
            if step_x > 0:
                self.move_x(self.get_x() + self.get_step())
            if step_x < 0:
                self.move_x(self.get_x() - self.get_step())

            
    def change_pos_y(self, step_y) -> None:
        self.__count_y += 1
        if self.__count_y == int(10/self.__speed):
            self.__count_y = 0
            if step_y > 0:
                self.move_y(self.get_y() + self.get_step())
            if step_y < 0:
                self.move_y(self.get_y() - self.get_step())


    def update_hp(self, value) -> None:
        clamp_val = max(min(value, self.__hp_capacity), 0)
        self.__hp = clamp_val


    def update_water(self, value) -> None:
        clamp_val = max(min(value, self.__water_capacity), 0)
        self.__water = clamp_val


    def update_hp_capasity(self, value) -> None:
        if value > 0:
            self.__hp_capacity = value

            
    def update_water_capasity(self, value) -> None:
        if value > 0:
            self.__water_capacity = value


    def get_hp(self) -> int:
        return self.__hp
    
    
    def get_water(self) -> int:
        return self.__water
    
    
    def get_speed(self) -> int:
        return self.__speed
    

    def get_hp_capacity(self) -> int:
        return self.__hp_capacity
    
    
    def get_water_capacity(self) -> int:
        return self.__water_capacity
    
    
    def get_gamage(self) -> None:
        self.update_hp(self.__hp - 1)
        self.set_icon(self.__icon_damage)
        self.__damaged_pos = self.get_pos()
        
        
    def up_hp_capacity(self) -> None:
        self.__hp_capacity += 1
        
        
    def up_water_capacity(self) -> None:
        self.__water_capacity += 1
        
    
    def up_speed(self) -> None:
        self.__speed += 0.1
        
        
    def return_icon(self) -> None:
        delta_x = self.__damaged_pos[0] - self.get_x()
        delta_y = self.__damaged_pos[1] - self.get_y()
        if delta_x > 1 or delta_x < -1 or delta_y > 1 or delta_y < -1:
            super().set_icon(self.__icon)
    
    
    def key_events(self) -> None:
        key_events_list = [
            ['s', self.change_pos_y, 1],
            ['w', self.change_pos_y, -1],
            ['a', self.change_pos_x, -1],
            ['d', self.change_pos_x, 1],
        ]
        
        for event in key_events_list:
            if keyboard.is_pressed(event[0]):
                event[1](event[2])
                
        self.return_icon()
        
        
    def update_water_event(self, count, step_for_count, any_map) -> None:
        if count*2 % step_for_count == 0:
            if any_map.cell_in_cash_is('water', super().get_x(), super().get_y()):
                self.update_water(self.__water + 1)
                
                
    def update_hp_event(self, count, step_for_count, any_hospital) -> None:
        if count % step_for_count == 0:
            if self.is_in_pos(any_hospital.get_pos()):
                self.update_hp(self.__hp + 1)
                
            
    def export_data(self) -> dict:
        child_data = {
            'speed' : self.__speed, 
            'hp' : self.__hp, 
            'water' : self.__water, 
            'hp_capacity' : self.__hp_capacity, 
            'water_capacity' : self.__water_capacity
        }
        parent_data = super().export_data()
        return {**parent_data, **child_data}
    
    
    def import_data(self, p_data):
        super().import_data(p_data)
        self.__speed = p_data['speed']
        self.__hp = p_data['hp']
        self.__hp_capacity = p_data['hp_capacity']
        self.__water = p_data['water']
        self.__water_capacity = p_data['water_capacity']
        