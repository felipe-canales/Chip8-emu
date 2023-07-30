class chip8 (pyglet.window.Window):

    def __init__(self):
        self.fonts = [0 for x in range(80)]
        # Memory related
        self.memory      = [0 for x in range(4096)]
        self.videoBuffer = [0 for x in range(64*32)]
        self.registers   = [0 for x in range(16)]
        self.keyboard    = [0 for x in range(16)]
        # Opcode
        self.opcode = 0
        # Pointers
        self.memoryIndex    = 0
        self.programCounter = 0x200
        # Timers
        self.delayTimer = 0
        self.soundTimer = 0
        # Stack
        self.stack = [0 for x in range(4096)]
        self.stackPointer = 0
        #---
        self.shouldDraw = False
    
    def start(self):
        self.clear()
        # Memory related
        self.memory      = [0 for x in range(4096)]
        self.videoBuffer = [0 for x in range(64*32)]
        self.registers   = [0 for x in range(16)]
        self.keyboard    = [0 for x in range(16)]
        # Opcode
        self.opcode = 0
        # Pointers
        self.memoryIndex    = 0
        self.programCounter = 0x200
        # Timers
        self.delayTimer = 0
        self.soundTimer = 0
        # Stack
        self.stack = [0 for x in range(4096)]
        self.stackPointer = 0
        #---
        self.shouldDraw = False

        i=0
        while i<80:
            self.memory[i]=self.fonts[i]
            i+=1
    
    def load(self,rom):
        log("Loading {}...".format(rom))
        binary = open(rom,"rb").read()
        i=0
        while i<len(library):
            self.memory[i+0x200]=ord(binary[i])

    def cycle():
        self.opcode = self.memory[self.programCounter]

        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4
        self.pc += 2

        op = self.opcode & 0xf000
        try:
            self.funcmap[op]() ####### ph
        except:
            print "INVALID OPCODE: {}".format(self.opcode)

        if self.delayTimer > 0: self.delayTimer -= 1
        if self.soundTimer > 0: self.soundTimer -= 1
        if self.sounfTimer == 0: #TODO play a sound

def draw():

def main():
    
