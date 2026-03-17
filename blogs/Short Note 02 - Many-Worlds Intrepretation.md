<h1 style="text-align: center;">
The Everettian Many-Worlds Interpretation
</h1>

**TODO: Get the actual qtrace outputs and plug them in**

*An Intuitive Guide for Quantum Computing Practitioners*

# 1. Introduction

Quantum mechanics is perhaps the most precisely tested theory in all of
science. Yet nearly a century after its formulation, physicists still
disagree about what it means. The mathematical formalism --- the
Schrödinger equation, wavefunctions, operators --- is agreed upon. The
disagreement is about interpretation: what is the wavefunction, and what
happens when we measure a quantum system?

The dominant textbook answer is the *Copenhagen interpretation*. It says
that a quantum system evolves as a wavefunction until a measurement
occurs, at which point the wavefunction *collapses* to a single definite
outcome. This is pragmatically useful but philosophically unsatisfying:
collapse is never derived from the Schrödinger equation, it is simply
postulated. What counts as a measurement? What physical process triggers
collapse? Copenhagen offers no mechanism.

The Everettian Many-Worlds Interpretation (MWI), proposed by Hugh
Everett III in 1957, takes a different stance: there is no collapse. The
wavefunction always evolves unitarily according to the Schrödinger
equation. What we experience as a measurement outcome is not collapse,
but it is the observer becoming *entangled* with the quantum system,
branching into one of many coexisting branches of the universal
wavefunction.

This note explains MWI intuitively, with worked circuit examples using
Qucircuit. The goal is to give you a mental model that is useful when
reasoning about superposition, entanglement, and measurement in quantum
circuits.

# 2. Branches: What They Actually Are

In MWI, the wavefunction is not a tool for computing probabilities of a
single outcome. It is a complete description of *all* coexisting
realities simultaneously. Each term in the superposition is a branch, a
fully real, self-consistent version of the world.

Consider a single qubit in a superposition state:

$$\ket{\psi} = \alpha\ket{0} + \ket{1}$$

Copenhagen says: the qubit has no definite value; when measured, it
*collapses* to $\ket{0}$ with probability $|\alpha|^{2}$, or
$\ket{1}$ with probability $|\beta|^{2}$.

MWI says: both branches exist. The branch where the qubit is $\ket{0}$
and the branch where it is $\ket{1}$ are both real. The amplitudes
$\alpha$ and $\beta$ are branch weights, they determine how much of
the wavefunction each branch carries, which corresponds to the
probability that an observer (who is themselves part of the
wavefunction) ends up in that branch.

This is not just philosophical rebranding. The distinction has concrete
consequences for how we reason about interference, entanglement, and the
behaviour of quantum algorithms, as we will see.

# 3. Watching a Branch Form Using A Single Qubit

Let us make this concrete with a circuit. We apply a Hadamard gate to a
single qubit initialized in $\ket{0}$. The Hadamard gate is the
canonical "branching" gate --- it takes a definite state and puts it
into an equal superposition:

$$H\ket{0} = \frac{1}{\sqrt{2}}\left( \ket{0} + \ket{1} \right)$$

In MWI terms: after the Hadamard gate, the universe has branched into
two equally weighted branches, one where the qubit is $\ket{0}$ and
one where it is $\ket{1}$. Both are real.

