<h1 style="text-align: center;">
QAOA Step by Step: Concepts, Circuits, and Code for Quantum Enthusiasts
</h1>

## Variational Quantum Algorithms

Quantum computers promise extraordinary capabilities, from simulating
complex molecules to solving optimization problems that overwhelm
classical machines. But today's hardware is still at an early stage.
Qubits are fragile, gates are noisy, and circuits must remain shallow
before errors dominate. This era, often called the *NISQ era* (Noisy
Intermediate-Scale Quantum), poses a clear challenge \-- how can we make
practical use of these imperfect quantum devices right now?

One of the promising answers is a family of methods called *Variational
Quantum Algorithms (VQAs)*. Instead of relying solely on a quantum
computer to solve a problem end-to-end, VQAs combine the strengths of
quantum and classical computing in a tight feedback loop. The quantum
computer prepares carefully chosen quantum states, and the classical
computer evaluates how good those states are and adjusts the quantum
circuit accordingly. This synergy makes VQAs robust against noise and
ideal for hardware available today.

### Why Variational Quantum Algorithms?

As mentioned earlier, current quantum hardware are intermediate-scale in
number of qubits, and are noisy, thus they are unable to run long
sequences of gates as they tend to lose coherence. However, even with
shallow circuits and a modest number of qubits, quantum computers can
explore extremely large spaces of possibilities. A quantum register of
just 20 qubits represents over a million possible classical states
simultaneously.

VQAs are designed such that instead of building a deep quantum circuit
to produce the final answer, they use a hybrid approach where a
parameterized **quantum circuit's** "knobs"/parameters are tuned by a
**classical optimizer**. The quantum circuit's job is to perform the
heavy lifting to encode candidate solutions into a quantum state. The
classical optimizer's job is to evaluate how good those solutions are
and nudge the parameters toward better ones.

This interaction between quantum exploration and classical optimization
allows VQAs to deliver useful, approximate results even with noisy
intermediate-scale hardware.

### How a Variational Quantum Algorithm Works

At a high level, the flow of a VQA looks very much like training a small
neural network, except that the model is a quantum circuit.

The idea begins with a parameterized quantum circuit, often called an
*ansatz*. This circuit includes adjustable rotation angles or other
tunable values that influence how the quantum state evolves. Once these
parameters are set, the circuit is executed on a quantum computer, which
returns a set of measurement outcomes, usually bitstrings like 0101 or
1110. These bitstrings represent candidate solutions to the problem at
hand.

<img src="./images/media/QAOAblog-01-image1.png" width="600">

*Figure : Variational Quantum Algorithms*

Next, these solutions are evaluated by a classical computer using a
*cost function*. This cost function depends on the problem; in an
optimization task like *MAXCUT*, it could compute the number of edges
crossing a cut. After scoring the results, a classical optimization
algorithm updates the parameters of the quantum circuit. This could be a
gradient-free optimizer like *Nelder-Mead*, *COBYLA*, or *SPSA*, all of
which tolerate noisy measurements well. The new parameters are fed back
into the circuit, and the quantum computer is run again.

This loop continues until the algorithm converges or reaches a stopping
criterion. Progressively, the quantum circuit becomes increasingly
biased toward producing high-quality solutions.

VQAs tightly interleave shallow quantum circuits that perform the hard
quantum evaluations with classical optimizers that steer the search;
hence they represent one of the most practical families of quantum
algorithms today.

### Where VQAs Are Useful

Variational quantum algorithms are already being applied to several
important domains. In quantum chemistry, they can estimate ground-state
energies using methods like the Variational Quantum Eigensolver (VQE).
In quantum machine learning, parameterized circuits act as trainable
models similar to neural networks. And in combinatorial optimization,
which is our focus in this blog series, the *Quantum Approximate
Optimization Algorithm (QAOA)* is one of the most widely studied
approaches.

Because QAOA is conceptually simple, mathematically elegant, and
practical to implement, it has become a favorite example for learning
quantum optimization. That is why this blog series focuses on it.

