import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=DeprecationWarning)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import QasmSimulator
from qiskit.circuit.library import HGate

plt.rcParams['figure.dpi'] = 150


# ---------------- Cluster ----------------
def prepare_5q_cluster(qc, qubits):
    h = HGate()
    for q in qubits:
        qc.append(h, [q])
    qc.cx(qubits[0], qubits[1])
    qc.cx(qubits[1], qubits[2])
    qc.cx(qubits[2], qubits[3])
    qc.cx(qubits[3], qubits[4])
    qc.cx(qubits[0], qubits[4])


# ---------------- Bell encode ----------------
def bell_measurement_encoding(qc, q_s, q_a, cr):
    qc.cx(q_s, q_a)
    qc.h(q_s)
    qc.measure(q_s, cr[0])
    qc.measure(q_a, cr[1])


# ---------------- Bell decode ----------------
def bell_measurement_recovery(qc, q0, q1, cr):
    qc.cx(q0, q1)
    qc.h(q0)
    qc.measure(q0, cr[0])
    qc.measure(q1, cr[1])


# ---------------- Measurements ----------------
def z_measurement(qc, q, cr):
    qc.measure(q, cr[0])


def x_measurement(qc, q, cr):
    qc.h(q)
    qc.measure(q, cr[0])


# =========================================================
# ====================== Circuits ==========================
# =========================================================

def bob_recover_circuit():
    q_s = QuantumRegister(2)
    q_a = QuantumRegister(2)
    q_b = QuantumRegister(2)
    q_c = QuantumRegister(2)
    q_d = QuantumRegister(2)
    q_e = QuantumRegister(2)

    cr_a1 = ClassicalRegister(2)
    cr_a2 = ClassicalRegister(2)
    cr_c1 = ClassicalRegister(1)
    cr_c2 = ClassicalRegister(1)
    cr_out = ClassicalRegister(2)

    qc = QuantumCircuit(q_s,q_a,q_b,q_c,q_d,q_e,
                        cr_a1,cr_a2,cr_c1,cr_c2,cr_out)

    # ✅ Bell secret
    qc.h(q_s[0])
    qc.cx(q_s[0], q_s[1])

    prepare_5q_cluster(qc,[q_a[0],q_b[0],q_c[0],q_d[0],q_e[0]])
    prepare_5q_cluster(qc,[q_a[1],q_b[1],q_c[1],q_d[1],q_e[1]])

    bell_measurement_encoding(qc,q_s[0],q_a[0],cr_a1)
    bell_measurement_encoding(qc,q_s[1],q_a[1],cr_a2)

    z_measurement(qc,q_c[0],cr_c1)
    z_measurement(qc,q_c[1],cr_c2)

    # ❗ 不做恢复门

    qc.measure(q_b[0], cr_out[0])
    qc.measure(q_b[1], cr_out[1])

    return qc


def charlie_recover_circuit():
    q_s = QuantumRegister(2)
    q_a = QuantumRegister(2)
    q_b = QuantumRegister(2)
    q_c = QuantumRegister(2)
    q_d = QuantumRegister(2)
    q_e = QuantumRegister(2)

    cr_a1 = ClassicalRegister(2)
    cr_a2 = ClassicalRegister(2)
    cr_b1 = ClassicalRegister(1)
    cr_b2 = ClassicalRegister(1)
    cr_d1 = ClassicalRegister(1)
    cr_d2 = ClassicalRegister(1)
    cr_out = ClassicalRegister(2)

    qc = QuantumCircuit(q_s,q_a,q_b,q_c,q_d,q_e,
                        cr_a1,cr_a2,cr_b1,cr_b2,cr_d1,cr_d2,cr_out)

    qc.h(q_s[0])
    qc.cx(q_s[0], q_s[1])

    prepare_5q_cluster(qc,[q_a[0],q_b[0],q_c[0],q_d[0],q_e[0]])
    prepare_5q_cluster(qc,[q_a[1],q_b[1],q_c[1],q_d[1],q_e[1]])

    bell_measurement_encoding(qc,q_s[0],q_a[0],cr_a1)
    bell_measurement_encoding(qc,q_s[1],q_a[1],cr_a2)

    z_measurement(qc,q_b[0],cr_b1)
    z_measurement(qc,q_b[1],cr_b2)

    x_measurement(qc,q_d[0],cr_d1)
    x_measurement(qc,q_d[1],cr_d2)

    qc.measure(q_c[0], cr_out[0])
    qc.measure(q_c[1], cr_out[1])

    return qc


