import threading, time
import winsound
import ch8io

STACK_ADDR = 0xEA0
DISPLAY_ADDR = 0xF00
PROGRAM_ADDR = 0x200

memory = [0 for _ in range(4096)]
registers = [0 for _ in range(16)]
I = 0
pc = PROGRAM_ADDR
sp = STACK_ADDR
dt = 0
st = 0

timer_lock = threading.Lock()

def timers():
    global st, dt
    while True:
        timer_lock.acquire()
        if st > 0:
            st -= 1
        #else:
        #    winsound.Beep(500,300)
        if dt > 0:
            print(dt)
            dt -= 1
        timer_lock.release()
        time.sleep(1/60)
threading.Thread(target=timers, daemon=True).start()

memory[0:5 * 16] = [
    0xF0,0x90,0x90,0x90,0xF0, #0
    0x20,0x60,0x20,0x20,0x70, #1
    0xF0,0x10,0xF0,0x80,0xF0, #2
    0xF0,0x10,0xF0,0x10,0xF0, #3
    0x90,0x90,0xF0,0x10,0x10, #4
    0xF0,0x80,0xF0,0x10,0xF0, #5
    0xF0,0x80,0xF0,0x90,0xF0, #6
    0xF0,0x10,0x20,0x40,0x40, #7
    0xF0,0x90,0xF0,0x90,0xF0, #8
    0xF0,0x90,0xF0,0x10,0xF0, #9
    0xF0,0x90,0xF0,0x90,0x90, #A
    0xE0,0x90,0xE0,0x90,0xE0, #B
    0xF0,0x80,0x80,0x80,0xF0, #C
    0xE0,0x90,0x90,0x90,0xE0, #D
    0xF0,0x80,0xF0,0x80,0xF0, #E
    0xF0,0x80,0xF0,0x80,0x80, #F
]

def get_sprite(val):
    return val * 5

def display_clear():
    memory[DISPLAY_ADDR:] = [0 for _ in range(256)]
    ch8io.display_clear()

def draw_group(addr, byte):
    changed = (memory[addr] ^ byte) != memory[addr]
    memory[addr] ^= byte
    return changed

def display_draw(x, y, bytes):
    x_byte, x_rest = x // 8, x % 8
    addr = DISPLAY_ADDR + (x_byte * 32 + y)
    changed = False
    for byte in bytes:
        byte1 = byte >> (x_rest)
        changed = draw_group(addr, byte1) or changed
        ch8io.display_draw(x_byte * 8, y, memory[addr])
        if x_byte < 7:
            byte2 = (byte << (8 - (x_rest))) % 0x100
            changed = draw_group(addr + 32, byte2) or changed
            ch8io.display_draw(x_byte * 8 + 8, y, memory[addr+32])
        y += 1
        addr += 1
    return int(changed)

def load_rom(data):
    data_len = len(data)
    memory[PROGRAM_ADDR:PROGRAM_ADDR + data_len] = list(data)


if __name__ == '__main__':
    print("test")
    time.sleep(10)