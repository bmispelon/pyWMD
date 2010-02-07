#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from base import MissileControlUI

class MyFrame(wx.Frame):
    def __init__(self, device, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.button_upleft = wx.Button(self, -1, u"↖")
        self.button_up = wx.Button(self, -1, u"↑")
        self.button_upright = wx.Button(self, -1, u"↗")
        self.button_left = wx.Button(self, -1, u"←")
        self.button_center = wx.Button(self, wx.ID_STOP, "")
        self.button_right = wx.Button(self, -1, u"→")
        self.button_downleft = wx.Button(self, -1, u"↙")
        self.button_down = wx.Button(self, -1, u"↓")
        self.button_downright = wx.Button(self, -1, u"↘")
        self.fire_button = wx.Button(self, -1, "FIRE")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.cb_fire, self.fire_button)
        self.Bind(wx.EVT_BUTTON, self.cb_stop, self.button_center)
        self.Bind(wx.EVT_BUTTON, self.cb_move('up'), self.button_up)
        self.Bind(wx.EVT_BUTTON, self.cb_move('down'), self.button_down)
        self.Bind(wx.EVT_BUTTON, self.cb_move('left'), self.button_left)
        self.Bind(wx.EVT_BUTTON, self.cb_move('right'), self.button_right)
        self.Bind(wx.EVT_BUTTON, self.cb_move('upright'), self.button_upright)
        self.Bind(wx.EVT_BUTTON, self.cb_move('downright'), self.button_downright)
        self.Bind(wx.EVT_BUTTON, self.cb_move('upleft'), self.button_upleft)
        self.Bind(wx.EVT_BUTTON, self.cb_move('downleft'), self.button_downleft)
        
        self.dev = device

    def __set_properties(self):
        from os.path import dirname
        icon_path = dirname(dirname(__file__))
        self.SetTitle("Weapon of Mousse Destruction")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(icon_path + "/icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        direction_controls = wx.GridSizer(3, 3, 0, 0)
        direction_controls.Add(self.button_upleft, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_up, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_upright, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_left, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_center, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_right, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_downleft, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_down, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        direction_controls.Add(self.button_downright, 0, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(direction_controls, 5, wx.EXPAND, 0)
        sizer_2.Add(self.fire_button, 2, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

    def cb_fire(self, event):
        self.dev.fire()
    
    def cb_stop(self, event):
        self.dev.stop()
    
    def cb_move(self, dir):
        return lambda e: self.dev.move(dir)


class SimpleGUI(MissileControlUI):
    def run(self):
        wxApp = wx.App(0)
        wx.InitAllImageHandlers()
        frame = MyFrame(self.dev, None, -1, "")
        wxApp.SetTopWindow(frame)
        frame.Show()
        
        wxApp.MainLoop()
