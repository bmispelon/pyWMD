#!/usr/bin/env python
#-*- coding:utf-8 -*-

from base import MissileControlUI

class SimpleTextUI(MissileControlUI):
    def help(self):
        print "Here are the instructions that you can give:"
        print "    * `go X`: moves to the X direction (up, down, left, right)"
        print "    * `fire`: fires one missile"
        print "    * `stop`: stops the device (only useful if it is still moving)"
        print "    * `exit`: exits this program"
        print "    * `help`: shows this message"
    
    
    def run(self):
        print "Welcome to the Missile control center. Type help then press Enter to get help."
        while True:
            input = raw_input('>')
            
            instructions = input.lower().split(' ')
            action = instructions.pop(0)
            
            if     action == 'fire': self.dev.fire()
            elif   action == 'fire!!!': self.dev.fire_all()
            elif   action == 'stop': self.dev.stop()
            elif   action == 'help': self.help()
            elif   action == 'exit': break
            elif action == 'go' and instructions: self.dev.move(instructions[0])
            else: print "I don't understand..."
        
        self.dev = None
        print "Good Bike !"
