#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton 
from kivy.uix.slider import Slider
from kivy.uix.label import Label
import urllib
import time
import threading
import socket
# from sshtunnel import SSHTunnelForwarder
socket.setdefaulttimeout(5)
# from flask import requests
server = "http://192.168.2.9:5000/"
outdoor = False

 # app_ref =  App.get_running_app()#Label.color = [0,1,0,0.5]
 #                app_ref.root.children[3].color

try:
	print urllib.urlopen(server).getcode()
except IOError:
	server = "http://localhost:5000"

def sendTemp(temp, app_ref):
    print "sending temp: ", temp
    auth_data = {'temp': temp}
    auth_data = urllib.urlencode(auth_data)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    UrlRequest(
        url=server+"set",
        req_body=auth_data,
        req_headers=headers,
    ).wait()
    temp =  float(urllib.urlopen(server+"temp").read())
    app_ref.root.children[3].color = getColor(temp)
    if temp > 16:
        app_ref.root.children[1].state ='down'
        app_ref.root.children[0].state = 'normal'
    else:
        app_ref.root.children[0].state = 'down'
        app_ref.root.children[1].state = 'normal'

def getColor(temp, setTemp=18.0, maxTemp = 21.0, minTemp=15.0):
    if temp < setTemp:
        r = 0
    elif temp > maxTemp:
        r = 1 
    else:
        r = (temp-setTemp)/(maxTemp-setTemp)

    if temp <= setTemp and temp > minTemp:
        g = 1 - (setTemp-temp)/(setTemp-minTemp)
    elif temp > setTemp and temp < maxTemp:
        g = 1 - (temp-setTemp)/(maxTemp-setTemp)
    else:
        g = 0

    if temp > setTemp:
        b = 0
    elif temp < minTemp:
        b = 1
    else:
        b = (setTemp-temp)/(setTemp-minTemp)
    print(r,g,b)
    return [r,g,b,1]

class mySlider(Slider):
    


    def on_touch_up(self, touch):
            released = super(mySlider, self).on_touch_up(touch)
            if released:
                app_ref =  App.get_running_app()#Label.color = [0,1,0,0.5]
                app_ref.root.children[3].color = [1,1,1,1]           
                threading.Thread(target = sendTemp, args = [self.value, app_ref]).start()
      
                return True
            else:
                return False

class MyApp(App):

    def sendTemp(self, temp):
        print "sending temp: ", temp
        auth_data = {'temp': temp}
        auth_data = urllib.urlencode(auth_data)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        UrlRequest(
            url=server+"set",
            req_body=auth_data,
            req_headers=headers,
        ).wait()
        self.getTemp()

    def getTemp(self):
        temp =  float(urllib.urlopen(server+"temp").read())
        self.Label.color = getColor(temp)
        self.Slider.value = temp
        if temp > 15:
            self.ButtonOn.state ='down'
            self.ButtonOff.state = 'normal'
        else:
            self.ButtonOff.state = 'down'
            self.ButtonOn.state = 'normal'
        return temp

    def build(self):



        self.Slider = mySlider(min = 14, max = 24, orientation = 'vertical', step=0.5, padding='40sp')
        self.Label = Label(text=str(self.Slider.value), font_size='40sp', size_hint_y=2)
        
        def changeLabel(instance, value):
            self.Label.text = str(value)
            self.Label.color = getColor(value)
        self.Slider.bind(value=changeLabel)
        # def colorLabel(instance, value):
            
        # self.Slider.bind(on_touch_down=colorLabel)
        def On(state):
            if self.ButtonOn.state=='down':
                self.Label.color = [1,1,1,1]
                threading.Thread(target = self.sendTemp, args = ["On"]).start()
            elif self.ButtonOff.state=='normal' :
                self.ButtonOn.state ='down'
        def Off(event):

            if self.ButtonOff.state=='down':
                self.Label.color = [1,1,1,1]
                threading.Thread(target = self.sendTemp, args = ["Off"]).start()
            elif self.ButtonOn.state=='normal' :
                self.ButtonOff.state ='down'
        self.ButtonOn = ToggleButton(text='On', group='onoff' , font_size='30sp', size_hint_y=0.5)
        self.ButtonOn.bind(on_release=On)
        self.ButtonOff = ToggleButton(text='Off', group='onoff', font_size='30sp' )
        self.ButtonOff.bind(on_release=Off)
        layout = GridLayout(cols=2, rows=2, )
        layout.add_widget(self.Label)
        layout.add_widget(self.Slider)
        layout.add_widget(self.ButtonOn)
        layout.add_widget(self.ButtonOff)
        self.Slider.value = self.getTemp()
        return layout



        

MyApp().run()


# class MainLayout(GridLayout):

#     count = 1

#     def send_message(self, message):
#         POST_data = self._prepare_data(message)
#         self._send_message(POST_data)

#     def _prepare_data(self, message):
#         auth_data = {'message': message}
#         auth_data = urllib.parse.urlencode(auth_data)
#         headers = {
#             'Content-type': 'application/x-www-form-urlencoded',
#             'Accept': 'application/json'
#         }
#         return {'auth_data': auth_data, 'headers': headers}

#     def _send_message(self, POST_data):
#         UrlRequest(
#             url='http://localhost:5000/',
#             req_body=POST_data['auth_data'],
#             req_headers=POST_data['headers'],
#             on_failure=self._on_connection_failure,
#             on_error=self._on_connection_error,
#             on_success=self._on_connection_success,
#         )

#     def _on_connection_success(self, request, result):
#         self.ids.status_label.text =\
#             'message %s delivered' % self.count
#         self.count += 1

#     def _on_connection_failure(self, request, result):
#         self.ids.status_label.text = 'connection fail'

#     def _on_connection_error(self, request, result):
#         self.ids.status_label.text = 'connection error'


# class Test(App):
#     pass


# Test().run()