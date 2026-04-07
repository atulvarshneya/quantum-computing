# Early Quantum Algorithms - Part 1: Deutsch-Jozsa algorithm

<p style="text-align: center;"> <em>The Deutsch–Jozsa Breakthrough: The First Steps Toward Exponential Quantum Speedup</em></p>


One of the most striking claims about quantum computing is that it can solve certain problems exponentially faster than classical computers.

But how does that actually happen?

In this post, we’ll explore two of the earliest quantum algorithms — Deutsch’s algorithm (1985) and its generalization, the Deutsch–Jozsa algorithm (1992). These are not just historical curiosities; they introduce the core ideas behind quantum speedup: superposition, phase kickback, and interference.

As companions to this post, there are two Python notebooks - [Deutsch's algorithm](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/Well-Known%20Algorithms/deutsch-qckt.ipynb), [Deutsch-Jozsa algorithm](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/Well-Known%20Algorithms/deutsch-jozsa-qckt.ipynb) - that have code for implementing these algorithms. 
These notebooks are written leveraging [Qucircuit](https://github.com/atulvarshneya/quantum-computing/tree/master), a full-featured free to use quantum computing simulator that I developed.

<!--
Superposition in quantum computers points towards the potential for
performing exponentially large computations compared to classical
computers. While such massive speedup is achievable for only certain
problems, it still makes the field full of promise. Even if not all the way to exponential speeedup,
exploiting its power to perform well beyond what is possible with
classical computers, e.g., Grover's algorithm yields quadratic speedup,
is itself a great advantage and motivation for this area of study.

In this post we learn about the Deutsch-Jozsa algorithm (1992) which is
considered the first example of a quantum algorithm to demonstrate an
exponential speedup over *deterministic* classical algorithms. It solves
a specific "black box" problem in *one* query, whereas deterministic
classical algorithms require an exponential number of queries *in the
worst case*. This exponential speedup isn't about clever programming; it 
is about exploiting the fundamental laws of quantum mechanics; specifically, 
leveraging the principles of quantum superposition and 
interference, to solve this problem with such a speedup.
-->

# First the narrower version - Deutsch's algorithm

We start this post with the narrower version of this algorithm, Deutsch's
algorithm, as a pedagogical step to learn Deutsch-Jozsa. Deutsch's
algorithm was the first to show the power of quantum computing by
demonstrating a problem that a quantum computer could solve in **one** step,
while a classical computer required **two**.

It is good to start with this algorithm here as it demonstrated speedup
by leveraging superposition and interference, thus paving the way for
future algorithms.

## Problem statement

Deutsch\'s algorithm solves a simple problem. Consider a
function $f(x)$ that takes a single bit (i.e. 0 or 1) as input and
returns a single bit (i.e. 0 or 1) as output. It is promised that $f(x)$
is either constant, or balanced -

-   A constant function is one where the output is always 0 or always 1,
    regardless of the input.
-   A balanced function is one where the output is 0 for one input and 1
    for the other input.

The function is provided as a "black-box", an oracle, such that we cannot look inside it to see how it works. So, when we refer to it as a quantum operator, we call it $U_f$.

The problem is to determine if the function is constant or balanced with as few evaluations as possible.

Since the function takes a single bit as input and gives a single bit output, there are only four possible functions.

| $f(0)$ | $f(1)$ | |
|:-----:|:-----:|-----|
| 0 | 0 | constant |
| 0 | 1 | balanced |
| 1 | 0 | balanced |
| 1 | 1 | constant |

It's easy to see that classically we would have to call the function
twice to determine if it\'s constant or balanced. For example, we might
call the function with input 0 and learn that the output is $f(0) = 1$.
Looking at the table above, we see two possible outcomes with this --
the last two rows. So, we still can't tell whether it is constant or
balanced. So, we would have to call the function a second time with
input 1 to determine that.

**Deutsch algorithm requires only 1 call to the function to determines that.**

## The Quantum Trick - the core intuition

The core ideas behind Deutsch's algorithm are the following. Each of these are explained  with rigor in the next section.

1. **Superposition**: It creates a superposition in the inut so it presents both the possible inputs to the oracle simultaneously.
2. **Phase kick-back**: This is a trick used often in quantum algorithms where the output value of the oracle leads to the change in the phase of the corresponding input. Note that the superposed inputs leading to output of 0 and output of 1 develop different phase. This encodes the function's output as a phase which makes quantum interference possible.
3. **Interference**: Having done these steps, the final step engineers an interference among the states of the input qubit such that the state converges to a single definite value (i.e., either $\ket{0}$ or $\ket{1}$), thus the measurement extracts that answer with 100% certainity.

Lets now get into the specifics of the algorithm.

## Specifics of the Deutsch's algorithm

At the outset, let us look at the the circuit for this quantum algorithm:

```text
                                  +----+
input qubit   |0> ----------[H]---|    |---[H]----[M]-
                                  | Uf | 
output qubit  |0> -[X]-[H]--------|    |--------------
                                  +----+
                           ^    ^        ^      ^
                           |    |        |      |
                           Ψ1   Ψ2       Ψ3     Ψ4
```

The input qubit as well as the output qubit are initially in state $\ket{0}$. The input qubit is put in superposition by applying Hadamard operation.

The output qubit is prepared in the state $\frac{1}{\sqrt{2}} \left( \ket{0} - \ket{1} \right)$, commonly represented as $\ket{-}$. Output qubit in $\ket{-}$ causes the phase kick-back -- the input that leads to output being 1, causes that input to acquire the phase of a $-ve$ sign.

The final hadamard undoes the superposition, and the phase acquired in the previous steps leads to an interference which puts the input qubit in one of $\ket{0}$ or in $\ket{1}$ states which is the answer extracted by performing measurement on it.

### Some mathematical groundwork for understanding the working of Deutsch's algorithm

**Hadamard operation**

Hadamard on a state $\ket{x}$ is written as

$$
\begin{equation*}
H\ket{x} \rightarrow
\begin{cases}
if\ x = 0 : & \frac{1}{\sqrt{2}}\left( \ket{0} + \ket{1} \right),\\
if\ x = 1 : & \frac{1}{\sqrt{2}}\left( \ket{0} - \ket{1} \right),
\end{cases}
\end{equation*}
$$

Which in a compact form can be written as the following. Lets call this "equation 1"

$$\boxed{H\ket{x} \rightarrow \frac{1}{\sqrt{2}} \sum_{z = 0}^{1}{\left( -1 \right)^{x \cdot z}\ket{z}}}$$

Thus if $\ket{x}=\ket{0}$, this becomes as the following. Lets call this "equation 2".

$$\boxed{H\ket{0}\rightarrow\frac{1}{\sqrt{2}}\sum_{x = 0}^{1}\ket{x}}$$


Writing in these compact forms comes in handy later on, so stay with me on this.

**Oracle operation and phase kick-back**

Now, lets look at the oracle provided for the problem. For $\ket{x}$ in any one of the computational basis states,

$$U_{f}\left( \ket{x}\ket{0} \right) \rightarrow \ket{x}\ket{f(x)}$$

However, more generally, lets assume the output qubit is not prepared as $\ket{0}$ but as state $\ket{y}$. Since every quantum operation must be reversible, the operation of the oracle would be:

$$U_{f}\left( \ket{x}\ket{y} \right) \rightarrow \ket{x}\ket{y \oplus f(x)}$$

An interesting thing happens if we prepare the output qubit as $\ket{-}$, i.e., $\frac{1} {\sqrt{2}} \left( \ket{0} - \ket{1} \right)$

$$U_{f}\left( \ket{x}\ket{-}  \right) \rightarrow \frac{1}{\sqrt{2}}\ket{x}\left( \ket{0 \oplus f(x)} - \ket{1 \oplus f(x)} \right)$$

And, for the two possible values of $f(x)$

$$
\begin{equation*}
U_{f}\left( \ket{x}\ket{-} \right) \rightarrow
\begin{cases}
if\ f(x) = 0 : & \frac{1}{\sqrt{2}}\ket{x}\left( \ket{0} - \ket{1} \right) = \ket{x}\ket{-},\\
if\ f(x) = 1 : & \frac{1}{\sqrt{2}}\ket{x}\left( \ket{1} - \ket{0} \right) = - \ket{x}\ket{-},
\end{cases}
\end{equation*}
$$

Or, in a compact form, it can be written as the following. Lets call it "equation 3"

$$\boxed{U_{f}\left( \ket{x}\ket{-} \right)\rightarrow\left(-1 \right)^{f\left( x \right)}\ket{x} \ket{-}}$$

I.e., if we prepare the output qubit as $\ket{-}$ then applying the
oracle simply adds a phase depending on the value of $f(x)$.

### Understanding the working of Deutsch's algorithm

Now, with these handy tools, we can see how Deutsch's algorithm works.

Please refer to the circuit of the algorithm shown earlier. 
Lets examine the state of the qubits at each step of the running of this circuit -- at $\psi_{1},\ \psi_{2},\ \psi_{3},\ \psi_{4}$ and then at the measurement step

### Step 1 - $\psi_{1}$ - preparing output qubit

The sequence of X followed by H gates, prepares the output qubit in $\frac{1} {\sqrt{2}} \left( \ket{0} - \ket{1} \right)$ state. I.e.,

$$\psi_{1} = \ket{0} \frac{1}{\sqrt{2}} \left( \ket{0} - \ket{1} \right) = \ket{0}\ket{-}$$

### Step 2 - $\psi_{2}$ - Creating full superposition in the input qubit

After applying Hadamard on the input qubit, we get the following by using equation 2,

$$\psi_{2} = \ \frac{1}{\sqrt{2}}\sum_{x = 0}^{1}{\ket{x}}\ket{-}$$

### Step 3 - $\psi_{3}$ - Applying $U_f$, and phase kick-back

Now, the oracle is applied and the phase kick-back occurs. We get the following using equation 3,

$$\psi_{3} = \frac{1}{\sqrt{2}}\sum_{x = 0}^{1}{( - 1)^{f(x)}\ket{x}}\ket{-}$$

### Step 4 - $\psi_{4}$ - Final Hadamard on the input qubit

Finally, Hadamard is applied on input qubit again, so using equation 1

$$\psi_{4} = \frac{1}{\sqrt{2}}\sum_{x = 0}^{1}{( - 1)^{f(x)}\left( \sum_{z = 0}^{1}{\frac{1}{\sqrt{2}}( - 1)^{x \cdot z}\ket{z}} \right)}\ket{-}$$

$$= \frac{1}{2}\left( \sum_{x = 0}^{1}{\sum_{z = 0}^{1}{( - 1)^{x \cdot z + f(x)}\ket{z}}} \right)\ket{-}$$

### Step 5 - Measurement of input qubit

We can now ignore the output qubit, since we are going to measure only the input qubit. From the previos expression, the state of the input qubit is given as

$$\frac{1}{2}\left( \sum_{x = 0}^{1}{\sum_{z = 0}^{1}{( - 1)^{x \cdot z + f(x)}\ket{z}}} \right)$$

We can rearrange this expression to clearly see the amplitude of each basis state

$$\sum_{z = 0}^{1}\left( {\sum_{x = 0}^{1}\frac{1}{2}{( - 1)^{x \cdot z + f(x)}}} \right)\ket{z}$$

Recall that the probability of measuring a basis state is given by the square of the modulus of the amplitude of that basis state

$$\left| {\sum_{x = 0}^{1}\frac{1}{2}{( - 1)^{x \cdot z + f(x)}}} \right|^2$$

Now the trick is to evaluate the probability of measuring $\ket{z}=\ket{0}$, which is given as

$$\left| {\sum_{x = 0}^{1}\frac{1}{2}{( - 1)^{x \cdot 0 + f(x)}}} \right|^2 = \left| {\sum_{x = 0}^{1}\frac{1}{2}{( - 1)^{f(x)}}} \right|^2$$

So, the probabilities of measuring $\ket{0}$
* If the function is constant, the summation in the above will be cumulative and evaluate to 1 -- specifically, if $f(x)$ is $0$ for both inputs, the expression will evaluate to 
$\left| \frac{1}{2} \left( {( - 1)^0+( - 1)^0} \right) \right|^2 = \left| \frac{1}{2} \left( 2 \right) \right|^2 = 1$, and, if $f(x)$ is $1$ for both inputs, the expression will evaluate to $\left| \frac{1}{2} \left( {( - 1)^1+( - 1)^1} \right) \right|^2 = \left| \frac{1}{2} \left( -2 \right) \right|^2 = 1$.
* If the function is balanced, one output of $f(x)$ will be $0$ and the other output will be $1$, thus the terms in the summation will cancel each other and the expression will evaluate to $0$ -- $\left| \frac{1}{2} \left( {( - 1)^0+( - 1)^1} \right) \right|^2 = \left| \frac{1}{2} \left( 1 - 1 \right) \right|^2 = 0$

In other words, the probability to measure $\ket{0}$ evaluates to $1$ if $f(x)$ is constant (*constructive interference*) and $0$ if $f(x)$ is balanced (*destructive interference*). In other words, the final measurement will be 
$\ket{0}$ (all zeros) if and only if f(x)} is constant and it will be the only other state $\ket{1}$ if f(x)} is balanced.

