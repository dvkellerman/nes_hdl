from amaranth import *
from amaranth.lib.coding import *
from typing import Tuple, Optional

# CPU State Machine States
class CPUState:
    FETCH_OPCODE = 0
    FETCH_OPERAND_1 = 1
    FETCH_OPERAND_2 = 2
    EXECUTE = 3
    WRITE_BACK = 4

# Addressing Mode Enumeration
class AddrMode:
    IMP = 0   # Implied
    IMM = 1   # Immediate
    ZP0 = 2   # Zero Page
    ZPX = 3   # Zero Page,X
    ZPY = 4   # Zero Page,Y
    ABS = 5   # Absolute
    ABX = 6   # Absolute,X
    ABY = 7   # Absolute,Y
    IND = 8   # Indirect
    IZX = 9   # (Indirect,X)
    IZY = 10  # (Indirect),Y
    REL = 11  # Relative
    ACC = 12  # Accumulator

# Instruction OpCodes - (mnemonic, addressing_mode, base_cycles)
OPCODES: dict[int, Tuple[str, int, int]] = {
    0x00: ("BRK", AddrMode.IMP, 7), 0x01: ("ORA", AddrMode.IZX, 6), 0x05: ("ORA", AddrMode.ZP0, 3), 0x06: ("ASL", AddrMode.ZP0, 5),
    0x08: ("PHP", AddrMode.IMP, 3), 0x09: ("ORA", AddrMode.IMM, 2), 0x0A: ("ASL", AddrMode.ACC, 2), 0x0D: ("ORA", AddrMode.ABS, 4),
    0x0E: ("ASL", AddrMode.ABS, 6), 0x10: ("BPL", AddrMode.REL, 2), 0x11: ("ORA", AddrMode.IZY, 5), 0x15: ("ORA", AddrMode.ZPX, 4),
    0x16: ("ASL", AddrMode.ZPX, 6), 0x18: ("CLC", AddrMode.IMP, 2), 0x19: ("ORA", AddrMode.ABY, 4), 0x1D: ("ORA", AddrMode.ABX, 4),
    0x1E: ("ASL", AddrMode.ABX, 7), 0x20: ("JSR", AddrMode.ABS, 6), 0x21: ("AND", AddrMode.IZX, 6), 0x24: ("BIT", AddrMode.ZP0, 3),
    0x25: ("AND", AddrMode.ZP0, 3), 0x26: ("ROL", AddrMode.ZP0, 5), 0x28: ("PLP", AddrMode.IMP, 4), 0x29: ("AND", AddrMode.IMM, 2),
    0x2A: ("ROL", AddrMode.ACC, 2), 0x2C: ("BIT", AddrMode.ABS, 4), 0x2D: ("AND", AddrMode.ABS, 4), 0x2E: ("ROL", AddrMode.ABS, 6),
    0x30: ("BMI", AddrMode.REL, 2), 0x31: ("AND", AddrMode.IZY, 5), 0x35: ("AND", AddrMode.ZPX, 4), 0x36: ("ROL", AddrMode.ZPX, 6),
    0x38: ("SEC", AddrMode.IMP, 2), 0x39: ("AND", AddrMode.ABY, 4), 0x3D: ("AND", AddrMode.ABX, 4), 0x3E: ("ROL", AddrMode.ABX, 7),
    0x40: ("RTI", AddrMode.IMP, 6), 0x41: ("EOR", AddrMode.IZX, 6), 0x45: ("EOR", AddrMode.ZP0, 3), 0x46: ("LSR", AddrMode.ZP0, 5),
    0x48: ("PHA", AddrMode.IMP, 3), 0x49: ("EOR", AddrMode.IMM, 2), 0x4A: ("LSR", AddrMode.ACC, 2), 0x4C: ("JMP", AddrMode.ABS, 3),
    0x4D: ("EOR", AddrMode.ABS, 4), 0x4E: ("LSR", AddrMode.ABS, 6), 0x50: ("BVC", AddrMode.REL, 2), 0x51: ("EOR", AddrMode.IZY, 5),
    0x55: ("EOR", AddrMode.ZPX, 4), 0x56: ("LSR", AddrMode.ZPX, 6), 0x58: ("CLI", AddrMode.IMP, 2), 0x59: ("EOR", AddrMode.ABY, 4),
    0x5D: ("EOR", AddrMode.ABX, 4), 0x5E: ("LSR", AddrMode.ABX, 7), 0x60: ("RTS", AddrMode.IMP, 6), 0x61: ("ADC", AddrMode.IZX, 6),
    0x65: ("ADC", AddrMode.ZP0, 3), 0x66: ("ROR", AddrMode.ZP0, 5), 0x68: ("PLA", AddrMode.IMP, 4), 0x69: ("ADC", AddrMode.IMM, 2),
    0x6A: ("ROR", AddrMode.ACC, 2), 0x6C: ("JMP", AddrMode.IND, 5), 0x6D: ("ADC", AddrMode.ABS, 4), 0x6E: ("ROR", AddrMode.ABS, 6),
    0x70: ("BVS", AddrMode.REL, 2), 0x71: ("ADC", AddrMode.IZY, 5), 0x75: ("ADC", AddrMode.ZPX, 4), 0x76: ("ROR", AddrMode.ZPX, 6),
    0x78: ("SEI", AddrMode.IMP, 2), 0x79: ("ADC", AddrMode.ABY, 4), 0x7D: ("ADC", AddrMode.ABX, 4), 0x7E: ("ROR", AddrMode.ABX, 7),
    0x81: ("STA", AddrMode.IZX, 6), 0x84: ("STY", AddrMode.ZP0, 3), 0x85: ("STA", AddrMode.ZP0, 3), 0x86: ("STX", AddrMode.ZP0, 3),
    0x88: ("DEY", AddrMode.IMP, 2), 0x8A: ("TXA", AddrMode.IMP, 2), 0x8C: ("STY", AddrMode.ABS, 4), 0x8D: ("STA", AddrMode.ABS, 4),
    0x8E: ("STX", AddrMode.ABS, 4), 0x90: ("BCC", AddrMode.REL, 2), 0x91: ("STA", AddrMode.IZY, 6), 0x94: ("STY", AddrMode.ZPX, 4),
    0x95: ("STA", AddrMode.ZPX, 4), 0x96: ("STX", AddrMode.ZPY, 4), 0x98: ("TYA", AddrMode.IMP, 2), 0x99: ("STA", AddrMode.ABY, 5),
    0x9A: ("TXS", AddrMode.IMP, 2), 0x9D: ("STA", AddrMode.ABX, 5), 0xA0: ("LDY", AddrMode.IMM, 2), 0xA1: ("LDA", AddrMode.IZX, 6),
    0xA2: ("LDX", AddrMode.IMM, 2), 0xA4: ("LDY", AddrMode.ZP0, 3), 0xA5: ("LDA", AddrMode.ZP0, 3), 0xA6: ("LDX", AddrMode.ZP0, 3),
    0xA8: ("TAY", AddrMode.IMP, 2), 0xA9: ("LDA", AddrMode.IMM, 2), 0xAA: ("TAX", AddrMode.IMP, 2), 0xAC: ("LDY", AddrMode.ABS, 4),
    0xAD: ("LDA", AddrMode.ABS, 4), 0xAE: ("LDX", AddrMode.ABS, 4), 0xB0: ("BCS", AddrMode.REL, 2), 0xB1: ("LDA", AddrMode.IZY, 5),
    0xB4: ("LDY", AddrMode.ZPX, 4), 0xB5: ("LDA", AddrMode.ZPX, 4), 0xB6: ("LDX", AddrMode.ZPY, 4), 0xB8: ("CLV", AddrMode.IMP, 2),
    0xB9: ("LDA", AddrMode.ABY, 4), 0xBA: ("TSX", AddrMode.IMP, 2), 0xBC: ("LDY", AddrMode.ABX, 4), 0xBD: ("LDA", AddrMode.ABX, 4),
    0xBE: ("LDX", AddrMode.ABY, 4), 0xC0: ("CPY", AddrMode.IMM, 2), 0xC1: ("CMP", AddrMode.IZX, 6), 0xC4: ("CPY", AddrMode.ZP0, 3),
    0xC5: ("CMP", AddrMode.ZP0, 3), 0xC6: ("DEC", AddrMode.ZP0, 5), 0xC8: ("INY", AddrMode.IMP, 2), 0xC9: ("CMP", AddrMode.IMM, 2),
    0xCA: ("DEX", AddrMode.IMP, 2), 0xCC: ("CPY", AddrMode.ABS, 4), 0xCD: ("CMP", AddrMode.ABS, 4), 0xCE: ("DEC", AddrMode.ABS, 6),
    0xD0: ("BNE", AddrMode.REL, 2), 0xD1: ("CMP", AddrMode.IZY, 5), 0xD5: ("CMP", AddrMode.ZPX, 4), 0xD6: ("DEC", AddrMode.ZPX, 6),
    0xD8: ("CLD", AddrMode.IMP, 2), 0xD9: ("CMP", AddrMode.ABY, 4), 0xDD: ("CMP", AddrMode.ABX, 4), 0xDE: ("DEC", AddrMode.ABX, 6),
    0xE0: ("CPX", AddrMode.IMM, 2), 0xE1: ("SBC", AddrMode.IZX, 6), 0xE4: ("CPX", AddrMode.ZP0, 3), 0xE5: ("SBC", AddrMode.ZP0, 3),
    0xE6: ("INC", AddrMode.ZP0, 5), 0xE8: ("INX", AddrMode.IMP, 2), 0xE9: ("SBC", AddrMode.IMM, 2), 0xEA: ("NOP", AddrMode.IMP, 2),
    0xEC: ("CPX", AddrMode.ABS, 4), 0xED: ("SBC", AddrMode.ABS, 4), 0xEE: ("INC", AddrMode.ABS, 6), 0xF0: ("BEQ", AddrMode.REL, 2),
    0xF1: ("SBC", AddrMode.IZY, 5), 0xF5: ("SBC", AddrMode.ZPX, 4), 0xF6: ("INC", AddrMode.ZPX, 6), 0xF8: ("SED", AddrMode.IMP, 2),
    0xF9: ("SBC", AddrMode.ABY, 4), 0xFD: ("SBC", AddrMode.ABX, 4), 0xFE: ("INC", AddrMode.ABX, 7),
}

def get_opcode_info(op: int) -> Tuple[str, int, int]:
    """Get (mnemonic, addressing_mode, cycles) for an opcode."""
    return OPCODES.get(op, ("NOP", AddrMode.IMP, 2))

def get_mnemonic(op: int) -> str:
    """Get mnemonic for an opcode."""
    return get_opcode_info(op)[0]

def get_addr_mode(op: int) -> int:
    """Get addressing mode for an opcode."""
    return get_opcode_info(op)[1]

def get_cycles(op: int) -> int:
    """Get base cycles for an opcode."""
    return get_opcode_info(op)[2]