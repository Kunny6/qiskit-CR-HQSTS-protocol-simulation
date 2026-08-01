import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

q = QuantumRegister(10, name='q')
cout = ClassicalRegister(2, name='cout')
qc = QuantumCircuit(q, cout)

# 阶段1：簇态制备
qc.h(q[0]); qc.cx(q[0], q[1]); qc.cx(q[1], q[2]); qc.cx(q[2], q[3]); qc.cx(q[3], q[4])
qc.h(q[5]); qc.cx(q[5], q[6]); qc.cx(q[6], q[7]); qc.cx(q[7], q[8]); qc.cx(q[8], q[9])
qc.barrier()

# 阶段2：协作测量（Bob-Z + Charlie-X + Emma-X）
qc.measure(q[1], cout[0])
qc.measure(q[6], cout[1])

qc.h(q[2]); qc.measure(q[2], cout[0])
qc.h(q[7]); qc.measure(q[7], cout[1])

qc.h(q[4]); qc.measure(q[4], cout[0])
qc.h(q[9]); qc.measure(q[9], cout[1])
qc.barrier()

# 阶段3：David恢复操作（无if，纯X/Z门）
# 组1（David0=q3）：X^(e0⊕x0⊕z0) + Z^(f0⊕y0⊕w0)
qc.x(q[3])
qc.z(q[3])

# 组2（David1=q8）：X^(e1⊕x1⊕z1) + Z^(f1⊕y1⊕w1)
qc.x(q[8])
qc.z(q[8])
qc.barrier()

# 阶段4：最终测量
qc.measure(q[3], cout[0])
qc.measure(q[8], cout[1])

# 生成电路图
circuit_drawer(
    qc, output='mpl', filename='david_final_ref_style.png',
    scale=0.8, plot_barriers=True, fold=25,
    style={'show_conditionals': False}
)
plt.show()
