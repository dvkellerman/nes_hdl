from amaranth import *

from .loads_stores import add_loads_stores
from .alu import add_alu_ops
from .inc_dec import add_inc_dec
from .shifts import add_shifts
from .control import add_control
from .stack import add_stack_transfers_flags


def execute_instruction(m, cpu, opcode):
    """Resolve operand value, then dispatch to instruction groups."""
    resolved = Signal(8, name="resolved")

    # Immediate opcodes use the fetched operand byte directly;
    # all other addressing modes get their value via data_in from memory.
    with m.Switch(opcode):
        with m.Case(
            0xA9, 0xA2, 0xA0,          # LDA, LDX, LDY imm
            0x09, 0x29, 0x49,           # ORA, AND, EOR imm
            0x69, 0xE9,                 # ADC, SBC imm
            0xC9, 0xC0, 0xE0,          # CMP, CPY, CPX imm
        ):
            m.d.comb += resolved.eq(cpu.operand)
        with m.Default():
            m.d.comb += resolved.eq(cpu.bus.data_rd)

    add_loads_stores(m, cpu, opcode, resolved)
    add_alu_ops(m, cpu, opcode, resolved)
    add_inc_dec(m, cpu, opcode, resolved)
    add_shifts(m, cpu, opcode)
    add_control(m, cpu, opcode)
    add_stack_transfers_flags(m, cpu, opcode)
