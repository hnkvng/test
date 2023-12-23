from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import DictProperty,StringProperty,ListProperty, BooleanProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.list import OneLineAvatarListItem,ImageLeftWidget
from kivy.uix.scrollview import ScrollView
import re
from tinydb import Query, TinyDB
from datetime import datetime

DATA = "../db/database.json"
#init database
class initDataBase():
    def connect(self):
        return TinyDB(DATA)
    def query(self):
        return Query() 
        
screen_width = 1080  # Ví dụ: Full HD (1080x1920 pixels)
screen_height = 1920

# Đặt kích thước cửa sổ ứng dụng với mật độ và kích thước của màn hình
Window.size = (screen_width / 3.0, screen_height / 3.0)



class Main(Screen):
    pass
#main

class Home(Widget):
    pass
#home
def initDict(value):
    return { 
        'MSSP': value,
        'Name': value,
        'Des': value,
        'Quantity': value,
        'DVT': value,
        'Buy': value,
        'Sell': value,
        'NSX': value,
        'HSD': value,
    }


class FormInput(Screen):
    listTarget = ListProperty([
        {
            'name':'MSSP',
            'log':'Nhập mã số sản phẩm',
        },
        {
            'name':'Name',
            'log':'Nhập tên sản phẩm'
        },
        {
            'name': 'Des',
            'log':'Nhập mô tả sản phẩm'
        },
        {
            'name': 'Quantity',
            'log':'Nhập số lượng sản phẩm mua',
            'test': lambda text: re.compile(r'[^0-9]').search(text),
            'error': "không được tồn tại chữ hoặc chữ cái đặc biệt"
        },
        {
            'name': 'DVT',
            'log':'Nhập đơn vị tính sản phẩm',
            'test': lambda text: re.compile(r'[^a-zA-Z]').search(text),
            'error': "không được tồn tại số hoặc chữ cái đặc biệt"
        },
        {
            'name': 'Buy',
            'log':'Nhập giá mua sản phẩm',
            'test': lambda text: re.compile(r'[^.\w]').search(text),
        },
        {
            'name': 'Sell',
            'log':'Nhập giá bán sản phẩm',
            'test': lambda text: re.compile(r'[^.\w]').search(text),
        },
        {
            'name': 'NSX',
            'log':'Nhập ngày sản xuất sản phẩm',
            'test': lambda text: re.compile(r'[^/\w]').search(text),
        },
        {
            'name': 'HSD',
            'log':'Nhập hạn sử dụng sản phẩm',
            'test': lambda text: re.compile(r'[^/\w]').search(text),
        },
    ])

    dataForm = DictProperty()
    message = DictProperty(initDict(''))  
    error = DictProperty(initDict(False))
    submit = BooleanProperty(False)
 
    def hanleChange(self, instance, name, text):
        self.dataForm.update({
            name:text
        })   
        self.handleData(instance, name, text)

    def handleSubmit(self):
        for key in self.error:
            if(self.error[key] == True):
                return
        self.dataForm.update({
            'creatAtTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        with initDataBase().connect() as base:
            base.table('Product').insert(self.dataForm)

    def handleData(self, instance, name, text): 
        if(self.checkNull(name, text) and self.checkLen(instance, name, text)):
            self.checkException(name,text)    
            
    def handleFocus(self, name, focus):
        if(focus):
            for target in self.listTarget:
                if(target['name'] == name):
                    self.message[name] = target['log']
        else:
            self.message[name] = ''

    def checkNull(self, name, text):
        if(len(text) == 0 and name != 'Des'):
            self.message[name] = "Không được để trống"
            self.error[name] = True
            return False
        self.message[name] = ''
        self.error[name] = False
        return True
    
    def checkLen(self, instance, name, text):
        if(len(text) > instance.max_text_length):
            self.message[name] = "Vượt quá độ dài cho phép"
            self.error[name] = True
            return False
        self.message[name] = ""
        self.error[name] = False
        return True

    def checkException(self, name, text):
        check = lambda check: re.compile(r'[!@#$%^&*(),.?":{}|<>]').search(check)
        listExcept = ['Des','Buy','Sell','NSX','HSD','DVT','Quantity']
        try:
            listExcept.index(name)
            for target in self.listTarget:
                if(target['name'] == name and name != 'Des'): 
                    if((name == 'NSX' or name == 'HSD')):
                        data = text.split('/')
                        try:
                            datetime(int(data[2]),int(data[1]), int(data[0]))
                            self.message[name] = ""
                            self.error[name] = False
                            return
                        except:
                            self.message[name] = "Ngày tháng năm không hợp lệ"
                            self.error[name] = True
                            return
                    if(target['test'](text)):
                        if(name == 'DVT' or name == 'Quantity'):
                            self.message[name] = target['error']
                            self.error[name] = True
                            return
                        
                        self.message[name] = "Không được tồn tại chữ cái đặc biệt"
                        self.error[name] = True
                        return
                
            self.message[name] = ""
            self.error[name] = False             
            return 
        except:
            if(check(text)):
                self.message[name] = "Không được có chữ cái đặc biệt"
                self.error[name] = True
                return
            self.message[name] = '' 
            self.error[name] = False
        

#forminut

class Medicien(ScrollView):
    dataCurrent = ListProperty(None)
    def getDataFromDataBase(self):
        with initDataBase().connect() as base:
            if(self.dataCurrent != base.table('Product').all() or self.dataCurrent is None):     
                self.dataCurrent = base.table('Product').all()
                self.uploadUI(self.dataCurrent)
    
    def uploadUI(self, data):
        md_list = self.children[0]
        md_list.clear_widgets()
        for item in data:
            try:
                list_item = OneLineAvatarListItem(text=item['Name'])
                list_item.add_widget(ImageLeftWidget(source='../img/medicine.jpg'))
                md_list.add_widget(list_item)
            except:
                print("error")

                
class NSXTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty() 
    def ShowDateSelect(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.handleSave)
        date_dialog.open()
    def handleSave(self, instance, value ,data_range):
        date = str(value).split("-")
        self.children[1].text = "/".join(list(reversed(date)))

       
class HSDTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()  

    def ShowDateSelect(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.handleSave)
        date_dialog.open()
    def handleSave(self, instance, value ,data_range):
        date = str(value).split("-")
        self.children[1].text = "/".join(list(reversed(date)))

#medicien
            
class Mandates (Widget):
    data = DictProperty()
    def __init__(self, **kwargs):
        super(Mandates, self).__init__(**kwargs)
        self.data = {
            'Thêm': [
                'plus-circle',
                "on_release", lambda add: MyApp().switchScreen('forminput'),
            ],
            'Xóa': [
                'delete',
                "on_press", lambda delete: print("Xóa"),
            ],
            'Chỉnh sửa': [
                'pencil',
                "on_press", lambda change: print("Sửa"),
            ],
            'Cập nhật': [
                'file-arrow-up-down-outline',
                "on_press", lambda change: print("Cập nhật"),
            ],
        }
#Options


class History(Widget):
    pass

class User(Widget):
    pass

Builder.load_file("main.kv")
Builder.load_file("formAdd.kv")

class MyApp(MDApp):
    sm = ScreenManager()
    def build(self):
        self.title = "Manager Medicine"
        self.icon = "../img/doctor.jpg"
        self.sm.add_widget(Main(name='main'))
        self.sm.add_widget(FormInput(name='forminput'))
        return self.sm
    def switchScreen(self, screen_name):
        self.sm.current = screen_name
        self.sm.transition.direction = 'left'
    def comeBack(self, screen_name):
        self.sm.current = screen_name
        self.sm.transition.direction = 'right'

if __name__ == "__main__":
    MyApp().run()





