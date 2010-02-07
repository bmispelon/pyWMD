#!/usr/bin/env python
#-*- coding:utf-8 -*-

from base import MissileControlUI

class SimpleNumpadUI(MissileControlUI):
    def help(self):
        print "Use your numeric keypad to move the device."
        print "Enter a digit between 1 and 9 and press Enter."
        print "To fire a missile, enter the number 42."
        print "To leave the program, leave the line blank and press Enter."
    
    def run(self):
        self.help()
        while True:
            input = raw_input('Direction :')
            if not input: break
            try: input = int(input)
            except ValueError: print 'Try again...'
            else: self.move_by_number(input)
        self.exit()
    
    def move_by_number(self, n):
        """Use numbers on a numeric keypad to move the device."""
        if n == 5: self.dev.stop()
        elif n in range(1, 10): self.dev.move(n)
        elif n == 42: self.dev.fire()
        else: print '%s is not a valid direction' % n
    
    def exit(self):
        self.dev = None
        print "Good Bike !"