## QAOA for MAXCUT Problem

Let $`G = (V,E)`$ be an undirected graph, where $`V`$ is the
set of vertices in the graph, and $`E`$ is the set of edges
therein, $`E \subseteq \{ ( i,j)|i,j \in V,\ i \neq j \}`$.

A cut is a partition of the vertex set into two disjoint
subsets $`S`$ and $`S^{'}`$, such
that $`S \cup S^{'} = V`$ and $`S \cap S^{'} = \varnothing`$. The cost of a
cut is the number of edges that span this partition - or are cut by this
partition. The MAXCUT problem is to find a partition that maximizes the
cost of the cut. 

Figure below shows an example MAXCUT for a graph drawn in two different
ways.

<img src="./images/media/QAOAblog-01-image2.png" width="500">

*Figure : Cut in a graph: group A orange, group B blue*


MAXCUT is an *NP-hard* problem and serves as a canonical benchmark for
combinatorial optimization algorithms, including QAOA. Being an NP-hard
problem informally means that, in general, it is computationally
infeasible to find the best solution in a reasonable amount of time. For
a graph with $N$ vertices, there are $2^{N}$ possible ways to assign
vertices to the two groups. Even for modest sizes, exhaustive search
becomes impractical. For example, a graph with 40 vertices has over a
trillion possible partitions.

There are good classical approximation algorithms, and in practice many
heuristics work well. But MAXCUT remains an excellent model problem for
exploring new optimization techniques, especially quantum ones.

### Representing Cuts as Bitstrings

Cuts of graphs naturally map onto *bitstrings*. Each vertex can belong
to one of two subsets, so we assign 0 for one subset, and 1 for the
other subset. This gives us a neat representation. With that, a cut of a
graph with $N$ vertices corresponds to an $N$-bit string. For example,
if $N\  = \ 4$, the string $0011$ represents a cut where vertex 0 is in
set 1, vertex 1 is in set 1, vertex 2 is in set 0, and vertex 3 is in
set 0. From this bitstring, we can compute the number of edges crossing
the cut. Specifically, if an edge connects two vertices with different
bit values, that edge contributes to the cut.

Since quantum computers natively work with superpositions of bitstrings,
hence by representing each vertex as a qubit, $N$-qubits can represent
*all* $2^{N}$ possible cuts at the same time.

### The Concept of Cost Hamiltonian

In this sub-section we just briefly introduce the concept of cost
Hamiltonian as applicable to QAOA for MAXCUT problem, we will cover this
in more details in a subsequent blog post.

The key idea is that by representing each vertex of the graph by a
qubit, we can formulate the cost function (the number of edges crossing
the cut) as a cost Hamiltonian, a quantum operator whose eigenvalues
correspond to the cut value.

The Hamiltonian we envision is diagonal in the computational basis, such
that the diagonal entry for a state $|x\rangle$ is exactly the cost
value of that assignment. The Hamiltonian, would look like this --

$$H_{c} = \begin{pmatrix}
cost(00\ldots 0) & 0 & \cdots & \  & 0 \\
0 & cost(00\ldots 1) & \  & \  & \  \\
 \vdots & \vdots \  & \ddots & \  & \vdots \\
\  & \  & \  & \  & 0 \\
0 & \ 0 & \cdots & \  & cost(11\ldots 1) \\
\end{pmatrix}$$

Thus, $H_{c}$ has each computational basis vector as its eigenvector,
with the corresponding cost value as its eigenvalue.

$$H_{c}\left| x \right\rangle = \begin{pmatrix}
\text{cost}\left( 00\ldots 0 \right) & 0 & \cdots & \  & 0 \\
0 & \text{cost}\left( 00\ldots 1 \right) & \  & \  & \  \\
 \vdots & \vdots \  & \ddots & \  & \vdots \\
\  & \  & \  & \  & 0 \\
0 & \ 0 & \cdots & \  & \text{cost}\left( 11\ldots 1 \right) \\
\end{pmatrix}\begin{pmatrix}
0 \\
0 \\
\begin{matrix}
\ldots \\
1 \\
\ldots \\
0 \\
\end{matrix} \\
\end{pmatrix} = cost\left( x \right)|x\rangle$$

