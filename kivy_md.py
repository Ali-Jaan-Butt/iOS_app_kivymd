from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.menu import MDDropdownMenu
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import json

class StartScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class DoctorsList(Screen):
    pass

class SecondList(Screen):
    pass

class ThirdList(Screen):
    pass

class FourthList(Screen):
    pass

class BookScreen(Screen):
    pass

class MyApp(MDApp):
    cred = credentials.Certificate("doctors-72cd1-firebase-adminsdk-pf7qv-7ca42b4bcf.json")
    firebase_admin.initialize_app(cred, {'databaseURL':'https://doctors-72cd1-default-rtdb.firebaseio.com'})
    ref = db.reference('/')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
    def build(self):
        return Builder.load_file('main.kv')

    def create_patch(self, namee, email, passw, age, gender_field):
        data = {'name':namee, 'email':email, 'password':passw, 'age':age, 'gender':gender_field}
        if data['name']=='' or data['email']=='' or data['password']=='' or data['age']=='' or data['gender']=='':
            return
        else:
            new_data_ref = self.ref.push(data)
            app = MDApp.get_running_app()
            app.change_screen('login_screen')
        
    def get_sign(self, email, password):
        data = self.ref.get()
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.error_label.text = "Invalid username or password"
        popup = Popup(title='Login Error', content=self.error_label, size_hint=(None, None), size=(400, 200))
        x = 1
        for i in data:
            if data[i]['email']==email and data[i]['password']==password:
                app = MDApp.get_running_app()
                app.change_screen('home_screen')
                x+=1
                break
            else:
                popup = popup
        if x==1:
            popup.open()
        else:
            pass
    
    def change_screen(self, screen):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen
    
    def show_gender_menu(self, instance, value):
        if value:
            menu_items = [
                {"text": "Male", "viewclass": "OneLineListItem", "on_release": lambda x="Male": self.set_gender(x)},
                {"text": "Female", "viewclass": "OneLineListItem", "on_release": lambda x="Female": self.set_gender(x)}
            ]
            self.menu = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=4,
            )
            self.menu.open()

    def set_gender(self, text_item):
        self.menu.dismiss()
        gender_field = self.root.ids.signup_screen.ids.gender_field
        gender_field.text = text_item
        print(gender_field.text)


if __name__ == '__main__':
    MyApp().run()
