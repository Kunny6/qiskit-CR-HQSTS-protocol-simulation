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

# 阶段2：协作测量（Bob-Z基 + David-X基）
qc.measure(q[1], cout[0])  # Bob0 → x0
qc.measure(q[6], cout[1])  # Bob1 → x1

qc.h(q[3]); qc.measure(q[3], cout[0])  # David0-X基 → y0
qc.h(q[8]); qc.measure(q[8], cout[1])  # David1-X基 → y1
qc.barrier()

# 阶段3：Charlie恢复操作（无if，纯X/Z门）
# 组1（Charlie0=q2）：X^(b0⊕x0) + Z^(d0⊕y0)
qc.x(q[2])
qc.z(q[2])

# 组2（Charlie1=q7）：X^(b1⊕x1) + Z^(d1⊕y1)
qc.z(q[7])  # X门不执行，只画Z门
qc.barrier()

# 阶段4：最终测量
qc.measure(q[2], cout[0])
qc.measure(q[7], cout[1])

# 生成电路图
circuit_drawer(
    qc, output='mpl', filename='charlie_final_ref_style.png',
    scale=0.8, plot_barriers=True, fold=25,
    style={'show_conditionals': False}
)
plt.show()
