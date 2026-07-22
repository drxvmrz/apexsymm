class SymmOperator:
    def __init__(self):
        self.name = ""
        self.eta = 0
        self.a11 = 0
        self.a12 = 0
        self.a13 = 0
        self.a21 = 0
        self.a22 = 0
        self.a23 = 0
        self.a31 = 0
        self.a32 = 0
        self.a33 = 0
        self.a_angle = 0
        self.b_angle = 0
        self.c_angle = 0
        self.t1_cart = 0
        self.t2_cart = 0
        self.t3_cart = 0
        self.t1_affn = 0
        self.t2_affn = 0
        self.t3_affn = 0

class Structure:
    def __init__(self):
        self.name = ""
        self.from_cif = ""
        self.a = 0.0
        self.cartesian_a = []
        self.b = 0.0
        self.cartesian_b = []
        self.c = 0.0
        self.cartesian_c = []
        self.alpha = 0.0
        self.beta = 0.0
        self.gamma = 0.0
        self.sp_gr = ""
        self.sp_gr_num = 0.0
        self.operators = []



