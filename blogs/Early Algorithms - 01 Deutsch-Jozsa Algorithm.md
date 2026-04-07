<!--
# The outline of the blog post

## Problem (Deutsch)
* Introduce the simple function:
  * constant vs balanced
* Classical cost: 2 evaluations
* Quantum claim: 1 evaluation

Keep this short — it’s just the hook.

> Treat it like: a 5–7 minute conceptual warm-up
> The real value is Deutsch–Jozsa.

## The Quantum Trick (intuition only)
Introduce the key idea:
* evaluate function on superposition
* use phase kickback
* extract answer via interference

This is the conceptual core.

## Deutsch Algorithm — now introduce math
* circuit
* intuition (not heavy math)
* highlight:<br>
“We didn’t compute f(0) and f(1) separately — we engineered interference.”

Structure the math it like this:

Step 1 — Setup (light math)
Show initial state: output qubit prepared in $\ket{-}$
$$\ket{0} \frac{1}{\sqrt{2}}(\ket{0} -\ket{1})$$

Step 2 — Superposition: applying H on input qubit
$$ \frac{1}{\sqrt{2}}(\ket{0}+\ket{1})\cdot\frac{1}{\sqrt{2}}(\ket{0}-\ket{1}) $$
$$ \frac{1}{2}(\ket{0}+\ket{1})\cdot(\ket{0}-\ket{1}) $$
Step 3 — Oracle (Introduce Phase Kickback)
$$ \frac{1}{2}\ket{0}(\ket{0\oplus f(0)} - \ket{1 \oplus f(0)}) + \frac{1}{2} \ket{1}(\ket{0 \oplus f(1)} - \ket{1 \oplus f(1)})$$

$$ \ket{x}\ket{-} \longrightarrow (-1)^{f(x)} \ket{x}\ket{-} $$
👉 This is the single most important equation in the post

Step 4 — Interference

After Hadamard:
$$\text{constant} \rightarrow \ket{0}$$
$$\text{balanced} \rightarrow \ket{1}$$

AV: I think must show math for getting these 0 and 1
$$
H \ket{x} \longrightarrow \frac{1}{\sqrt{2}} ((-1)^{x \cdot 0} \ket{0} +(-1)^{x \cdot 1} \ket{1})
$$
where 
$$
(x \cdot y) = x_0 y_0 \oplus x_1 y_1
$$
And then show for $\ket{0}$ the amplitude is 1 if constant, and 0 if balanced.

Step 5 — Plain English Interpretation

Immediately explain:

* function values encoded as phase
* interference extracts global property
🚀 Key Insight for Your Blog

Your differentiation will come from this pattern:
* Equation → Interpretation → Insight.

Not just equations.

## Scaling to Deutsch–Jozsa
Now transition:

> “What if the input size is n bits?”

* Classical deterministic → $2^{𝑛−1}+1$ queries
* Quantum → $1$ query

This is where the “exponential” story lands.

?? math for DJ??

## Caveat (important - keep this)
You already plan this, which is great:

> With randomized classical algorithms, the advantage disappears.

This builds credibility and trust.

## What is really happening

This is your differentiator. Apply your 5-point lens:

1. Where is superposition used?  
input register initialized to all possible inputs
2. Where does phase kickback happen?  
oracle encodes function values into phase
3. Where does interference happen?  
final Hadamards cause constructive/destructive interference
4. What information is encoded?  
global property (constant vs balanced) encoded in phase pattern
5. How does measurement extract it?  
measurement reads out the interference result directly

This section will be gold for your audience.

-->

# Exponential Speedup Algorithms: Deutsch-Jozsa algorithm

<p style="text-align: center;"> <em>First signs of possibility of exponential speedup</em></p>

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

# First a narrower version - Deutsch's algorithm

We start this post with a narrower version of this algorithm, Deutsch
algorithm as a pedagogical step to learn Deutsch-Jozsa. Deutsch's
algorithm (1985) was the first to show the power of quantum computing by
demonstrating a problem that a quantum computer could solve in **one** step,
while a classical computer required **two**.

It is good to start with this algorithm here as it demonstrated speedup
by leveraging superposition and interference, thus paving the way for
future algorithms.

## Problem statement

Deutsch\'s algorithm solves a simple problem. Consider a
function $f(x)$ that takes a single bit (i.e. 0 or 1) as input and
returns a single bit (i.e. 0 or 1) as output. It is promised that $f(x)$
is either constant, or balanced -

-   A constant function is one where the output is always 0 or always 1,
    regardless of the input.
-   A balanced function is one where the output is 0 for one input and 1
    for the other input.

The function is provided as a "black-box", an oracle, such that we cannot look inside it to see how it works. So, when we refer to it as a quantum operator, we call it $U_f$.

The problem is to determine if the function is constant or balanced.

Since the function takes a single bit as input and gives a single bit output, there are only four possible functions.

| $f(0)$ | $f(1)$ | |
|:-----:|:-----:|-----|
| 0 | 0 | constant |
| 0 | 1 | balanced |
| 1 | 0 | balanced |
| 1 | 1 | constant |

