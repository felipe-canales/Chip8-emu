import sys
import pygame
import internals as q
from internals import *
import ch8io
from random import randint

def syscall(arg):
    if arg == 0x0E0:
        display_clear()
        return
    if arg == 0x0EE:
        q.pc = memory[q.sp] + memory[q.sp-1] * 0x100
        q.sp -= 2
        return
    raise ValueError

def goto(arg):
    q.pc = arg - 2

def call(arg):
    q.sp +=2
    memory[q.sp-1] = q.pc // 0x100
    memory[q.sp] = q.pc % 0x100
    q.pc = arg - 2

def skip_if(arg, bol):
    reg = arg // 0x100
    val = arg % 0x100
    if (registers[reg] == val) == bol:
        q.pc += 2

def skip_reg(arg, bol):
    reg1 = arg // 0x100
    reg2 = (arg % 0x100) // 0x10
    if arg % 0x10 != 0:
        raise ValueError
    if (registers[reg1] == registers[reg2]) == bol and arg % 0x10 == 0:
        q.pc += 2

def set_val(arg):
    reg = arg // 0x100
    val = arg % 0x100
    registers[reg] = val

def add(arg):
    reg = arg // 0x100
    val = arg % 0x100
    registers[reg] = (registers[reg] + val) % 0x100

def arit(arg):
    reg1 = arg // 0x100
    reg2 = (arg % 0x100) // 0x10
    op = arg % 0x10
    if op == 0x0:
        registers[reg1] = registers[reg2]
    elif op == 0x1:
        registers[reg1] |= registers[reg2]
    elif op == 0x2:
        registers[reg1] &= registers[reg2]
    elif op == 0x3:
        registers[reg1] ^= registers[reg2]
    elif op == 0x4:
        registers[reg1] += registers[reg2]
        registers[0xF] = int(registers[reg1] > 0xFF)
        registers[reg1] %= 0x100
    elif op == 0x5:
        registers[0xF] = int(registers[reg1] > registers[reg2])
        registers[reg1] = ((registers[reg1] - registers[reg2]) + 0x100) % 0x100
    elif op == 0x6:
        registers[0xF] = registers[reg1] % 2
        registers[reg1] //= 2
    elif op == 0x7:
        registers[0xF] = int(registers[reg1] < registers[reg2])
        registers[reg1] = ((registers[reg2] - registers[reg1]) + 0x100) % 0x100
    elif op == 0xE:
        registers[0xF] = registers[reg1] // 0x80
        registers[reg1] *= 2
    else:
        raise ValueError

def set_i(arg):
    q.I = arg

def jmp_v0(arg):
    q.pc = arg + registers[0x0]

def rnd(arg):
    reg = arg // 0x100
    val = arg % 0x100
    registers[reg] = randint(0 , 0xFF) & val

def draw(arg):
    reg1 = arg // 0x100
    reg2 = (arg % 0x100) // 0x10
    n = arg % 0x10
    registers[0xF] = display_draw(registers[reg1], registers[reg2], memory[q.I : q.I + n])

def skip_key(arg):
    reg1 = arg // 0x100
    rest = arg % 0x100
    cond = (0xA1, 0x9E).index(rest)
    if ch8io.keyboard_check(registers[reg1], cond):
        q.pc += 2

def io(arg):
    reg = arg // 0x100
    op = arg % 0x100
    if op == 0x07:
        timer_lock.acquire()
        registers[reg] = q.dt
        timer_lock.release()
    elif op == 0x0A:
        registers[reg] = ch8io.keyboard_wait()
    elif op == 0x15:
        timer_lock.acquire()
        q.dt = registers[reg]
        timer_lock.release()
    elif op == 0x18:
        timer_lock.acquire()
        q.st = registers[reg]
        timer_lock.release()
    elif op == 0x1E:
        q.I += registers[reg]
    elif op == 0x29:
        q.I = get_sprite(registers[reg])
    elif op == 0x33:
        memory[q.I] = registers[reg] // 100
        memory[q.I+1] = (registers[reg] % 100) // 10
        memory[q.I+2] = registers[reg] % 10
    elif op == 0x55:
        memory[q.I:q.I + reg + 1] = registers[:reg + 1]
    elif op == 0x65:
        registers[:reg + 1] = memory[q.I:q.I + reg + 1]
    else:
        raise ValueError

opcodes = {
    0x0: syscall,
    0x1: goto,
    0x2: call,
    0x3: lambda x: skip_if(x, True),
    0x4: lambda x: skip_if(x, False),
    0x5: lambda x: skip_reg(x, True),
    0x6: set_val,
    0x7: add,
    0x8: arit,
    0x9: lambda x: skip_reg(x, False),
    0xa: set_i,
    0xb: jmp_v0,
    0xc: rnd,
    0xd: draw,
    0xe: skip_key,
    0xf: io,
}

def execute(opcode):
    opcodes[opcode // 0x1000](opcode % 0x1000)

def main():
    rom = sys.argv[1]
    load_rom(open(rom, 'rb').read())
    pygame.init()
    ch8io.display_init()
    running = True
    while running:
        execute(memory[q.pc] * 0x100 + memory[q.pc+1])
        q.pc += 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
