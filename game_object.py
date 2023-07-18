class Game_Object(object):
    __icon = ' '
    __x = 1
    __y = 1
    __id = 0
    __obj_count_id = 0
    __step = int(0)
    __is_active = True
    __max_x = 10
    __max_y = 10

    def __init__(self, max_x = 10, max_y = 10, icon = '*', x = 1, y = 1, step = 0, activity = True
                 ) -> None:
        self.__id = Game_Object.__obj_count_id
        Game_Object.__obj_count_id += 1
        self.__step = step
        self.__is_active = True
        self.__icon = icon
        self.__max_x = max_x
        self.__max_y = max_y
        self.set_pos(x, y)
        self.__is_active = activity

    
    def get_id(self) -> int:
        return self.__id


    def get_x(self) -> int:
        return self.__x
    
    
    def get_y(self) -> int:
        return self.__y
    

    def get_step(self) -> int:
        return self.__step
    

    def get_pos(self) -> list:
        return [self.__x, self.__y]
    

    def set_activity(self, is_active: bool) -> None:
        self.__is_active = bool(is_active)
        
        
    def set_step(self, value: int) -> None:
        if value >= 0:
            self.__step = int(value)

    
    def get_status(self) -> bool:
        return self.__is_active


    def move_x(self, x) -> None:
        self.__x = self.clamp(x, 1, (self.__max_x)-2)
        

    def move_y(self, y) -> None:
        self.__y = self.clamp(y, 1, (self.__max_y)-2)


    def set_pos(self, x, y) -> None:
        self.move_x(x)
        self.move_y(y)


    def set_icon(self, icon) -> None:
        self.__icon = icon


    def get_icon(self) -> str():
        return self.__icon
    
    
    def clamp(self, current, min_v, max_v):
        return max(min(current, max_v), min_v)
    

    def is_in_pos(self, object_pos) -> bool:
        return (self.get_pos() == object_pos)
    
    
    def export_data(self) -> dict:
        return {
            'x' : self.__x,
            'y' : self.__y,
            'step': self.__step,
            'is_active' : self.__is_active,
            'max_x' : self.__max_x,
            'max_y' : self.__max_y
        }
        
        
    def import_data(self, go_data) -> None:
        self.__step = go_data['step']
        self.__max_x = go_data['max_x']
        self.__max_y = go_data['max_y']
        self.set_pos(go_data['x'], go_data['y'])
        self.__is_active = go_data['is_active']