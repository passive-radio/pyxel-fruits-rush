import pyxel
import time

from world import World
from component import *
from system import *
from screen import *
from font import BDFRenderer

version = '0.1.dev'

class App(World):
    def __init__(self):
        super().__init__()
        self.FPS = 60
        pyxel.init(640, 480, title = "test", fps = self.FPS)
        pyxel.mouse(True)
        self.count_frame = 0
        self.scene_systems: dict[list] = {}
        self.scene_screens: dict[list] = {}
        self.schedule: dict[dict] = {"launch": {"launch": 0, "start-playing": 0},
            "choose-difficulty": {"choose-difficulty": 0, "start-playing": 0},
            "start-playing": {"start-timer": 0},
            "main": {"main": 0, "update-resources": 0, "cal-result": 0},
            "result": {"difficulty-up": 0},
            "update-resources": {"update-resources": 0}}
        self.font_base = BDFRenderer("assets/font/umplus_j12r.bdf")
        self.next_scene = None
        self.time_left_to_sc = 10
    
    def run(self):
        # print(self.current_scene)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.update_state()
        self.count_frame += 1
        self.current_time = time.time()
        if self.next_scene is not None:
            self.prev_scene = self.current_scene
            self.current_scene = self.next_scene
            self.next_scene = None
        
    def draw(self):
        pyxel.cls(0)
        self.update_screen()
    
    def update_state(self):
        for system in self.scene_systems[self.current_scene]:
            system: System
            system.process()

    def update_screen(self):
        for screen in self.scene_screens[self.current_scene]:
            screen: Screen
            screen.draw()
            
    def add_system(self, system, scenes: list[str], priority = 0):
        if type(scenes) == str:
            scene = scenes
            if self.scene_systems.get(scene) is None:
                self.scene_systems.update({scene: []})
            self.scene_systems[scene].append(system)
            self.scene_systems[scene] = sorted(self.scene_systems[scene], key=lambda x: x.priority)
            return
        
        for scene in scenes:
            if self.scene_systems.get(scene) is None:
                self.scene_systems.update({scene: []})
            self.scene_systems[scene].append(system)
            self.scene_systems[scene] = sorted(self.scene_systems[scene], key=lambda x: x.priority)

    def add_screen(self, screen, scenes: list[str], priority = 0):
        for scene in scenes:
            if self.scene_screens.get(scene) is None:
                self.scene_screens.update({scene: []})
            self.scene_screens[scene].append(screen)
            self.scene_screens[scene] = sorted(self.scene_screens[scene], key=lambda x: x.priority)
    
if __name__ == "__main__":
    app = App()
    player = app.create_entity()
    np_opponent = app.create_entity()
    
    app.add_component_to_entity(np_opponent, NPOpponentComponent(0))
    app.add_component_to_entity(np_opponent, ResourcesComponent(0, 0))
    app.add_component_to_entity(player, ResourcesComponent(0, 0))
    app.add_component_to_entity(player, PlayerComponent())
    
    app.add_system(sys_handle_input(app, -100), ["launch", "choose-difficulty", "start-playing", "main", "update-resources", "result"])
    app.add_system(ev_start_timer(app), ["start-playing"])
    app.add_system(sys_round_timer(app, -101), ["main"])
    app.add_system(ev_update_resources(app), ["main"])
    app.add_system(sys_npc_move(app), ["main"])
    app.add_system(sys_choose_difficulty(app), ["choose-difficulty"])
    app.add_system(ev_cal_result(app), ["main"])
    app.add_system(sys_result(app), ["result"])
    app.add_system(ev_difficulty_manager(app), ["result"])
    
    app.add_screen(sc_launch_screen(app), ["launch"])
    app.add_screen(sc_start_playing_screen(app), ["start-playing"])
    app.add_screen(sc_main_screen(app), ["main", "update-resources"])
    app.add_screen(sc_choose_difficulty(app), ["choose-difficulty"])
    app.add_screen(sc_show_result(app), ["result"])
    
    app.current_scene = "launch"
    app.run()
    