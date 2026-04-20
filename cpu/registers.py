from amaranth import *

class Registers(Module):
    def __init__(self):
        self.a = Signal(8, name="a")
        self.x = Signal(8, name="x")
        self.y = Signal(8, name="y")
        self.sp = Signal(8, name="sp")
        self.pc = Signal(16, name="pc")
        
        self.p = Signal(8, name="p")
        
        self.flag_n = Signal(name="flag_n")
        self.flag_v = Signal(name="flag_v")
        self.flag_d = Signal(name="flag_d")
        self.flag_i = Signal(name="flag_i")
        self.flag_z = Signal(name="flag_z")
        self.flag_c = Signal(name="flag_c")
        
    def set_flags_nz(self, value):
        self.flag_n.value = value[7]
        self.flag_z.value = value == 0
        
    def set_flags_cnz(self, value):
        self.flag_c.value = value[8]
        self.flag_n.value = value[7]
        self.flag_z.value == (value[:8] == 0)
        
    def set_flags_cmp(self, result, reg):
        self.flag_n.value = result[7]
        self.flag_z.value = result[:8] == reg
        self.flag_c.value = result[8]
        
    def set_p(self):
        self.p.eq(Cat(self.flag_c[0], self.flag_z[0], 0b00100000, self.flag_d[0], self.flag_i[0], 0b00000010, self.flag_v[0], self.flag_n[0]))