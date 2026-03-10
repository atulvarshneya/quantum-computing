<h1 style="text-align: center;">
Quantum Computing Blog
</h1>

Welcome to a practitioner’s guide to quantum computing.

This blog is designed for curious computer scientists, software engineers, and technology enthusiasts who want to understand quantum computing from the inside out — not as abstract physics, but as something you can actually build, simulate, and experiment with. The focus here is hands-on and algorithm-centric: we will explore the most important quantum computing algorithms, unpack how and why they work, and implement them step by step using [Qucircuit](https://github.com/atulvarshneya/quantum-computing/blob/master/qucircuit/README.md), a full-featured quantum computing simulator that runs locally on your own machine. Along the way, a dedicated series of “Short Notes” will distill key concepts from quantum mechanics and quantum information into clear, practical explanations that strengthen your intuition without requiring a deep background in physics. If you enjoy learning by building, reasoning from first principles, and understanding systems at a conceptual level, this site is for you.

<div style="text-align: right">
- Atul Varshneya<br>
<a href="https://www.linkedin.com/in/atulvarshneya/">LinkedIn</a>
</div>

## Blog Posts
* QAOA Step by Step<br>
This is a short series of posts that explains Quantum Approximate Optimization Algorithm (QAOA) 
from a practitioner's perspective. The posts focus on guiding the reader to implement this algorithm
using MAXCUT problem as an example, followed by getting a bit deeper into its mathematical details.

  * [QAOA Step by Step: Concepts, Circuits, and Code for Quantum Enthusiasts](https://github.com/atulvarshneya/quantum-computing/blob/master/blogs/QAOAblog-01.md), February 27, 2026<br>
Quantum computers promise extraordinary capabilities.
But today's hardware are still at an early stage.
Qubits are fragile, gates are noisy, and circuits must remain shallow
before errors dominate. This era, often called the *NISQ era* (Noisy
Intermediate-Scale Quantum), poses a clear challenge \-- how can we make
practical use of these imperfect quantum devices right now? 
One of the promising answers is a family of methods called *Variational
Quantum Algorithms (VQAs)*.<br>
Variational quantum algorithms are already being applied to several
important domains. In this blog series, we discuss the *Quantum Approximate
Optimization Algorithm (QAOA)* which is a VQA approach applied to combinatorial optimization. 
Because QAOA is conceptually simple, mathematically elegant, and
practical to implement, it has become a popular example for learning
quantum optimization.

  * [QAOA Step by Step: A Closer Look into Cost and Mixer Operators](https://github.com/atulvarshneya/quantum-computing/blob/master/blogs/QAOAblog-02.md), March 10, 2026<br>
  In the previous post in this series, we explored the overall structure of QAOA:
superposition, alternating cost and mixer operators, layered depth, and
classical parameter optimization. We kept the discussion intentionally
at a high-level so we could clearly see the architecture without getting
buried in equations.<br>
In this post we zoom-in a bit into some mathematical details of the Cost and
Mixer Hamiltonians and their corresponding unitaries used in the QAOA's
quantum circuit. We continue to use MAXCUT as the running example to explore QAOA.

* [Grover's Algorithm: Quantum Speedup of Unstructured Search](https://github.com/atulvarshneya/quantum-computing/blob/master/blogs/GroversAlgorithm-blog.md), December 10, 2025<br>
In this post, we take an educational approach for a well-known quantum
algorithm, *Grover's algorithm*. We first explain how Grover's
algorithm works, then we introduce the *dinner party problem* which
involves identifying a set of friends that can be invited together to a
party satisfying a set of constraints. And then we explain how
Grover's algorithm can be used to solve it.

## Short Notes

* Is Superposition more fundamental than Entanglement: A Perspective, *To be posted soon. Stay tuned.*<br>

* Why I find it easer to understand Quantum Computing through Many-Worlds interpretation, *To be posted soon. Stay tuned.*<br>

* What is measurement afterall, *To be posted soon. Stay tuned.*<br>

* Noise in Quantum Computers, *To be posted soon. Stay tuned.*<br>
<!--
https://youtu.be/3MWbGkjMu-w?t=1063
-->
