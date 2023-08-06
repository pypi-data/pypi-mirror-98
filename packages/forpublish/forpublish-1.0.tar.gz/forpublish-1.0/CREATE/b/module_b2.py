print('b2')
from a import *
# import math
print(module_a2.math.sin(3.14))
from . import module_b1
from ..a.aa import module_aa
# # import a.aa.module_aa
# module_aa.fun_aa()