Thus, Deutsch algorithm performs only **one** query to the function to determine the type of the function.

# Deutsch-Jozsa algorithm

Deutsch's algorithm was an important first step in demonstrating how quantum computers could be more efficient than classical computers, but improvement it demonstrated was fairly modest: it required **one** query, compared to **two** in the classical case. But something remarkable happens when we scale this idea to n-bit inputs. 

In 1992, David Deutsch and Richard Jozsa, extended the original algorithm to more qubits. The problem statement was similar: determine whether a function is balanced or constant with as few evaluations as possible. But this time, the function had $n$ bits of input and the same $1$ bit of output, i.e., it mapped $f:\{0,1\}^n \rightarrow \{0,1\}$.

With $n$ bits, the input can have $2^n$ unique values - $0, 1, ..., \left( 2^n-1 \right)$. So, in a balanced function, $2^{n-1}$ inputs would have outputs as $0$, and the other $2^{n-1}$ inputs would have outputs as $1$. Thus in the worst case, a classical computer could get the first $2^{n-1}$ queries to the oracle give the same output, but it would not be posssible to determine if it is a constant function without making $1$ more query. That is, in the worst case it would require $2^{n-1} + 1$ queries, implying a $O(2^n)$ time complexity.

Deutsch and Jozsa showed that using a quantum computer the determination could be made with just $1$ query, thus essentially an exponential speedup.

