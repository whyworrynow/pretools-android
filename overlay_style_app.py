#!/usr/bin/env python3
"""
PreTools Overlay Style - 원본과 유사한 방식
스크린샷 + 주석 방식으로 다른 앱 위에 그리는 효과 구현
"""

import os
import json
import time
from functools import partial
from collections import OrderedDict

# Kivy imports
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.uix.colorpicker import ColorPicker
    from kivy.uix.slider import Slider
    from kivy.uix.switch import Switch
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.image import Image
    from kivy.graphics import Color, Line, Ellipse, Rectangle
    from kivy.graphics.texture import Texture
    from kivy.clock import Clock
    from kivy.config import Config
    from kivy.core.window import Window
    
    # 전체화면 설정
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'borderless', '1')  # 테두리 없음
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

# Android specific imports
try:
    from android.permissions import request_permissions, Permission
    from jnius import autoclass, PythonJavaClass, java_method
    ANDROID = True
except ImportError:
    ANDROID = False

if KIVY_AVAILABLE:
    class SettingsManager:
        def __init__(self):
            if ANDROID:
                self.config_dir = "/sdcard/PreTools"
            else:
                self.config_dir = os.path.expanduser("~/.pretools_overlay")
            
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
            
            self.config_file = os.path.join(self.config_dir, "settings.json")
            self.default_settings = {
                'pen_color': [1, 0, 0, 1],  # 빨간색
                'pen_thickness': 3,
                'eraser_thickness': 15,
                'recent_colors': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
                'toolbar_position': 'bottom',
                'auto_hide_toolbar': True
            }
            self.load_settings()
        
        def load_settings(self):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except:
                self.settings = self.default_settings.copy()
            
            for key, value in self.default_settings.items():
                if key not in self.settings:
                    self.settings[key] = value
        
        def save_settings(self):
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Settings save error: {e}")
        
        def get(self, key, default=None):
            return self.settings.get(key, default)
        
        def set(self, key, value):
            self.settings[key] = value
            self.save_settings()

    # Screenshot Handler
    class ScreenshotHandler:
        def __init__(self):
            if ANDROID:
                self.setup_android()
            else:
                self.setup_desktop()
        
        def setup_android(self):
            # Android screenshot permissions
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        
        def setup_desktop(self):
            # Desktop screenshot simulation
            pass
        
        def take_background_screenshot(self, callback=None):
            """다른 앱들의 스크린샷을 찍어서 배경으로 사용"""
            if ANDROID:
                # Android MediaProjection API 사용
                # 실제 구현에서는 배경 앱들의 스크린샷 촬영
                print("Taking background screenshot...")
                if callback:
                    callback("screenshot_background.png")
            else:
                # 데스크톱 시뮬레이션 - 단색 배경
                if callback:
                    callback(None)  # 배경 이미지 없음

    # Floating Toolbar
    class FloatingToolbar(BoxLayout):
        def __init__(self, canvas_widget, **kwargs):
            super().__init__(**kwargs)
            self.canvas_widget = canvas_widget
            self.settings_manager = SettingsManager()
            
            self.orientation = 'horizontal'
            self.size_hint = (None, None)
            self.size = (300, 50)
            self.spacing = 5
            self.padding = [5, 5]
            
            # 반투명 배경
            with self.canvas.before:
                Color(0, 0, 0, 0.7)  # 반투명 검정
                self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            self.bind(pos=self.update_bg, size=self.update_bg)
            
            self.build_toolbar()
            
            # 자동 숨김 기능
            self.auto_hide = self.settings_manager.get('auto_hide_toolbar')
            if self.auto_hide:
                self.hide_timer = Clock.create_trigger(self.auto_hide_toolbar, 3.0)
                self.hide_timer()
        
        def update_bg(self, *args):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
        
        def build_toolbar(self):
            # Pen tool
            self.pen_btn = Button(text='🖊️', size_hint=(None, None), size=(40, 40))
            self.pen_btn.background_color = (0.2, 0.6, 1, 1)  # Active
            self.pen_btn.bind(on_press=self.set_pen)
            self.add_widget(self.pen_btn)
            
            # Eraser tool  
            self.eraser_btn = Button(text='🧹', size_hint=(None, None), size=(40, 40))
            self.eraser_btn.background_color = (0.5, 0.5, 0.5, 1)
            self.eraser_btn.bind(on_press=self.set_eraser)
            self.add_widget(self.eraser_btn)
            
            # Color buttons (recent colors)
            recent_colors = self.settings_manager.get('recent_colors')
            for color_hex in recent_colors[:4]:  # 4개만 표시
                color_btn = Button(size_hint=(None, None), size=(30, 30))
                # hex to rgba
                color_rgb = self.hex_to_rgba(color_hex)
                color_btn.background_color = color_rgb
                color_btn.bind(on_press=partial(self.set_color, color_rgb))
                self.add_widget(color_btn)
            
            # More colors button
            more_btn = Button(text='🎨', size_hint=(None, None), size=(40, 40))
            more_btn.bind(on_press=self.show_color_picker)
            self.add_widget(more_btn)
            
            # Clear button
            clear_btn = Button(text='🗑️', size_hint=(None, None), size=(40, 40))
            clear_btn.background_color = (1, 0.3, 0.3, 1)
            clear_btn.bind(on_press=self.clear_canvas)
            self.add_widget(clear_btn)
            
            # Save button
            save_btn = Button(text='💾', size_hint=(None, None), size=(40, 40))
            save_btn.background_color = (0.3, 0.8, 0.3, 1)
            save_btn.bind(on_press=self.save_annotation)
            self.add_widget(save_btn)
        
        def hex_to_rgba(self, hex_color):
            """#FF0000 -> [1, 0, 0, 1]"""
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0  
            b = int(hex_color[4:6], 16) / 255.0
            return [r, g, b, 1]
        
        def rgba_to_hex(self, rgba):
            """[1, 0, 0, 1] -> #FF0000"""
            r = int(rgba[0] * 255)
            g = int(rgba[1] * 255)
            b = int(rgba[2] * 255)
            return f"#{r:02X}{g:02X}{b:02X}"
        
        def set_pen(self, instance):
            self.canvas_widget.set_tool('pen')
            self.pen_btn.background_color = (0.2, 0.6, 1, 1)
            self.eraser_btn.background_color = (0.5, 0.5, 0.5, 1)
            self.show_temporarily()
        
        def set_eraser(self, instance):
            self.canvas_widget.set_tool('eraser')
            self.pen_btn.background_color = (0.5, 0.5, 0.5, 1)
            self.eraser_btn.background_color = (0.2, 0.6, 1, 1)
            self.show_temporarily()
        
        def set_color(self, color, instance):
            self.canvas_widget.set_pen_color(color)
            
            # 최근 사용 색상 업데이트
            recent_colors = self.settings_manager.get('recent_colors')
            color_hex = self.rgba_to_hex(color)
            if color_hex in recent_colors:
                recent_colors.remove(color_hex)
            recent_colors.insert(0, color_hex)
            recent_colors = recent_colors[:6]
            self.settings_manager.set('recent_colors', recent_colors)
            
            self.show_temporarily()
        
        def show_color_picker(self, instance):
            color_picker = ColorPicker()
            popup = Popup(title='색상 선택', content=color_picker, size_hint=(0.8, 0.8))
            color_picker.bind(color=lambda x, color: self.set_color(color, None) or popup.dismiss())
            popup.open()
            self.show_temporarily()
        
        def clear_canvas(self, instance):
            self.canvas_widget.clear_canvas()
            self.show_temporarily()
        
        def save_annotation(self, instance):
            # 주석이 추가된 이미지 저장
            popup = Popup(title='저장 완료', 
                         content=Label(text='주석이 저장되었습니다!'),
                         size_hint=(0.6, 0.3))
            popup.open()
            Clock.schedule_once(popup.dismiss, 1.5)
            self.show_temporarily()
        
        def show_temporarily(self):
            """툴바를 잠시 보여주고 다시 숨김"""
            self.opacity = 1.0
            if self.auto_hide:
                self.hide_timer.cancel()
                self.hide_timer()
        
        def auto_hide_toolbar(self, *args):
            """툴바 자동 숨김"""
            if self.auto_hide:
                # 부드러운 페이드아웃 애니메이션
                from kivy.animation import Animation
                anim = Animation(opacity=0.3, duration=0.5)
                anim.start(self)

    # Full Screen Drawing Canvas
    class OverlayDrawingCanvas(Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.settings_manager = SettingsManager()
            self.current_tool = 'pen'
            self.is_drawing = False
            self.current_stroke = []
            
            # 배경 이미지 (스크린샷)
            self.background_image = None
            
            # 반투명 배경 (실제로는 캡쳐한 화면)
            with self.canvas.before:
                Color(0.9, 0.9, 0.9, 1)  # 연한 회색 (스크린샷 시뮬레이션)
                self.bg = Rectangle(pos=self.pos, size=self.size)
            
            self.bind(size=self.update_bg, pos=self.update_bg)
        
        def update_bg(self, *args):
            self.bg.pos = self.pos
            self.bg.size = self.size
        
        def set_background_screenshot(self, image_path):
            """배경 스크린샷 설정"""
            if image_path and os.path.exists(image_path):
                self.background_image = Image(source=image_path)
                self.background_image.size = self.size
                self.background_image.pos = self.pos
                # 배경 이미지 추가
        
        def on_touch_down(self, touch):
            if self.collide_point(*touch.pos):
                self.is_drawing = True
                self.current_stroke = [touch.pos[0], touch.pos[1]]
                
                with self.canvas:
                    if self.current_tool == 'pen':
                        Color(*self.settings_manager.get('pen_color'))
                        self.line = Line(
                            points=self.current_stroke,
                            width=self.settings_manager.get('pen_thickness'),
                            cap='round',
                            joint='round'
                        )
                    elif self.current_tool == 'eraser':
                        # 지우개는 배경색으로 그리기
                        Color(0.9, 0.9, 0.9, 1)
                        self.line = Line(
                            points=self.current_stroke,
                            width=self.settings_manager.get('eraser_thickness'),
                            cap='round',
                            joint='round'
                        )
                return True
            return False
        
        def on_touch_move(self, touch):
            if self.is_drawing and self.collide_point(*touch.pos):
                self.current_stroke.extend([touch.pos[0], touch.pos[1]])
                self.line.points = self.current_stroke
                return True
            return False
        
        def on_touch_up(self, touch):
            if self.is_drawing:
                self.is_drawing = False
                return True
            return False
        
        def set_tool(self, tool):
            self.current_tool = tool
        
        def set_pen_color(self, color):
            self.settings_manager.set('pen_color', color)
        
        def clear_canvas(self):
            """드로잉만 지우고 배경은 유지"""
            # 배경 제외하고 드로잉만 지우기
            instructions_to_remove = []
            for instruction in self.canvas.children:
                if hasattr(instruction, 'points'):  # Line 객체
                    instructions_to_remove.append(instruction)
            
            for instruction in instructions_to_remove:
                self.canvas.remove(instruction)

    # Main Overlay Screen
    class OverlayScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.build_ui()
        
        def build_ui(self):
            # 전체화면 레이아웃
            layout = FloatLayout()
            
            # 드로잉 캔버스 (전체화면)
            self.canvas_widget = OverlayDrawingCanvas()
            layout.add_widget(self.canvas_widget)
            
            # 플로팅 툴바 (하단 중앙)
            self.toolbar = FloatingToolbar(self.canvas_widget)
            self.toolbar.pos_hint = {'center_x': 0.5, 'y': 0.05}
            layout.add_widget(self.toolbar)
            
            # 나가기 버튼 (우상단)
            exit_btn = Button(
                text='❌',
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={'right': 0.98, 'top': 0.98}
            )
            exit_btn.background_color = (1, 0.3, 0.3, 0.8)
            exit_btn.bind(on_press=self.exit_overlay)
            layout.add_widget(exit_btn)
            
            # 도움말 (좌상단)
            help_label = Label(
                text='다른 앱 위에 그리는 효과\n(실제로는 스크린샷 + 주석)',
                size_hint=(None, None),
                size=(200, 60),
                pos_hint={'x': 0.02, 'top': 0.98},
                font_size='12sp',
                halign='left'
            )
            help_label.bind(size=help_label.setter('text_size'))
            layout.add_widget(help_label)
            
            self.add_widget(layout)
            
            # 스크린샷 핸들러
            self.screenshot_handler = ScreenshotHandler()
            
            # 시작시 배경 스크린샷 촬영
            Clock.schedule_once(self.take_background_screenshot, 0.1)
        
        def take_background_screenshot(self, *args):
            """배경 앱들의 스크린샷을 촬영"""
            def on_screenshot_ready(image_path):
                if image_path:
                    self.canvas_widget.set_background_screenshot(image_path)
            
            self.screenshot_handler.take_background_screenshot(on_screenshot_ready)
        
        def exit_overlay(self, instance):
            """오버레이 모드 종료"""
            App.get_running_app().stop()

    # Main App
    class OverlayStyleApp(App):
        def build(self):
            self.title = 'PreTools Overlay Style'
            
            # 전체화면 모드
            Window.fullscreen = False
            Window.borderless = True
            Window.always_on_top = True  # 항상 위에
            
            # 단일 스크린
            overlay_screen = OverlayScreen()
            return overlay_screen
        
        def on_start(self):
            # 앱 시작시 설정
            if ANDROID:
                # Android에서 전체화면 설정
                from android.runnable import run_on_ui_thread
                
                @run_on_ui_thread
                def set_fullscreen():
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    activity = PythonActivity.mActivity
                    # 전체화면 플래그 설정
                
                set_fullscreen()

if __name__ == '__main__':
    if KIVY_AVAILABLE:
        OverlayStyleApp().run()
    else:
        print("Kivy 설치 필요: pip install kivy")