def david_recover_circuit():
    q_s = QuantumRegister(2)
    q_a = QuantumRegister(2)
    q_b = QuantumRegister(2)
    q_c = QuantumRegister(2)
    q_d = QuantumRegister(2)
    q_e = QuantumRegister(2)

    cr_a1 = ClassicalRegister(2)
    cr_a2 = ClassicalRegister(2)
    cr_b1 = ClassicalRegister(1)
    cr_b2 = ClassicalRegister(1)
    cr_c1 = ClassicalRegister(1)
    cr_c2 = ClassicalRegister(1)
    cr_e1 = ClassicalRegister(1)
    cr_e2 = ClassicalRegister(1)
    cr_out = ClassicalRegister(2)

    qc = QuantumCircuit(q_s,q_a,q_b,q_c,q_d,q_e,
                        cr_a1,cr_a2,cr_b1,cr_b2,
                        cr_c1,cr_c2,cr_e1,cr_e2,cr_out)

    qc.h(q_s[0])
    qc.cx(q_s[0], q_s[1])

    prepare_5q_cluster(qc,[q_a[0],q_b[0],q_c[0],q_d[0],q_e[0]])
    prepare_5q_cluster(qc,[q_a[1],q_b[1],q_c[1],q_d[1],q_e[1]])

    bell_measurement_encoding(qc,q_s[0],q_a[0],cr_a1)
    bell_measurement_encoding(qc,q_s[1],q_a[1],cr_a2)

    z_measurement(qc,q_b[0],cr_b1)
    z_measurement(qc,q_b[1],cr_b2)

    x_measurement(qc,q_c[0],cr_c1)
    x_measurement(qc,q_c[1],cr_c2)

    x_measurement(qc,q_e[0],cr_e1)
    x_measurement(qc,q_e[1],cr_e2)

    qc.measure(q_d[0], cr_out[0])
    qc.measure(q_d[1], cr_out[1])

    return qc


# =========================================================
# ====================== Post-processing ===================
# =========================================================

def clean(k):
    return "".join(k.split())


def post_bob(bits):
    out = list(map(int, bits[-2:]))

    # Alice Bell（前4位）
    a = bits[0:4]

    if a[0] == '1':
        out[0] ^= 1
    if a[2] == '1':
        out[1] ^= 1

    return "".join(map(str,out))


def post_charlie(bits):
    out = list(map(int, bits[-2:]))

    # David X measurement（位置稳定在中段）
    if bits.count('1') % 2 == 1:
        out[0] ^= 1
        out[1] ^= 1

    return "".join(map(str,out))


def post_david(bits):
    out = list(map(int, bits[-2:]))

    if bits.count('1') % 2 == 1:
        out[0] ^= 1
        out[1] ^= 1

    return "".join(map(str,out))


def process(counts, func):
    final = {'00':0,'01':0,'10':0,'11':0}
    for k,v in counts.items():
        bits = clean(k)
        new = func(bits)
        final[new] += v
    return final


# =========================================================
# ====================== Simulation ========================
# =========================================================

def simulate_and_plot():

    sim = QasmSimulator()
    shots = 10000

    rb = sim.run(bob_recover_circuit(), shots=shots).result()
    rc = sim.run(charlie_recover_circuit(), shots=shots).result()
    rd = sim.run(david_recover_circuit(), shots=shots).result()

    cb = process(rb.get_counts(), post_bob)
    cc = process(rc.get_counts(), post_charlie)
    cd = process(rd.get_counts(), post_david)

    print("\nFinal Results:")
    print("Bob:", cb)
    print("Charlie:", cc)
    print("David:", cd)

    # Plot
    states = ['00','01','10','11']
    fig, axs = plt.subplots(1,3,figsize=(18,5))

    for ax, data, title in zip(
        axs,
        [cb,cc,cd],
        ['Bob','Charlie','David']
    ):
        ax.bar(states,[data[s] for s in states])
        ax.axhline(2500, linestyle='--')
        ax.set_title(title)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    simulate_and_plot()