Using this Hamiltonian we formulate a unitary operator,
$U_{c}(\gamma) = e^{- i\gamma H_{c}}$, which turns out to be [fairly
straight forward to implement in a quantum circuit]{.underline}. Why
this $U_{c}(\gamma)$ operator is useful is explained in the subsequent
section.

We can in fact make a stronger statement about the ease of implementing
the unitary $U_{c}(\gamma)$ for the MAXCUT problem on a quantum circuit.
This observation extends beyond MAXCUT to the broader class of
*Quadratic Unconstrained Binary Optimization (QUBO)* problems. MAXCUT
itself can be formulated as a QUBO problem, and conversely, any QUBO
problem can be reduced to an instance of MAXCUT.

Note that we do not build $U_{c}(\gamma)$ by explicitly calculating the
entries of the Hamiltonian $H_{c}$, that would be infeasible as it would
require us to calculate $2^{N} \times 2^{N}$ entries of that matrix. We
instead build a quantum circuit of $N$ qubits, which implicitly
implements the required $2^{N} \times 2^{N}$ unitary operator[^1].

In a later post we will get into mathematical details of deriving the
cost Hamiltonian for MAXCUT and its corresponding unitary operator.

## The Core Structure of QAOA

A QAOA circuit has a very elegant structure:

-   Prepare an initial superposition

-   Apply a sequence of alternating quantum operators

-   Measure the qubits to obtain candidate solutions

Let's unpack each of these steps.

### Step 1: Preparing the Initial Superposition

Note that with $N$ qubits, a quantum system can represent all $2^{N}$
possible cuts simultaneously in superposition. This is the starting
point of QAOA, the algorithm begins with a quantum state that represents
all candidate solutions at once.

At the very beginning, all qubits are initialized to the state
$|0\rangle$. A Hadamard gate is then applied to every qubit. This
creates the uniform superposition:

$$\frac{1}{\sqrt{2^{N}}}\sum_{x \in \{ 0,1\}^{N}}^{}{|x\rangle}\ $$

This step is crucial. It ensures that QAOA does not bias the search
toward any particular solution at the start. Instead, the algorithm
*learns* which cuts are better through quantum interference and
classical optimization.

#### Quantum Circuit for Preparing Initial Superposition

This step is realized as the following quantum circuit:

```
q1  --[H]--
q2  --[H]--
.
.
qN  --[H]--
```

### Step 2: Alternating Cost and Mixer Operators

Once the superposition is created, QAOA applies a repeating sequence of
two alternating quantum operators:

-   a **cost operator**, derived from the problem being solved, and

-   a **mixer operator**, which drives exploration of the solution
    space.

Each pair of cost and mixer operations is called a QAOA layer. If the
algorithm uses $p$ such layers, we say the circuit has *depth* $p$.

#### The Cost Operator: Imprinting the Problem onto the Quantum State

Since the quantum circuits use unitary operators, so we define a unitary
operator, as was discussed in an earlier section (*The Concept of Cost
Hamiltonian*)

$$U_{C}\left( \gamma \right) = e^{- i\gamma H_{C}}$$

*where* $H_{C}$ *is the* cost Hamiltonian*, and* $\gamma$ *is a
real-valued parameter. The parameter* $\gamma$ *is tuned as part of the
QAOA algorithm such that the circuit outputs as close to optimal
solution as possible.*

So, what does the cost unitary do? Recall from earlier that each
computational basis vector $|x\rangle$ is an eigenvector of $H_{C}$ with
the eigenvalue equal to the cut value, $C\left( x \right)$, of that
solution. Hence, $U_{C}\left( \gamma \right)$ simply adds a phase to
each state proportional to its specific cut value.

$$U_{C}\left( \gamma \right)\left| x \right\rangle = e^{- i\gamma H_{C}}\left| x \right\rangle = e^{- i\gamma C\left( x \right)}|x\rangle$$