Let us run this on the simulator and observe the statevector evolving in
real time (we use Qucircuit's Qdeb backend and set qtrace=True):

*Code --- Single qubit branching via Hadamard*

```python
import qckt
import qckt.backend as bknd

# 1 qubit, 1 classical bit
circuit = qckt.QCkt(1, 1, 'Branching via Hadamard')
circuit.H(0) # Apply Hadamard, this is the branching event
circuit.M([0]) # Measure

job = qckt.Job(circuit, qtrace=True)
bkeng = bknd.Qdeb()
bkeng.runjob(job)
```

*Representative output:*

```text
Initial State
0    1.00000000+0.00000000j

H Qubit[0]
0    0.70710678+0.00000000j     <- branch 1: qubit=0, amplitude 1/sqrt(2)
1    0.70710678+0.00000000j     <- branch 2: qubit=1, amplitude 1/sqrt(2)

MEASURED Qubit[0] = [0] with probability = 0.5
0    1.00000000+0.00000000j     <- Measured: 0 (or 1, with equal probability)
```

The output shows exactly what MWI describes. After the Hadamard, the
statevector has two non-zero entries --- two branches, each carrying
amplitude $\frac{1}{\sqrt{2}}$. The squared magnitude of each amplitude
gives the probability: $\left( \frac{1}{\sqrt{2}} \right)^{2} = 0.5$ for
each branch. When we measure, we as observers become entangled with the
qubit and *find ourselves in one of the two branches*. The other branch
does not disappear --- it simply no longer interacts with us.

# 4. Entanglement: Branches Becoming Correlated

In the [Short Note on superposition and
entanglement](https://github.com/atulvarshneya/quantum-computing/blob/master/blogs/Short%20Note%2001%20-%20Superposition%20and%20Entanglement.md),
we saw how entanglement arises from superposition combined with a
conditional interaction. MWI gives this a particularly clear reading:
entanglement is what happens when the branches of two systems become
correlated.

Consider two qubits. Before any interaction, their branches are
independent --- knowing the state of one tells you nothing about the
other. After a conditional operation (like a CNOT gate applied to a
qubit in superposition), the branches become locked together: each
branch of the first qubit now has a definite corresponding state in the
second qubit. The two systems can no longer be described independently.
This is entanglement.

The canonical example is the Bell state, created by a Hadamard on qubit
$0$ followed by a CNOT:

$$\frac{1}{\sqrt{2}}\left( \ket{00} + \ket{11} \right)$$

In MWI language, this state has exactly two branches. Branch 1: both
qubits are $0$. Branch 2: both qubits are $1$. There is no branch where
qubit 0 is $0$ and qubit 1 is $1$, or vice versa. The branches are
perfectly correlated. This correlation is not a signal or a causal
influence --- it is simply the structure of the wavefunction.

# 5. Code Example --- Entanglement as Branch Correlation

Let us trace through the Bell state circuit step by step and watch the
branch structure evolve in the statevector:

*Code --- Building a Bell state, tracing branch evolution*

```python
import qckt
import qckt.backend as bknd

# 2 qubits, 2 classical bits
circuit = qckt.QCkt(2, 2, 'Bell State')
circuit.H(0)      # Step 1: branch qubit 0
circuit.CX(0, 1)  # Step 2: correlate branches of qubit 1 with qubit 0
circuit.M([1, 0]) # Measure both qubits

job = qckt.Job(circuit, qtrace=True)
bkeng = bknd.Qdeb()
bkeng.runjob(job)

# Also run multi-shot to confirm branch probabilities
circuit2 = qckt.QCkt(2, 2, 'Bell State multi-shot')
circuit2.H(0)
circuit2.CX(0, 1)

job2 = qckt.Job(circuit2, shots=1000)
bkeng2 = bknd.Qeng()
bkeng2.runjob(job2)
creg_counts = job2.get_counts()
print(creg_counts)
```

*Representative output:*

```text
Initial State
00    1.00000000+0.00000000j    <- single branch: both qubits 0

H Qubit[0]
00    0.70710678+0.00000000j    <- branch 1: q0=0, q1=0 (independent)
01    0.70710678+0.00000000j    <- branch 2: q0=1, q1=0 (independent)

CX Qubit[0, 1]
00    0.70710678+0.00000000j    <- branch 1: q0=0, q1=0 (correlated)
11    0.70710678+0.00000000j    <- branch 2: q0=1, q1=1 (correlated)
                                Note: |01> and |10> have zero amplitude, those branches do not exist

MEASURED Qubit[1, 0] = [1, 1] with probability = 0.5
11    1.00000000+0.00000000j    <- Measured: 00 or 11 (never 01 or 10)>




And, the output of multishot run

{0: 496, 3: 504}    <- we see only |00> and |11> outcomes, each approximately 50% of the time>
```

The trace tells the story precisely. After the Hadamard, the two
branches are independent --- qubit 1 is 0 in both. After the CNOT, the
branches are correlated --- qubit 1 has been forced to match qubit 0 in
each branch. The states $\ket{01}$ and $\ket{10}$ have zero amplitude: those
branches do not exist in this wavefunction.

The multi-shot run confirms this: over $1000$ measurements, we see only
$\ket{00}$ and $\ket{11}$ outcomes, each approximately $50\%$ of the
time. Each shot is the simulator (or a real quantum computer) sampling
one branch. The perfect correlation is not due to any signal between the
qubits at measurement time, the correlation was baked into the branch
structure the moment the CNOT was applied.

# 6. Measurement: You Are Part of the Wavefunction Too

This is where MWI makes its boldest claim, and where it most cleanly
resolves the measurement problem.

In Copenhagen, measurement is a special physical process that collapses
the wavefunction. The observer is treated as external to the quantum
system --- a classical entity that peers in and forces a definite
outcome. But this is conceptually awkward: where exactly is the boundary
between the quantum system and the classical observer? No such boundary
exists in nature.

MWI dissolves this problem by treating the observer as a physical system
like any other. When you measure a qubit in superposition, *you* become
entangled with it. The combined wavefunction of qubit + observer
branches into:

$$\frac{1}{\sqrt{2}}(\ket{0}\ket{observer\ saw\ 0}\  + \ \ket{1}\ket{observer\ saw\ 1})$$

Both branches are real. In one branch, you are an observer who saw 0. In
the other, you are an observer who saw 1. You subjectively experience
only one outcome because your physical state, your memory, your
measurement apparatus, is part of one branch and cannot interact with
the other.

The probability of ending up in each branch is given by the Born rule:
$|amplitude|^{2}$. In MWI, deriving the Born rule from first principles
is non-trivial (more on this in Section 9), but *operationally* the rule
is the same as in Copenhagen. The difference is conceptual:
probabilities in MWI are not about which outcome *will happen* --- they
are about which branch *you will find yourself in*.

# 7. Decoherence: Why Branches Feel Classical

A natural objection to MWI: if all branches are real and the
wavefunction never collapses, why do we never experience superposition
in everyday life? Why does a cat never seem to be simultaneously alive
and dead?

The answer is **decoherence**. When a quantum system interacts with its
environment, i.e., with air molecules, photons, any surrounding
particles, it becomes entangled with an enormous number of environmental
degrees of freedom. The branches of the wavefunction acquire effectively
orthogonal environmental states.

Recall from [Short Note on superposition and
entanglement](https://github.com/atulvarshneya/quantum-computing/blob/master/blogs/Short%20Note%2001%20-%20Superposition%20and%20Entanglement.md)
that interference between two branches requires them to overlap, i.e.,
mathematically, their inner product must be non-zero. Once a branch is
entangled with a macroscopic environment, its environmental state is
orthogonal to the other branch's environmental state. Their inner
product is effectively zero. The interference among branches becomes
practically impossible.

This is not collapse. Both branches still exist in the universal
wavefunction. But they are rendered mutually invisible, each branch
evolves as if the other does not exist, which is exactly what we
experience as classical, definite outcomes.

The speed of decoherence depends on the size of the system. A single
isolated qubit in a well-engineered quantum computer can maintain
coherence (keep its branches interfering) for microseconds to
milliseconds. A macroscopic object like a cat decoheres in order of
$10^{- 20}$ *seconds* or faster, far too quickly for superposition to be
observable at human scales.

This has a direct practical implication for quantum computing:
maintaining coherence, i.e., keeping the branches of your computation
from becoming entangled with the environment is precisely the
engineering challenge of building a quantum computer. Every source of
noise is a decoherence channel, a pathway by which your computational
branches become entangled with, and effectively lost to, the
environment.

# 8. A Practitioner's Takeaway

MWI is not just philosophical comfort. It provides a concrete mental
model for reasoning about quantum circuits:

-   Every gate operation either creates branches (superposition gates
    like H) or correlates branches across qubits (entangling gates like
    CX). Tracing the branch structure through a circuit is a powerful
    debugging tool.

-   Quantum algorithms work by constructing interference between
    branches. The art of quantum algorithm design is engineering the
    branch amplitudes so that wrong answers cancel out and the correct
    answer is amplified. Grover's algorithm, Deutsch-Jozsa, and the
    QFT-based algorithms all follow this pattern.

-   Noise and decoherence are unwanted entanglement with the
    environment. Every error in a quantum circuit can be understood as a
    branching event caused by the environment, because the environment
    has "measured" your qubit and collapsed its branches from your
    circuit's perspective.

-   The statevector in the quantum computer simulator ***is*** the
    wavefunction. Reading it through an MWI lens as a list of coexisting
    branches with their weights gives you direct intuition for what the
    circuit is doing at every step. Liberally use Qdeb with qtrace=True.

I find that using MWI framing makes the mechanisms of quantum algorithms
considerably more transparent.

# 9. Honest Caveats

MWI is a preference, not settled science. Two open problems deserve
acknowledgment:

**The preferred basis problem**. MWI says the universe branches, but the
Schrödinger equation alone does not specify *which basis* the branching
occurs in. Why do we branch into states like $\ket{alive}$ and $\ket{dead}$ rather
than their superpositions? Decoherence theory largely resolves this ---
environmental interactions select a preferred "pointer basis" --- but
the resolution is still debated at the foundational level.

**The probability problem**. In MWI, all branches exist. What does it
mean to say one branch has probability 0.7 and another has probability
0.3? Deriving the Born rule, the rule that says probabilities equal
squared amplitudes, purely from the MWI axioms without circularity is a
hard open problem. David Deutsch and David Wallace have proposed
decision-theoretic derivations, but these remain contested.

These are genuine foundational challenges. The practical stance taken in
this note is that MWI provides the most coherent and intuitive framework
for reasoning about quantum circuits, while acknowledging that no
interpretation is fully problem-free.
