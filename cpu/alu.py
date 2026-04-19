from amaranth import *
from typing import Tuple

class ALU:
    @staticmethod
    def add(a: int, b: int, carry: int = 0) -> int:
        return a + b + carry
    
    @staticmethod
    def adc_flags(a: int, b: int, carry_in: int) -> Tuple[int, int, int]:
        result = a + b + carry_in
        overflow = (~(a ^ b) & (a ^ result) & 0x80) != 0
        carry = result >= 0x100
        return result[:8], carry, overflow
        
    @staticmethod
    def sbc_flags(a: int, b: int, carry_in: int) -> Tuple[int, int, int]:
        return ALU.adc_flags(a, ~b + 1, carry_in)
    
    @staticmethod
    def cmp_flags(a: int, b: int) -> Tuple[int, int]:
        result = a - b
        carry = result >= 0
        return result[:8], carry
    
    @staticmethod
    def and_op(a: int, b: int) -> int:
        return a & b
    
    @staticmethod
    def ora(a: int, b: int) -> int:
        return a | b
    
    @staticmethod
    def eor(a: int, b: int) -> int:
        return a ^ b
    
    @staticmethod
    def asl(value: int) -> int:
        return (value << 1) & 0xFF
    
    @staticmethod
    def lsr(value: int) -> int:
        return value >> 1
    
    @staticmethod
    def rol(value: int, carry: int) -> int:
        return ((value << 1) | carry) & 0xFF
    
    @staticmethod
    def ror(value: int, carry: int) -> int:
        return (value >> 1) | (carry << 7)
    
    @staticmethod
    def inc(value: int) -> int:
        return (value + 1) & 0xFF
    
    @staticmethod
    def dec(value: int) -> int:
        return (value - 1) & 0xFF
    
    @staticmethod
    def set_nz(result: int) -> Tuple[int, int]:
        n = (result >> 7) & 1
        z = 1 if result == 0 else 0
        return n, z