Intuitively, "Good" cuts acquire one type of phase, and "Bad" cuts
acquire another. This phase encoding is subtle but powerful. It does not
directly change probabilities *yet*, but it sets the stage for quantum
interference to amplify good solutions and suppress bad ones in later
steps.

#### The Mixer Operator: Exploring the Search Space

If we applied only the cost operator repeatedly, the quantum state would
only accumulate phases, and the probability of measuring any state would
remain the same, i.e., all states would remain equally likely. To truly
*explore* the space of solutions, QAOA introduces a second operator, the
mixer.

The standard mixer Hamiltonian used in QAOA is

$$H_{B} = \sum_{i = 1}^{N}X_{i}$$

where $X_{i}$ is the Pauli-X operator acting on qubit $i$.

Just as we did for cost Hamiltonian, we define a unitary operator for
mixer Hamiltonian as

$$U_{B}\left( \beta \right) = \ e^{- i\beta H_{B}}$$

where $H_{B}$ is the mixer Hamiltonian, and $\beta$ is a real-valued
parameter. Again, the parameter $\beta$ is tuned as part of QAOA
algorithm such that the circuit outputs as close to optimal solution as
possible.

So, what does the mixer unitary do? It rotates each qubit around the
X-axis of the *Bloch sphere*. This causes amplitude to flow between
neighboring bitstrings, i.e., those that differ by a single bit flip.
Basically, the mixer operator causes constructive interference to
increase the amplitude of good states, and destructive interference to
reduce the amplitudes of bad states. Thus, the probability of measuring
good states increases as a result.

Looking at it in a different way, the mixer ensures that the algorithm
does not get "stuck", the probability mass moves through the space of
all cuts, and useful interference patterns can form between good and bad
solutions.

#### What Does a Full QAOA Layer Do?

Each QAOA layer first applies the cost operator (problem-specific), then
the mixer operator (problem-independent). One layer nudges the quantum
state in the direction of better solutions. Multiple layers allow these
nudges to accumulate.

As mentioned earlier, the algorithm uses $p$ such layers. The overall
quantum operation applied by the $p$ QAOA layers looks like this:

$$U\left( \gamma,\beta \right) = e^{- i\beta_{p}H_{B}}e^{- i\gamma_{p}H_{C}}\ldots e^{- i\beta_{1}H_{B}}e^{- i\gamma_{1}H_{C}}$$

As the depth $p$ increases the quantum state becomes more expressive,
the algorithm can approximate more complex probability distributions,
the quality of the best solution typically improves (though noise also
increases).

In the limit of very large $p$, QAOA approaches adiabatic quantum
optimization. But in practice, even small $p$ values often give
surprisingly good results.

> **A sidebar**: Mixer unitary causes amplitudes to flow between
> neighboring states, those that differ by a bit flip. And, QAOA applies
> the cost and mixer unitaries multiple times, in $p$ layers. Each layer
> can propagate amplitude further through the solution space.
>
> However, keeping circuits shallow is a major goal for QAOA because of
> noise and decoherence in current quantum hardware. So, if you need
> $p\  \approx \ N$, the number of qubits, to reach good states that are
> far apart in Hamming space, that could become problematic as $N$
> grows. Hence there seems to be a tension in QAOA's design.
>
> But please note that for some problems (like MAXCUT), relatively small
> $p$ can give good results. For others, you might need $p$ that scales
> with $N$, where QAOA can become impractical. **This is an area of
> active research** whether QAOA requires $p = O(N)$, or can succeed
> with lower bounds on $p$ such as
> $O\left( 1 \right),\ O\left( \text{logN} \right)$, for various problem
> classes. There\'s no universal answer. Researchers also explore
> problem-specific mixer Hamiltonians that might allow larger \"jumps\"
> through the solution space, potentially reducing the required depth of
> the circuit.

#### Quantum Circuit for Cost and Mixer Unitaries

The cost Hamiltonian turns out to be as following. For now you can check
it to be correct by constructing it by hand for a small number of
vertices and edges. In a sequel to this post, we will get a bit deeper
into the rationale for this.

