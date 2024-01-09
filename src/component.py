from typing import Type, TypeVar
from dataclasses import dataclass, field

version = '0.1.dev'

"""
This module uses dataclass decorator to define the base component class, thus Python 3.7+ is required.
Please change the Python version in your envinment to 3.7 or higher if you uses Python < 3.7.
"""

@dataclass
class Component:
    """Base class for components."""
    
@dataclass
class ResourcesComponent(Component):
    apple: int = 0
    banana: int = 0
    
class PlayerComponent(Component):
    pass

class NPOpponentComponent(Component):
    def __init__(self, difficulty: int = 0) -> None:
        "difficulty = 0: easy, 1: normal, 2: hard"
        self.difficulty: int = difficulty
        self.press_btn_random_threshold = self.__def_press_btn_random_threshold()
        
    def __def_press_btn_random_threshold(self):
        if self.difficulty == 0:
            return 0.3
        elif self.difficulty == 1:
            return 0.5
        elif self.difficulty == 2:
            return 0.85
        else:
            return 0.3
        