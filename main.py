__version__ = "1.0.0"
"""SNEERYBOOSTER MOBILE - Dense Premium UI, Mobile Viewport 430dp."""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation

# Force portrait mobile size, but constrain content to 430dp centered
Window.size = (390, 844)  # iPhone 12-ish, dense

from ui.screens.home import HomeScreen
from ui.screens.games import GamesScreen
from ui.screens.boost import BoostScreen
from ui.screens.ai import AIScreen
from ui.screens.settings import SettingsScreen

from core.booster import BoosterEngine
from core.game_detector import GameDetector
from core.performance import PerformanceMonitor
from core.overlay import OverlayManager
from core.dnd import DNDManager
from core.storage import storage_manager
from utils.logger import log

class SneeryBoosterApp(App):
    def build(self):
        self.title = "SNEERYBOOSTER MOBILE"
        # Core
        self.performance = PerformanceMonitor()
        self.overlay = OverlayManager()
        self.dnd = DNDManager()
        self.game_detector = GameDetector()
        self.booster = BoosterEngine(
            game_detector=self.game_detector,
            dnd=self.dnd,
            overlay=self.overlay,
            performance=self.performance
        )
        storage_manager.ensure()

        # Root - outer background with ambient blobs
        root = FloatLayout()
        with root.canvas.before:
            Color(1,1,1,1)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
            # Ambient blobs
            Color(0.85, 0.91, 1, 0.22)
            self.blob1 = RoundedRectangle(pos=(root.x-dp(60), root.y+root.height-dp(260)), size=(dp(280), dp(280)), radius=[dp(140)])
            Color(0.94, 0.88, 1, 0.16)
            self.blob2 = RoundedRectangle(pos=(root.x+root.width-dp(160), root.y+root.height-dp(420)), size=(dp(260), dp(260)), radius=[dp(130)])
            Color(0.85, 0.91, 1, 0.08)
            self.blob3 = RoundedRectangle(pos=(root.x+dp(40), root.y+dp(80)), size=(dp(200), dp(200)), radius=[dp(100)])
        root.bind(pos=self._update_bg, size=self._update_bg)

        # Mobile viewport - constrained to 430dp, centered
        self.viewport = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(390), dp(800)), pos_hint={'center_x':0.5, 'center_y':0.5})
        # Shadow for viewport
        with self.viewport.canvas.before:
            Color(0.06, 0.18, 0.42, 0.08)
            self.vp_shadow = RoundedRectangle(radius=[dp(24)], pos=(self.viewport.x+dp(2), self.viewport.y-dp(4)), size=self.viewport.size)
            Color(1,1,1,0.96)
            self.vp_bg = RoundedRectangle(radius=[dp(24)], pos=self.viewport.pos, size=self.viewport.size)
            Color(1,1,1,0.9)
            self.vp_border = RoundedRectangle(radius=[dp(24)], pos=self.viewport.pos, size=self.viewport.size)
        self.viewport.bind(pos=self._update_vp, size=self._update_vp)

        # ScreenManager inside viewport
        self.sm = ScreenManager(transition=FadeTransition(duration=0.22))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(GamesScreen(name='games'))
        self.sm.add_widget(BoostScreen(name='boost'))
        self.sm.add_widget(AIScreen(name='ai'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        # Content area with screens
        content = BoxLayout(orientation='vertical')
        content.add_widget(self.sm)

        # Floating frosted nav - 64dp height, rounded 24, margin 12
        nav_container = BoxLayout(size_hint_y=None, height=dp(72), padding=[dp(12), dp(8), dp(12), dp(12)])
        nav = BoxLayout(spacing=dp(4), padding=dp(6))
        nav.size_hint_y = None
        nav.height = dp(56)
        with nav.canvas.before:
            Color(1,1,1,0.88)
            self.nav_bg = RoundedRectangle(radius=[dp(28)], pos=nav.pos, size=nav.size)
            Color(0,0,0,0.06)
            self.nav_shadow = RoundedRectangle(radius=[dp(28)], pos=(nav.x, nav.y-dp(2)), size=nav.size)
            Color(1,1,1,0.9)
            self.nav_border = RoundedRectangle(radius=[dp(28)], pos=nav.pos, size=nav.size)
        nav.bind(pos=self._update_nav, size=self._update_nav)

        self.nav_buttons = {}
        self.nav_indicator = Widget(size_hint=(None,None), size=(dp(32), dp(3)), pos_hint={'center_y':0.5})
        with self.nav_indicator.canvas:
            Color(0.16, 0.42, 1, 1)
            self.ind_rect = RoundedRectangle(radius=[dp(1.5)], pos=self.nav_indicator.pos, size=self.nav_indicator.size)
        self.nav_indicator.bind(pos=lambda inst,val: setattr(self.ind_rect, 'pos', val))

        for key, label in [('home','HOME'),('games','GAMES'),('boost','BOOST'),('ai','AI'),('settings','SETTINGS')]:
            btn = Button(text=label, font_size='9sp', bold=True, background_color=(0,0,0,0), color=(0.58,0.63,0.72,1))
            btn.background_normal = ''
            btn.bind(on_release=lambda _,k=key: self.switch_to(k))
            self.nav_buttons[key] = btn
            nav.add_widget(btn)
        # Add indicator under active
        # For simplicity, indicator is separate, we move it on switch
        nav_container.add_widget(nav)
        self.nav = nav

        content.add_widget(nav_container)
        self.viewport.add_widget(content)
        root.add_widget(self.viewport)

        # Bind window resize to keep viewport centered and constrained
        Window.bind(size=self._on_window_resize)
        Clock.schedule_once(lambda dt: self._update_vp(), 0.1)
        Clock.schedule_once(lambda dt: self.switch_to('home'), 0.2)

        log.info("SNEERYBOOSTER MOBILE dense build - viewport 390dp")
        return root

    def _update_bg(self, *args):
        # Update outer bg and blobs
        if hasattr(self, 'bg_rect'):
            root = self.root
            if root:
                self.bg_rect.pos = root.pos
                self.bg_rect.size = root.size
                self.blob1.pos = (root.x-dp(60), root.y+root.height-dp(260))
                self.blob2.pos = (root.x+root.width-dp(160), root.y+root.height-dp(420))
                self.blob3.pos = (root.x+dp(40), root.y+dp(80))

    def _update_vp(self, *args):
        if hasattr(self, 'vp_bg'):
            self.vp_bg.pos = self.viewport.pos
            self.vp_bg.size = self.viewport.size
            self.vp_shadow.pos = (self.viewport.x+dp(2), self.viewport.y-dp(4))
            self.vp_shadow.size = self.viewport.size
            self.vp_border.pos = self.viewport.pos
            self.vp_border.size = self.viewport.size

    def _update_nav(self, *args):
        self.nav_bg.pos = self.nav.pos
        self.nav_bg.size = self.nav.size
        self.nav_shadow.pos = (self.nav.x, self.nav.y-dp(2))
        self.nav_shadow.size = self.nav.size
        self.nav_border.pos = self.nav.pos
        self.nav_border.size = self.nav.size

    def _on_window_resize(self, instance, size):
        # Keep viewport at 390dp, centered, not stretched
        max_w = dp(430)
        w = min(size[0] - dp(32), max_w)
        h = min(size[1] - dp(32), dp(844))
        self.viewport.size = (w, h)
        self.viewport.pos_hint = {'center_x':0.5, 'center_y':0.5}

    def switch_to(self, name):
        # Page transition + nav indicator
        if self.sm.current != name:
            self.sm.transition = SlideTransition(direction='left', duration=0.22)
            self.sm.current = name
        # Update nav colors and indicator
        for k, btn in self.nav_buttons.items():
            if k == name:
                btn.color = (0.16, 0.42, 1, 1)
                btn.bold = True
                # Move indicator under this button
                target_x = btn.x + (btn.width - self.nav_indicator.width)/2
                anim = Animation(x=target_x, duration=0.32, t='out_expo')
                anim.start(self.nav_indicator)
            else:
                btn.color = (0.58,0.63,0.72,1)
                btn.bold = False

    def show_game_profile(self, package):
        print(f"Show profile for {package}")

    def on_pause(self):
        return True
    def on_resume(self):
        pass

if __name__ == '__main__':
    SneeryBoosterApp().run()