It's easy to see that classically we would have to call the function
twice to determine if it\'s constant or balanced. For example, we might
call the function with input 0 and learn that the output is $f(0) = 1$.
Looking at the table above, we see two possible outcomes with this --
the last two rows. So, we still can't tell whether it is constant or
balanced. So, we would have to call the function a second time with
input 1 to determine that.

**Deutsch algorithm requires only 1 call to the function to determines that.**

## The Quantum Trick - just the intuition

The core ideas behind Deutsch's algorithm are the following. Each of these are explained  with rigor in the next section.

1. **Superposition**: It creates a superposition in the inut so it presents both the possible inputs to the function simultaneously.
2. **Phase kick-back**: This is a trick used often in quantum algorithms where the output value of the function leads to the change in the phase of the corresponding input. Note that the inputs leading to output of 0 and inputs with output of 1 develop different phase. As mentioned above, the two inputs with the updated phases exist simultaneously.
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

The input qubit as wella as the output qubit are initially in state $\ket{0}$. The input qubit is put in superposition by applying Hadamard operation.

The output qubit is put in the state $\frac{1}{\sqrt{2}} \left( \ket{0} - \ket{1} \right)$, commonly represented as $\ket{-}$. Output qubit in $\ket{-}$ causes the phase kick-back -- the input that leads to output being 1, causes that input to acquire the phase of a $-ve$ sign.

The final hadamard undoes the superposition, and the phase acquired in the previous steps leads to an interference which puts the input qubit in one of $\ket{0}$ or in $\ket{1}$ states which is the answer extracted by performing measurement on it.

### Some mathematical groundwork for understanding the working of Deutsch's algorithm

**Hadamard operation**

Hadamard on a state $\ket{x}$ is written as

