import pyxel
import time
import random

from world import World
from component import *

version = '0.1.dev'

class System():
    def __init__(self, world, priority: int = 0) -> None:
        self.world: World = world
        self.priority = priority
        
    def process(self):
        pass
    
@dataclass
class SceneTransition():
    scenes: list[str] = field(default_factory=list)
    events: dict[dict] = field(default_factory=dict)
    to: dict[dict] = field(default_factory=dict)

class ev_update_resources(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.tag = "update-resources"
    
    def process(self):
        if self.world.schedule[self.world.current_scene][self.tag] != 1:
            return
        
        for entity, (player, resources) in self.world.get_components(PlayerComponent, ResourcesComponent):
            resources.apple += 1
            resources.banana += 1
            # print(resources.apple, resources.banana)
            
        self.world.schedule[self.world.current_scene][self.tag] = 0
        self.world.current_scene = "main"
        
class sys_handle_input(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        
        self.scenes_transitions = SceneTransition(
            scenes = ["launch", "choose-difficulty", "start-playing", "main", "result"],
            events = {"launch": {},
                    "choose-difficulty": {},
                    "start-playing": {"start-timer": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
                    "main": {"update-resources": lambda: pyxel.btnp(pyxel.KEY_SPACE),
                            "cal-result": lambda: self.world.time_left_to_sc <= 0},
                    "result": {"difficulty-up": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
            },
            to = {"launch": {"choose-difficulty": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
                "choose-difficulty": {"start-playing": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
                "start-playing": {"main": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
                "main": {"result": lambda: self.world.time_left_to_sc <= 0},
                "result": {"start-playing": lambda: pyxel.btnp(pyxel.KEY_RETURN)},
            },
        )
        
    def process(self):
        if self.world.current_scene not in self.scenes_transitions.scenes:
            # print("scene not found!")
            return
        # cli_text = f"Current scene: {self.world.current_scene} --------\nEvent candidates..\n"
        for event, triger in self.scenes_transitions.events[self.world.current_scene].items():
            # cli_text += f"Event: {event}, Triger: {triger}\n"
            if triger():
                self.world.schedule[self.world.current_scene][event] = 1
                # self.world.current_scene = event
                # print("Next Event:", self.world.current_scene, "!")
                
        for scene, triger in self.scenes_transitions.to[self.world.current_scene].items():
            if triger():
                self.world.next_scene = scene
                # print("Next scene:", self.world.next_scene)
        
        # print(cli_text)
        
class ev_start_timer(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.event = "start-timer"
    
    def process(self):
        if self.world.schedule[self.world.current_scene][self.event] != 1:
            return
        self.world.schedule[self.world.current_scene][self.event] = 0
        self.world.start_time = time.time()
        self.world.prev_time = self.world.start_time

class ev_cal_result(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.event = "cal-result"
    
    def process(self):
        if self.world.schedule[self.world.current_scene][self.event] != 1:
            return
        self.world.schedule[self.world.current_scene][self.event] = 0
        winner = None
        max_score = 0
        for entity, (resourecs) in self.world.get_component(ResourcesComponent):
            if max_score < resourecs.apple + resourecs.banana:
                max_score = resourecs.apple + resourecs.banana
                winner = entity
                
        self.world.winner = winner
        print(f"Winner is {winner}!")

class sys_result(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def process(self):
        pass
    

class sys_choose_difficulty(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.selected_difficulty = 0
        self.world.selected_difficulty = self.selected_difficulty

    def process(self):
        if pyxel.btnp(pyxel.KEY_A):
            self.selected_difficulty -= 1
        elif pyxel.btnp(pyxel.KEY_D):
            self.selected_difficulty += 1
            
        if self.selected_difficulty < 0:
            self.selected_difficulty = 0
        elif self.selected_difficulty > 2:
            self.selected_difficulty = 2
            
        self.world.selected_difficulty = self.selected_difficulty
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            for entity, opponent in self.world.get_component(NPOpponentComponent):
                opponent.difficulty = self.selected_difficulty
            self.world.current_scene = "start-playing"
        
class sys_round_timer(System):
    def __init__(self, world, priority: int = 0, round_time: int = 10) -> None:
        super().__init__(world, priority)
        self.round_time = round_time
        
    def process(self):
        self.world.time_left_to_sc = self.round_time - (self.world.current_time - self.world.start_time) // 1

class sys_npc_move(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.random_seed = random.seed(0)
        self.__default_press_interval = 0.1 # interval between NPC button press [sec]
    def process(self):
        if self.world.current_time - self.world.prev_time < self.__default_press_interval:
            return
        print("NPC will press button!")
        rand = random.random()
        for entity, (opponent, resources) in self.world.get_components(NPOpponentComponent, ResourcesComponent):
            if rand > opponent.press_btn_random_threshold:
                resources.apple += 1
                resources.banana += 1
        self.world.prev_time = self.world.current_time

class ev_difficulty_manager(System):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        self.event = "difficulty-up"
        
    def process(self):
        if self.world.schedule[self.world.current_scene][self.event] != 1:
            return
        level = None
        for entity, opponent in self.world.get_component(NPOpponentComponent):
            level = opponent.difficulty
            if self.world.winner == 0 and level is not None and level < 2:
                opponent.difficulty += 1
            elif self.world.winner == 0 and level is not None and level > 1:
                self.world.next_scene = "launch"
        print("Next level:", level)
        self.world.schedule[self.world.current_scene][self.event] = 0
        
        for entity, player in self.world.get_component(ResourcesComponent):
            player.apple = 0
            player.banana = 0