
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