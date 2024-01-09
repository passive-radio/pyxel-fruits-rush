import pyxel
from component import *

version = '0.1.dev'

class Screen():
    def __init__(self, world, priority: int = 0) -> None:
        self.world: world = world
        self.priority = priority
        
    def draw(self):
        pass
    
class sc_launch_screen(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
    
    def draw(self):
        pyxel.cls(0)
        self.world.font_base.draw_text(55, 41, "ようこそサンプルゲームへ", 7)
        self.world.font_base.draw_text(55, 60, "エンターキーを押してスタート", 7)
        
class sc_start_playing_screen(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        
    def draw(self):
        pyxel.cls(0)
        self.world.font_base.draw_text(55, 41, "果物をふやそう！", 7)
        difficulty = self.world.get_component(NPOpponentComponent)[0][1].difficulty
        levels = ["よわい", "そこそこ強い", "けっこう強い"]
        self.world.font_base.draw_text(55, 80, f"敵: Level {difficulty} {levels[difficulty]}", 7)
        self.world.font_base.draw_text(55, 150, "エンターキーを押すと始まるよ！", 7)
        
class sc_main_screen(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
    
    def draw(self):
        self.world.font_base.draw_text(55, 10, "果物をふやそう！", 7)
        self.world.font_base.draw_text(300, 10, f"残り時間: {self.world.time_left_to_sc}", 7)
        self.world.font_base.draw_text(120, 50, "自分", 7)
        self.world.font_base.draw_text(380, 50, "敵", 7)
        difficulty = self.world.get_component(NPOpponentComponent)[0][1].difficulty
        levels = ["よわい", "そこそこ強い", "けっこう強い"]
        self.world.font_base.draw_text(400, 50, f"Level {difficulty} {levels[difficulty]}", 7)
        
        self.world.font_base.draw_text(55, 100, "りんご", 7)
        self.world.font_base.draw_text(55, 160, "バナナ", 7)
        
        self.world.font_base.draw_text(130, 100, f"{self.world.get_component(ResourcesComponent)[0][1].apple}", 7)
        self.world.font_base.draw_text(130, 160, f"{self.world.get_component(ResourcesComponent)[0][1].banana}", 7)
        
        self.world.font_base.draw_text(390, 100, f"{self.world.get_component(ResourcesComponent)[1][1].apple}", 7)
        self.world.font_base.draw_text(390, 160, f"{self.world.get_component(ResourcesComponent)[1][1].banana}", 7)

class sc_show_result(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
    
    def draw(self):
        self.world.font_base.draw_text(55, 10, "けっか発表！", 7)
        # self.world.font_base.draw_text(55, 10, "果物をふやそう！", 7)
        self.world.font_base.draw_text(120, 50, "自分", 7)
        self.world.font_base.draw_text(380, 50, "敵", 7)
        difficulty = self.world.get_component(NPOpponentComponent)[0][1].difficulty
        levels = ["よわい", "そこそこ強い", "けっこう強い"]
        self.world.font_base.draw_text(400, 50, f"Level {difficulty} {levels[difficulty]}", 7)
        self.world.font_base.draw_text(55, 100, "りんご", 7)
        self.world.font_base.draw_text(55, 160, "バナナ", 7)
        
        self.world.font_base.draw_text(130, 100, f"{self.world.get_component(ResourcesComponent)[0][1].apple}", 7)
        self.world.font_base.draw_text(130, 160, f"{self.world.get_component(ResourcesComponent)[0][1].banana}", 7)
        
        self.world.font_base.draw_text(390, 100, f"{self.world.get_component(ResourcesComponent)[1][1].apple}", 7)
        self.world.font_base.draw_text(390, 160, f"{self.world.get_component(ResourcesComponent)[1][1].banana}", 7)
        
        self.world.font_base.draw_text(120 + 260 * self.world.winner, 30, "勝ち！", 7)
        
        if self.world.winner == 0 and self.world.get_component(NPOpponentComponent)[0][1].difficulty < 2:
            self.world.font_base.draw_text(120, 400, "エンターキーを押して次のラウンドへ", 7)
        elif self.world.winner == 1:
            self.world.font_base.draw_text(120, 400, "エンターキーを押して再挑戦", 7)
        elif self.world.winner == 0:
            self.world.font_base.draw_text(120, 400, "強くなりすぎた君の周りには、いつしか誰もいなくなった...", 7)

class sc_choose_difficulty(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
        
    def draw(self):
        self.world.font_base.draw_text(55, 41, "敵の強さを選んでください", 7)
        
        for i, level in enumerate(["よわい", "そこそこ強い", "けっこう強い"]):
            if self.world.selected_difficulty == i:
                self.world.font_base.draw_text(55 + i * 100, 100, level, 8)
            else:
                self.world.font_base.draw_text(55 + i * 100, 100, level, 7)
            
        self.world.font_base.draw_text(30, 80, "←A", 7)
        self.world.font_base.draw_text(300, 80, "D→", 7)
        