As we go into the details of Deutsch-Jozsa algorithm, I have intentionally kept the discussion completely parallel to the discussion of the Deutsch's algorithm to make it very straight forward to follow.

## The Same Quantum Trick as in Deutsch's Algorithm

The technique used for this remaines basically the same as for Deutsch's algorithm -

1. **Superposition**: It creates a superposition in the input so it presents all $2^n$ possible inputs to the oracle simultaneously.
2. **Phase kick-back**: the output values of the oracle leads to the change in the phase of the corresponding input.
3. **Interference**: engineer an interference among the states of the input qubit to get a definite answer -- if the function is constant, the input state converges to $\pm \ket{0}^{\otimes n}$ (all $n$ qubits = $\ket{0}$, with amplitude of $\pm 1$), and if balanced, then some state other than $\ket{0}^{\otimes n}$.

## Specifics of the Deutsch-Jozsa algorithm

The circuit for Deutsch-Jozsa algorithm is shown below for input of $6$ qubits --

```text
                      +------+
q000 ----------[H]----|      |----[H]----[M]-
                      |      |          
q001 ----------[H]----|      |----[H]----[M]-
                      |      |          
q002 ----------[H]----|      |----[H]----[M]-
                      |      |          
q003 ----------[H]----|  Uf  |----[H]----[M]-
                      |      |          
q004 ----------[H]----|      |----[H]----[M]-
                      |      |          
q005 ----------[H]----|      |----[H]----[M]-
                      |      |          
q006 -[X]-[H]---------|      |---------------
                      +------+
              ^    ^             ^    ^
              |    |             |    |
              Ψ1   Ψ2            Ψ3   Ψ4
```

