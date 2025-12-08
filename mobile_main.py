from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.icon_definitions import md_icons
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window

import cv2
import requests
import base64
import threading
import pyttsx3

# Configuration
SERVER_URL = "http://127.0.0.1:5000/analyze" # Change to 192.168.x.x for real mobile
Window.size = (360, 640) # Simulate Mobile Screen

class LuminaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        
        # Main Screen
        screen = MDScreen()
        
        # Layout
        layout = MDBoxLayout(orientation='vertical', spacing="10dp", padding="20dp")
        
        # Toolbar
        toolbar = MDTopAppBar(title="Lumina Vision", elevation=2)
        toolbar.right_action_items = [["dots-vertical", lambda x: print("Settings")]]
        # MDTopAppBar must be added to a container that handles it, usually at top
        # For simple BoxLayout, we just add it first.
        
        # To make layout correct with Toolbar at top
        root_box = MDBoxLayout(orientation='vertical')
        root_box.add_widget(toolbar)
        
        # Content Box
        content_box = MDBoxLayout(orientation='vertical', spacing="20dp", padding="20dp")
        
        # Camera Feed (using OpenCV)
        # Using a layout to constrain size if needed, but Image usually fits
        self.image = Image(allow_stretch=True, keep_ratio=True)
        content_box.add_widget(self.image)
        
        # Result Card
        self.result_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="80dp",
            padding="15dp",
            radius=[12],
            elevation=1
        )
        self.result_label = MDLabel(
            text="Ready to scan...",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        self.result_card.add_widget(self.result_label)
        content_box.add_widget(self.result_card)
        
        # Controls (Rectangular Buttons)
        controls = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height="60dp",
            spacing="20dp",
            adaptive_size=False
        ) # Removed padding to align with parent
        
        # Spacer to center buttons if needed, or just use spacing
        controls.add_widget(MDLabel(size_hint_x=1)) # Flexible spacer
        
        btn_detect = MDFillRoundFlatIconButton(
            icon="eye-outline",
            text="Identify",
            font_size="16sp",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(None, None),
            width="130dp",
            height="44dp"
        )
        btn_detect.bind(on_release=lambda x: self.analyze("detect"))
        
        btn_read = MDFillRoundFlatIconButton(
            icon="text",
            text="Read Text",
            font_size="16sp",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(None, None),
            width="130dp",
            height="44dp"
        )
        btn_read.bind(on_release=lambda x: self.analyze("read"))
        
        controls.add_widget(btn_detect)
        controls.add_widget(btn_read)
        controls.add_widget(MDLabel(size_hint_x=1)) # Flexible spacer
        
        content_box.add_widget(controls)
        root_box.add_widget(content_box)
        screen.add_widget(root_box)
        
        # Setup Camera
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
             print("ERROR: Could not open camera.")
             self.result_label.text = "Camera Error! Check connection."
        
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
        
        # Setup TTS
        self.engine = pyttsx3.init()
        
        return screen

    def update_frame(self, dt):
        try:
            ret, frame = self.capture.read()
            if ret:
                # Flip and buffer
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture
                self.current_frame = frame
        except Exception as e:
            print(f"Frame error: {e}")

    def analyze(self, mode):
        self.result_label.text = "Analyzing..."
        threading.Thread(target=self._send_request, args=(mode,)).start()

    def _send_request(self, mode):
        try:
            # Enhance frame for sending (convert to jpg base64)
            ret, buffer = cv2.imencode('.jpg', self.current_frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            img_data = f"data:image/jpeg;base64,{jpg_as_text}"
            
            response = requests.post(SERVER_URL, json={"image": img_data, "mode": mode})
            if response.status_code == 200:
                result = response.json().get("result", "No result")
                Clock.schedule_once(lambda x: self._update_ui(result))
                self._speak(result)
            else:
                Clock.schedule_once(lambda x: self._update_ui("Server Error"))
        except Exception as e:
            Clock.schedule_once(lambda x: self._update_ui(f"Connection Error: {e}"))

    def _update_ui(self, text):
        self.result_label.text = text

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    LuminaApp().run()