$$H_{C} = \sum_{\left( i,j \right) \in E}^{}{\frac{1}{2}\ (I - Z_{i}Z_{j})}$$

With this we can see that the unitary
$U_{C}\left( \gamma \right) = e^{- i\gamma H_{C}}$, is

$$U_{C}\left( \gamma \right) = \prod_{\left( i,j \right) \in E}^{}e^{- i\frac{\gamma}{2}\left( I - Z_{i}Z_{j} \right)} = \prod_{\left( i,j \right) \in E}^{}{e^{- i\frac{\gamma}{2}\text{I\ }} \bullet e^{+ i\frac{\gamma}{2}Z_{i}Z_{j}}}
$$

$$U_{C}\left( \gamma \right) = \prod_{\left( i,j \right) \in \ E}^{}e^{i\frac{\gamma}{2}\left( Z_{i}\ Z_{j} \right)}$$

The standard identity for implementing this operator is:

$$e^{i\frac{\gamma}{2}\ Z_{i}\ Z_{j}} = CNOT_{i \rightarrow j}\text{\ \ }R_{Z}\left( - \gamma \right)_{j}\text{\ CNO}T_{i \rightarrow j}$$

In quantum circuit form, for each edge $(i,j)$, the following sequence
of quantum gates are added to the quantum circuit -

```
qi  ---*------------------*---
.      |                  |
.      |                  |
qj  --[X]--[Rz(-gamma)]--[X]--
```

$$H_{B} = \sum_{i = 1}^{N}X_{i}$$

Hence the mixer unitary is

$$U_{B}\left( \beta \right) = e^{- i\beta H_{B}} = \prod_{i = 1}^{N}e^{- i\beta X_{i}}$$

For a single qubit, the operator

$$e^{- i\beta X}$$

is implemented exactly by a rotation around the X-axis of the Bloch
sphere:

$$R_{x}\left( 2\beta \right)$$

So, the **entire mixer layer** is simply $R_{x}\left( 2\beta \right)$
applied to every qubit.

In quantum circuit form

```
q1  --[Rx(2*beta)]--
q2  --[Rx(2*beta)]--
.
.
qN  --[Rx(2*beta)]--
```

### Step 3: Classical Optimizer

All of QAOA's intelligence resides not in the circuit itself, but in how
the parameters $\gamma_{k}$ and $\beta_{k}$ are chosen.

After the quantum circuit is executed and measured many times, the
classical computer estimates the expected cut value produced by the
current parameters. It then updates the parameters and runs the circuit
again. This loop continues until performance stabilizes.

This is where QAOA truly becomes a hybrid algorithm: quantum mechanics
shapes the probability distribution, and classical optimization steers
it.

## Getting Hands-on with QAOA Implementation in Python

It's a good time now to see the code in action, you can explore a
complete Python implementation of QAOA for MAXCUT
[here](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/Well-Known%20Algorithms/QAOA-maxcut.ipynb).
This Python notebook walks through all the major ideas behind QAOA in a
tutorial format, building the algorithm step by step and showing exactly
how the circuit behaves.

The implementation runs on
[Qucircuit](https://github.com/atulvarshneya/quantum-computing/tree/master),
a full-featured quantum computing simulator that I developed to support
educational and experimental work in quantum algorithms. You can install
Qucircuit in just a few seconds using:

```shell
pip install qucircuit
```

Once installed, you can run the entire QAOA implementation locally on
your own computer and experiment with it at your own pace.

## What Comes Next

This post presented the key ideas behind QAOA at the architectural
level: superposition, alternating operators, layers, and parameter
tuning. In the next post, we'll go deeper into the cost and Mixer
Hamiltonians, $H_{C}$ and $H_{B}$, and corresponding unitaries, $U_{C}$
and $U_{B}$, for MAXCUT and develop better understanding about them.

[^1]: Every N-qubit unitary operator if written-out explicitly is a
    $2^{N} \times 2^{N}$ matrix.