The subsequent discussion refers to it.

### Mathematical groundwork for understanding the working of Deutsch-Jozsa algorithm

The math groundwork for Deutsch-Jozsa algorithm is very similar to that for Deutsch algorithm, so lets cover it quickly -

**Hadamard operation on multiple qubits**

Hadamard on a multi-qubit state $\ket{x}, where\ x=x_{n-1}, x_{n-2} ... x_1, x_0$ is written as the following. Lets call it "equation 4"

$$\boxed{H^{\otimes n}\ket{x} \rightarrow \frac{1}{\sqrt{2^n}} \sum_{z = 0}^{2^n-1}{\left( -1 \right)^{x \cdot z}\ket{z}}}$$
$$where\ x \cdot z = x_{n-1} z_{n-1} + x_{n-2} z_{n-2} + ... + x_0 z_0\ \text{ is the sum of the bitwise products}$$

Thus, if $\ket{x}=\ket{0}^{\otimes n}$, this becomes as the following. Lets call it "equation 5".

$$\boxed{H^{\otimes n}\ket{0}^{\otimes n}\rightarrow\frac{1}{\sqrt{2^n}}\sum_{x = 0}^{2^n-1}\ket{x}}$$

**Oracle operation and phase kick-back**

This remains the same as shown for Deutsch algorithm, except that $\ket{x}$ is $n$ qubits here. Lets call it "equation 6"

$$\boxed{U_{f}\left( \ket{x}\ket{-} \right)\rightarrow\left(-1 \right)^{f\left( x \right)}\ket{x} \ket{-}}$$

### Understanding the working of Deutsch-Jozsa algorithm

Here also we examine the state of the qubits at each step of the running of the Deutsch-Jozsa circuit -- at $\psi_{1},\ \psi_{2},\ \psi_{3},\ \psi_{4}$ and then the measurement step