$$H\ket{x} \rightarrow \left\{ \begin{array}{r}
\frac{1}{\sqrt{2}}\left( \ket{0} + \ket{1} \right),\ if\ x = 0 \\
\frac{1}{\sqrt{2}}\left( \ket{0} - \ket{1} \right),\ if\ x = 1
\end{array} \right.\ $$

Which in a compact form can be written as the following, lets call this "equation 1"

$$\boxed{H\ket{x} \rightarrow \frac{1}{\sqrt{2}} \sum_{z = 0}^{1}{\left( -1 \right)^{x \cdot z}\ket{z}}}$$

Thus if $x=0$, this becomes as the following. Lets call this "equation 2".

$$\boxed{\mathbf{H}\ket{0}\rightarrow\frac{1}{\sqrt{2}}\sum_{x = 0}^{1}\ket{x}}$$


Writing in these compact forms comes in handy later on, so stay with me on this.

**Oracle operation and phase kick-back**

Now, lets look at the oracle provided for the problem. For $\ket{x}$ in any one of the computational basis states,

$$U_{f}\left( \ket{x}\ket{0} \right) \rightarrow \ket{x}\ket{f(x)}$$

However, more generally, lets assume the output qubit is not prepared as $\ket{0}$ but as state $\ket{y}$. Since every quantum operation must be reversible, the operation of the oracle would be:

$$U_{f}\left( \ket{x}\ket{y} \right) \rightarrow \ket{x}\ket{y \oplus f(x)}$$

An interesting thing happens if we prepare the output qubit as
$\ket{-}$, i.e.,$\frac{1}{\sqrt{2}}\left( \ket{0} - \ket{1} \right)$

$$U_{f}\left( \ket{x}\ket{-}  \right) \rightarrow \frac{1}{\sqrt{2}}\ket{x}\left( \ket{0 \oplus f(x)} - \ket{1 \oplus f(x)} \right)$$

And, for the two possible values of $f(x)$

$$U_{f}\left( \ket{x}\ket{-} \right) \rightarrow \left\{ \begin{array}{l}
\frac{1}{\sqrt{2}}\ket{x}\left( \ket{0} - \ket{1} \right) = \ket{x}\ket{-},\ if\ f(x) = 0 \\
\frac{1}{\sqrt{2}}\ket{x}\left( \ket{1} - \ket{0} \right) = - \ket{x}\ket{-},\ if\ f(x) = 1
\end{array} \right.\ $$

Or, in a compact form, it can be written as the following, lets call it "equation 3"

$$\boxed{U_{f}\left( \ket{x}\ket{-} \right)\rightarrow\left(-1 \right)^{f\left( x \right)}\ket{x} \ket{-}}$$

I.e., if we prepare the output qubit as $\ket{-}$ then applying the
oracle simply adds a phase depending on the value of $f(x)$.

### Understanding the working of Deutsch's algorithm

Now, with these handy tools, we can see how Deutsch's algorithm works.

Please refer to the circuit of the algorithm shown earlier. 
Lets examine the state of the qubits at each step of the running of this circuit -- at $\psi_{1},\ \psi_{2},\ \psi_{3},\ \psi_{4}$

### Step 1 - $\psi_{1}$ - preparing output qubit

The sequence of X followed by H gates, prepares the output qubit in $\frac{1}{\sqrt{2}} \left( \ket{0} - \ket{1} \right) $ state. I.e.,

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

### Measurement of input qubit if $f(x)$ is constant and if it is balanced

We can now ignore the output qubit, since we are going to measure only
the input qubit. To zoom in on the state of the input qubit, let us expand the summation over $z$, and then expand the summation over $x$,

$$\frac{1}{2}\sum_{x = 0}^{1}\left( ( - 1)^{x\  \cdot 0 + f(x)}\ket{0} + ( - 1)^{(x \cdot 1) + f(x)}\ket{1} \right)

= \frac{1}{2}\sum_{x = 0}^{1}\left( ( - 1)^{f(x)}\ket{0} + ( - 1)^{x + f(x)}\ket{1} \right)$$

$$= \frac{1}{2}\left( ( - 1)^{f(0)}\ket{0} + ( - 1)^{f(0)}\ket{1} + ( - 1)^{f(1)}\ket{0} + ( - 1)^{1 + f(1)}\ket{1} \right)$$

Collecting together the coefficients of $\ket{0}$ and $\ket{1}$,

$$= \frac{1}{2}\left( \left( ( - 1)^{f(0)} + ( - 1)^{f(1)} \right)\ket{0} + \left( ( - 1)^{f(0)} + ( - 1)^{1 + f(1)} \right)\ket{1} \right)$$

Therefore, if $f(x)$ is constant and if it is balanced, the input qubit states are as

* If $f(x)$ is constant, the input qubit states are
  * $if\ f(0) = f(1) = 0:\ \ $
$\frac{1}{2}\left( \left( ( - 1)^{0} + ( - 1)^{0} \right)\ket{0} + \left( ( - 1)^{0} + ( - 1)^{1} \right)\ket{1} \right)\ \ \ \ \ \ = 1\ket{0} + 0\ket{1} = \ket{0}$
  * $if\ f(0) = f(1) = 1:$
$\ \ \frac{1}{2}\left( \left( ( - 1)^{1} + ( - 1)^{1} \right)\ket{0} + \left( ( - 1)^{1} + ( - 1)^{1 + 1} \right)\ket{1} \right)\ \ \ = - 1\ket{0} + 0\ket{1} = \  - \ket{0}$
* And, If $f(x)$ is balanced, the input qubit states are
  * $if\ f(0) = 0,\ f(1) = 1:\ $
$\ \frac{1}{2}\left( \left( ( - 1)^{0} + ( - 1)^{1} \right)\ket{0} + \left( ( - 1)^{0} + ( - 1)^{1 + 1} \right)\ket{1} \right) = 0\ket{0} + 1\ket{1} = \ket{1}$
  * $if\ f(0) = 1,f(1) = 0:$
$\ \ \frac{1}{2}\left( \left( ( - 1)^{1} + ( - 1)^{0} \right)\ket{0} + \left( ( - 1)^{1} + ( - 1)^{1 + 0} \right)\ket{1} \right) = 0\ket{0} + ( - 1)\ket{1} = - \ket{1}$

I.e.,
-   if $f(x)$ is constant the probability of measuring input qubit as 0
    is 100%, and,
-   if $f(x)$ is balanced the probability of measuring input qubit as 1
    is 100%

In this way Deutsch algorithm performs only **one** query to teh oracle to determine the type of the function.
## Key takeaways
1. Where is superposition used?  
input qubit initialized to all possible inputs
2. Where does phase kickback happen?  
oracle encodes function values into phase of input qubit
3. Where does interference happen?  
final Hadamards cause constructive/destructive interference to converge the state of input qubit into one computational basis state
4. What information is encoded?  
global property (constant vs balanced) encoded in phase pattern
5. How does measurement extract it?  
measurement reads out the interference result directly

# Deutsch-Jozsa algorithm



## Caveat

Note that Deutsch-Jozsa demonstrates speed up compared to 
*deterministic* classical algorithms, if compared with randomized
classical algorithms the advantage disappears. In a subsequent post we
will go over Simon's algorithm, which is considered the first strong
case of exponential speedup. In any case, Deutsch-Jozsa helps understand
some very important concepts which are often useful in designing quantum
algorithms.







# Stronger Case of Exponential Speedup: Simon's Algorithm

The [Deutsch-Jozsa
algorithm](https://en.wikipedia.org/wiki/Deutsch%E2%80%93Jozsa_algorithm) (DJ)
provides exponential speedup over a *deterministic* classical computer
on determining whether a function f is constant or balanced, with the
promise that exactly one of these is true. However soon as you allow
your classical computer to perform random sampling of f, and tolerate
small failure probability, the quantum advantage disappears. Since
random sampling is a realistic feature of classical computers, one could
argue DJ does not show a true advantage over classically accessible
models of computation.

[Simon\'s algorithm](https://en.wikipedia.org/wiki/Simon%27s_problem),
on the other hand, demonstrates exponential speedup even over
probabilistic computers. More formally, Simon\'s provides an oracle
separation between BQP (class of problems efficiently solvable by
quantum computers) and BPP (class of problems efficiently solvable by
classical computers).
