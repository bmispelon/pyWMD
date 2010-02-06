#!/usr/bin/env python
#-*- coding:utf-8 -*-
import usb

class DeviceNotFoundError(Exception): pass

class MissileDevice:
    VENDOR_ID = 0x1130
    PRODUCT_ID = 0x0202
    
    MISSILE_BAY_SIZE = 3
    
    h_amp = 4 # ie 6 horizontal movements cover the whole range
    v_amp = 2 # ie 4 vertical movements cover the whole range

    INITA     = (85, 83, 66, 67,  0,  0,  4,  0)
    INITB     = (85, 83, 66, 67,  0, 64,  2,  0)

    STOP      = ( 0,  0,  0,  0,  0,  0)
    LEFT      = ( 0,  1,  0,  0,  0,  0)
    RIGHT     = ( 0,  0,  1,  0,  0,  0)
    UP        = ( 0,  0,  0,  1,  0,  0)
    DOWN      = ( 0,  0,  0,  0,  1,  0)
    LEFTUP    = LEFT + UP
    RIGHTUP   = RIGHT + UP
    LEFTDOWN  = LEFT + DOWN
    RIGHTDOWN = RIGHT + DOWN
    FIRE      = ( 0,  0,  0,  0,  0,  1)
    
    dev = None
    handle = None

    def __init__(self):
        """Attempts to find and open the missile device.
        If the device is not found, a DeviceNotFoundError is raised"""
        self.dev = self._find_device()
        if self.dev is None: raise DeviceNotFoundError()
        self._open_device()
     
    def _find_device(self):
        """Finds the device corresponding to the VENDOR_ID and PRODUCT_ID.
        Returns the device object if found, None otherwise."""
        from itertools import chain
        
        for dev in chain(*[b.devices for b in usb.busses()): # flattens the list
            if dev.idVendor==self.VENDOR_ID and dev.idProduct==self.PRODUCT_ID:
                return dev
        return None
    
    def _open_device(self):
        """Opens the communication channel with the device."""
        self.handle = self.dev.open()
        self.handle.detachKernelDriver(0)
        self.handle.detachKernelDriver(1)
        self.handle.setConfiguration(self.dev.configurations[0])
        self.handle.claimInterface(self.dev.configurations[0].interfaces[0][0])
        self.handle.setAltInterface(self.dev.configurations[0].interfaces[0][0])
    
    def _close_device(self):
        """Closes the "connection" to the device.
        NOTE: If this method is not called before the program exits,
        the device will have to be physically unplugged and replugged
        for the program to work again."""
        self.handle.reset()
        self.dev, self.handle = None, None
        
    def __del__(self):
        if self.dev: self._close_device()
    
    def _send_msg(self, msg):
        """To communicate with the device, one needs to send these values.
        I have no idea what they mean."""
        req_type = usb.TYPE_CLASS | usb.RECIP_INTERFACE | usb.ENDPOINT_OUT
        # self.handle.controlMsg(0x21, 0x09, msg, 0x02, 0x01)
        self.handle.controlMsg(req_type, usb.REQ_SET_CONFIGURATION, msg, value=usb.DT_CONFIG, index=1)
    
    def _cmdfill(self):
        """The CMDFILL tuple gets added to the command that gets sent to the device.
        It controls the amplitude of movements (ie the number of movements it takes to cover the full range).
        Note that vertical and horizontal amplitude are independent.
        For a given amplitude integer, the horizontal range is 3 times as wide as the vertical one."""
        return tuple([self.h_amp, self.v_amp] + 56 * [0])
    
    def _command(self, cmd):
        """Apparently, one needs to send two specific messages to the device before sending in a command.
        I have no idea what they do."""
        self._send_msg(self.INITA)
        self._send_msg(self.INITB)
        self._send_msg(cmd + self._cmdfill())
    
    def fire(self, n=1, d=5):
        """Fires n missiles, waiting d seconds between each launch.
        If n has the special value ALL, all the available missiles are launched.
        if d has the special value RANDOM, the delay will be variable between launches (but always more than 5 seconds).
        Which missile gets fired seem to depend on the device.
        Also, it seems that if the device fails to fire a missile (e.g. if the bay was not loaded),
        it will automatically move to the next one and try to fire again.
        If all the bays are empty, the device does not appear to do anything."""
        
        from time import sleep
        
        if n == 'ALL' or n > self.MISSILE_BAY_SIZE: n = self.MISSILE_BAY_SIZE
        for i in range(n):
            self._command(self.FIRE)
            if i + 1 != n: # To avoid pausing at the end
                if d == 'RANDOM': d = randint(5, 30)
                sleep(d)
    
    
    def fire_all(self, delay=5):
        """Fires all available missiles, waiting $delay seconds between shots."""
        self.fire('ALL', delay)
    
    
    def move(self, direction):
        available = {
            'up':    self.UP,
            'u':     self.UP,
            'north': self.UP,
            'n':     self.UP,
            '8':     self.UP,
            
            'down':  self.DOWN,
            'd':     self.DOWN,
            'south': self.DOWN,
            's':     self.DOWN,
            '2':     self.DOWN,
            
            'left': self.LEFT,
            'l':    self.LEFT,
            'west': self.LEFT,
            'w':    self.LEFT,
            '4':    self.LEFT,
            
            'right': self.RIGHT,
            'r':     self.RIGHT,
            'east':  self.RIGHT,
            'e':     self.RIGHT,
            '6':     self.RIGHT,
            
            'leftup':    self.LEFTUP,
            'lu':        self.LEFTUP,
            'upleft':    self.LEFTUP,
            'ul':        self.LEFTUP,
            'northwest': self.LEFTUP,
            'nw':        self.LEFTUP,
            '7':         self.LEFTUP,
            
            'leftdown':  self.LEFTDOWN,
            'ld':        self.LEFTDOWN,
            'downleft':  self.LEFTDOWN,
            'dl':        self.LEFTDOWN,
            'southwest': self.LEFTDOWN,
            'sw':        self.LEFTDOWN,
            '1':         self.LEFTDOWN,
            
            'rightup':   self.RIGHTUP,
            'ru':        self.RIGHTUP,
            'upright':   self.RIGHTUP,
            'ur':        self.RIGHTUP,
            'northeast': self.RIGHTUP,
            'ne':        self.RIGHTUP,
            '9':         self.RIGHTUP,
            
            'rightdown': self.RIGHTDOWN,
            'rd':        self.RIGHTDOWN,
            'downright': self.RIGHTDOWN,
            'dr':        self.RIGHTDOWN,
            'southeast': self.RIGHTDOWN,
            'se':        self.RIGHTDOWN,
            '3':         self.RIGHTDOWN,
        }
        
        try: self._command(available[str(direction).lower()])
        except KeyError: pass # direction not supported
    
    def stop(self):
        """Stops any movement that may be going on."""
        self._command(self.STOP)


class MissileControlUI:
    def __init__(self, device=None):
        if device:
            self.dev = device
        else:
            self.dev = MissileDevice()


 
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



if __name__=="__main__":
    from optparse import OptionParser
    p = OptionParser()
    p.set_defaults(fire=0, text_ui=True, numpad_ui=False)
    p.add_option('-f', '--fire', help="Fires a missile (can be cumulated).", action='count', dest='fire')
    p.add_option('-t', '--text-ui', help="Start a minimal text interface.", action='store_true', dest='text_ui')
    p.add_option('-n', '--numpad-ui', help="Start a minimal interface using the numeric keypad.", action='store_true', dest='numpad_ui')
    
    options, args = p.parse_args()
    
    try: device = MissileDevice()
    except usb.USBError:
        print "There was a problem communicating with the device."
        print "Make sure you have the appropriate permissions to access USB devices (try running as root)."
        print "If you still have problems, try unplugging and replugging the device and try again."
    
    if options.fire:
        device.fire(options.fire)
    elif options.text_ui: SimpleTextUI(device).run()
    elif options.numpad_ui: SimpleNumpadUI(device).run()
