# 🚁 🟩 🟦 🟫 🌳 🌲 🌴 🕍 🏥 🔥 ☁️

from game_object import Game_Object
from map import Map
from player import Player
from generation import Landscape_Generation
from game_logic import Game_logic, Event_handler
from my_console import Output_menu
import keyboard, os, cursor, time, win32console, win32con, time, json


if __name__ == '__main__':
    print('         FIRE HELICOPTER          ')
    print('Сontrol:')
    print()
    print('    W/A/S/D - up/left/down/right  ')
    print('    C - save game')
    print('    L - load game')
    print('    P - pause')
    print()
    print('    Press ENTER for Start')
    i = 500
    while i>0:
        if keyboard.is_pressed('enter'):
            i = 0
        time.sleep(0.01)
        i -= 1
    
    SIZE_X = 30
    SIZE_Y = 25
    DELAY = 0.001
    play_game = True
    menu = Output_menu()
    generator = Landscape_Generation(SIZE_X, SIZE_Y, '🟦', '🌲', '🟫', '🔥', '🟩')
    game_map = Map(generator)
    game_handler = Game_logic(game_map, '💭', score= 100)
    player = Player(SIZE_X, SIZE_Y, '🚁', int(SIZE_X/2), int(SIZE_Y/2), 1, 0.4,
                    hp= 3, water= 5)
    hospital = Game_Object(SIZE_X, SIZE_Y, '🏥', 2, 2, 0)
    workshop = Game_Object(SIZE_X, SIZE_Y, '🕍', 4, 2, 0)
    game_objects = [hospital, workshop, player]
    
    process_events = Event_handler([[game_handler.clouds_collision, player],
                                    [game_handler.put_out_fire_by, player],
                                    [game_handler.update_fire_ticks],
                                    [game_handler.burn_trees],
                                    [game_handler.put_clouds]])
    
    generation_events = Event_handler([[game_handler.move_clouds],
                                       [game_handler.generate_tree],
                                       [game_handler.generate_fire],
                                       [game_handler.generate_fire]])
    
    cloud_spawn_event = Event_handler([[game_handler.generate_clouds]])
    
    
    # Создание экранного буфера консоли
    my_console = win32console.CreateConsoleScreenBuffer(
        DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE,  # Режимы доступа к буферу
        ShareMode = 0,  # Режим совместного использования буфера
        SecurityAttributes = None,  # Атрибуты безопасности
        Flags = 1  # Флаги создания буфера
    )

    # Установка созданного буфера как активного
    my_console.SetConsoleActiveScreenBuffer()
    
    
    def draw_display():
        it = 0
        for list in game_map.get_matrix():
            list.append('    ')
            try:
                if list[0] == ' ':
                    list.append(' ' * (85 - len(list)))
                my_console.WriteConsoleOutputCharacter(
                    Characters = str(''.join(list)),  # Значение элемента, преобразованное в строку
                    WriteCoord = win32console.PyCOORDType(0, it)  # Координаты позиции вывода элемента
                )
            except Exception as ex:
                # print(ex)
                pass 
            it += 1


    def pause_n_play(freeze_player = True):
        time.sleep(0.1)
        global play_game
        if play_game == True:
            play_game = False
            pause_frame = menu.get_pause_frame(game_handler.score)
            if freeze_player:
                player.set_step(0)
            else:
                for it in range(len(pause_frame)):
                    menu.put_str(pause_frame[it], it)
            
            menu.put_console_on(game_map)
            draw_display()
        else:
            time.sleep(0.1)
            play_game = True
            player.set_step(1)
            
            
    def check_game_condition():
        global stop_update
        if player.get_hp() <= 0 or game_handler.score <= 0:
            time.sleep(0.1)
            stop_frame = menu.get_over_frame(game_handler.score)

            for it in range(len(stop_frame)):
                menu.put_str(stop_frame[it], it)

            menu.put_console_on(game_map)
            draw_display()
            time.sleep(2)
            stop_update = True
            
            
    def save_game():
        data = {
               'player': player.export_data(),
               'hospital': hospital.export_data(),
               'workshop': workshop.export_data(),
               'game_handler': game_handler.export_data(),
               'game_map': game_map.export_data()
               }
        with open('save.json', 'w') as save:
            json.dump(data, save)
            
            
    def load_game():
        global player
        with open('save.json', 'r') as load:
            data = json.load(load)
    
        player.import_data(data['player'])
        hospital.import_data(data['hospital'])
        workshop.import_data(data['workshop'])
        game_map.import_data(data['game_map'])
        game_handler.import_data(data['game_handler'])
    

    cursor.hide()
    delta_for_fps = 0.01
    count = 0
    periodicity = 160
    count_for_save = 0
    count_for_load = 0

    '''
    Сделать сохранение:
        - Списки всех объектов - облака, пожары,
        - Саму карту и все ее аттрибуты
        - Стату игрока - все аттрибуты
        - Координаты госпиталя и мастерской
    
    '''
    
    stop_update = False
    # stop_update = True
    workshop_flag = False
    while not stop_update:
        start = time.time()
        game_map.clear_map()
        fps = int(1/delta_for_fps)
        count += 1
        if count >= 10001:
            count = 0
        
        if play_game:
            player.update_water_event(count, periodicity, game_map)
            player.update_hp_event(count, periodicity, hospital)
            menu.update_game_info(player, game_handler, fps)
            
        else:
            pause_frame = menu.get_pause_frame(game_handler.score)
            for it in range(len(pause_frame)):
                menu.put_str(pause_frame[it], it)
                
        if count_for_save > 0:
            menu.put_str('  Game saved.'+ ' '*19, 0)
            count_for_save -= 1
            
        if count_for_load > 0:
            menu.put_str('  Saved game loaded.'+ ' '*19, 0)   
            count_for_load -= 1
                         
        menu.put_console_on(game_map)
            
        player.key_events()
        process_events.run(periodicity, periodicity, play_game)

        for object in game_objects:
            game_map.put_game_object(object)

        generation_events.run(count, periodicity, play_game)
        cloud_spawn_event.run(count, periodicity*3, play_game)
        
        workshop_flag_cash = workshop_flag
        workshop_flag = player.is_in_pos(workshop.get_pos())
        if workshop_flag_cash != workshop_flag:
            pause_n_play(False) 
        if player.is_in_pos(workshop.get_pos()):
            menu.show_workshop_menu(player, game_map, game_handler)
            
        if keyboard.is_pressed('p'):
            pause_n_play()
        if keyboard.is_pressed('c'):
            save_game()
            count_for_save = 250
        if keyboard.is_pressed('l'):
            load_game()
            count_for_load = 250
        
        check_game_condition()
        draw_display()
        time.sleep(DELAY)
        delta_for_fps = time.time() - start
        
        # stop_update = (count == 2000)
    

    