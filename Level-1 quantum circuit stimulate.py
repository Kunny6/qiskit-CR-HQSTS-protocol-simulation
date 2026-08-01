import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# 1. 寄存器定义（和参考文献完全一致：q0-q9 + cout）
q = QuantumRegister(10, name='q')  # q0-q4:组1, q5-q9:组2
cout = ClassicalRegister(2, name='cout')
qc = QuantumCircuit(q, cout)

# --------------------------
# 阶段1：制备五量子比特簇态（参考文献同款）
# --------------------------
# 组1：q0→q1→q2→q3→q4
qc.h(q[0])
qc.cx(q[0], q[1])
qc.cx(q[1], q[2])
qc.cx(q[2], q[3])
qc.cx(q[3], q[4])

# 组2：q5→q6→q7→q8→q9
qc.h(q[5])
qc.cx(q[5], q[6])
qc.cx(q[6], q[7])
qc.cx(q[7], q[8])
qc.cx(q[8], q[9])

qc.barrier()  # 垂直虚线（和参考文献一致）

# --------------------------
# 阶段2：Charlie Z基测量（无if，纯测量门）
# --------------------------
qc.measure(q[2], cout[0])  # Charlie0 → x0
qc.measure(q[7], cout[1])  # Charlie1 → x1

qc.barrier()

# --------------------------
# 阶段3：Bob恢复操作（无if，直接画X/Z门，参数在图注说明）
# --------------------------
# 组1（Bob0=q1）：X^a0 + Z^(x0⊕c0)
qc.x(q[1])  # a0=1，执行X门
qc.z(q[1])  # x0⊕c0=1，执行Z门

# 组2（Bob1=q6）：X^a1 + Z^(x1⊕c1)
# a1=0，不画X门；x1⊕c1=1，画Z门
qc.z(q[6])

qc.barrier()

# --------------------------
# 阶段4：最终测量（参考文献同款）
# --------------------------
qc.measure(q[1], cout[0])
qc.measure(q[6], cout[1])

# 生成电路图（无任何if，和参考文献风格一致）
circuit_drawer(
    qc, output='mpl', filename='bob_final_ref_style.png',
    scale=0.8, plot_barriers=True, fold=25,
    style={'show_conditionals': False}  # 强制隐藏if标注
)
plt.show()