### Step 1 - $\psi_{1}$ - preparing output qubit

The output qubit is prepared in $\frac{1} {\sqrt{2}} \left( \ket{0} - \ket{1} \right)$ state. I.e.,

$$\psi_{1} = \ket{0}^{\otimes n} \frac{1}{\sqrt{2}} \left( \ket{0} - \ket{1} \right) = \ket{0}^{\otimes n}\ket{-}$$

### Step 2 - $\psi_{2}$ - Creating full superposition in the input qubit

After applying Hadamard on each input qubit, we get the following by using equation 5

$$\psi_{2} = \ \frac{1}{\sqrt{2^n}}\sum_{x = 0}^{2^n-1}{\ket{x}}\ket{-}$$

### Step 3 - $\psi_{3}$ - Applying $U_f$, and phase kick-back

Now, the oracle is applied and the phase kick-back occurs. We get the following using equation 6

$$\psi_{3} = \frac{1}{\sqrt{2^n}}\sum_{x = 0}^{2^n-1}{( - 1)^{f(x)}\ket{x}}\ket{-}$$

### Step 4 - $\psi_{4}$ - Final Hadamard on the input qubit

Finally, Hadamard is applied on input qubit again, so using equation 4
$$\psi_{4} = \frac{1}{\sqrt{2^n}}\sum_{x = 0}^{1}{( - 1)^{f(x)}\left( \sum_{z = 0}^{2^n-1}{\frac{1}{\sqrt{2^n}}( - 1)^{x \cdot z}\ket{z}} \right)}\ket{-}$$


$$= \frac{1}{2^n}\left( \sum_{x = 0}^{2^n-1}{\sum_{z = 0}^{2^n-1}{( - 1)^{x \cdot z + f(x)}\ket{z}}} \right)\ket{-}$$

### Step 5 - Measurement of input qubits

Now ignoring the output qubit, and with some simple rearranging, we can rewrite the input qubits state as

$$\sum_{z = 0}^{2^n-1}\left( {\sum_{x = 0}^{2^n-1}\frac{1}{2^n}{( - 1)^{x \cdot z + f(x)}}} \right)\ket{z}$$

So, the amplitude for a state $\ket{k}$ is 

$$\left( {\sum_{x = 0}^{2^n-1}\frac{1}{2^n}{( - 1)^{x \cdot k + f(x)}}} \right)$$

Therefore, the probability for measuring $k=0$

$$\left| {\sum_{x = 0}^{2^n-1}\frac{1}{2^n}{( - 1)^{f(x)}}} \right|^2$$

which evaluates to $1$ if $f(x)$ is constant (*constructive interference*) and $0$ if $f(x)$ is balanced (*destructive interference*). In other words, the final measurement will be 
$\ket{0}^{\otimes n}$ (all zeros) if and only if f(x)} is constant and will yield some other state if f(x)} is balanced.

Thus, Deutsch-Jozsa algorithm performs only **one** query to the function to determine the type of the function. This is **exponential** speedup over *deterministic* classical algorithms.

## Caveat

Note that Deutsch-Jozsa demonstrates speed up compared to 
*deterministic* classical algorithms, if compared with randomized
classical algorithms the advantage disappears. In a subsequent post we
will go over Simon's algorithm, which is considered the first strong
case of exponential speedup. In any case, Deutsch-Jozsa helps understand
some very important concepts which are often useful in designing quantum
algorithms.

# Key takeaways from these two quantum algorithms
1. Where is superposition used?  
input qubit(s) initialized to all possible input values

2. Where does phase kickback happen?  
oracle encodes function values into phase of input qubit(s)

3. Where does interference happen?  
final Hadamard(s) cause constructive/destructive interference to have a 100% or 0% probability for measuring $0$ for constant or balanced $f(x)$, respectively

# Getting hands-on with the algorithms discussed here

As mentioned earlier, there are companion Python notebooks that have code for both these algorithms.
The python notebooks are at the links given below.
* [Deutsch's algorithm](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/Well-Known%20Algorithms/deutsch-qckt.ipynb)
* [Deutsch-Jozsa algorithm](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/Well-Known%20Algorithms/deutsch-jozsa-qckt.ipynb)

These are written using [Qucircuit](https://github.com/atulvarshneya/quantum-computing/tree/master),
a full-featured free to use quantum computing simulator that I developed to support
educational and experimental work in quantum algorithms. You can run on your own computers locally, these and all other code provided in the blog posts here.

You can install
Qucircuit in just a few seconds using:

```shell
pip install qucircuit
```
