from amaranth import *
from cpu.instructions import (
    get_opcode_info, get_mnemonic, get_addressing_mode, 
    get_instruction_length, get_cycles, AddressingMode
)
from cpu.alu import ALU

class Decoder:
    def __init__(self):
        pass
    
    @staticmethod
    def decode(irq_flag, opcode):
        info = get_opcode_info(opcode)
        if info is None:
            return "ILL", AddressingMode.IMP, 1, 2
        
        name, mode, length, cycles = info
        return name, mode, length, cycles
    
    @staticmethod
    def calc_address(mode, pc, a, x, y, data):
        if mode == AddressingMode.IMM:
            return pc, 2
        elif mode == AddressingMode.ZP0:
            return data[0], 2
        elif mode == AddressingMode.ZPX:
            return (data[0] + x) & 0xFF, 2
        elif mode == AddressingMode.ZPY:
            return (data[0] + y) & 0xFF, 2
        elif mode == AddressingMode.ABS:
            return data, 3
        elif mode == AddressingMode.ABX:
            return (data[0] + x), 3
        elif mode == AddressingMode.ABY:
            return (data[0] + y), 3
        elif mode == AddressingMode.REL:
            offset = data[0]
            if offset >= 128:
                offset -= 256
            return (pc + offset) & 0xFFFF, 2
        else:
            return 0, 0
    
    @staticmethod
    def calc_indirect(addr, x):
        lo = addr
        hi = (addr + 1) & 0xFF
        return ((hi << 8) | lo)
    
    @staticmethod
    def calc_indirect_y(addr, y, add_cycles):
        return ((addr[1] << 8) | addr[0]) + y, add_cycles