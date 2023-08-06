<!-- !split -->
<!-- jupyter-book 02_04_testdoc.md -->
# Custom Environments

Here is an attempt to create a theorem environment via Mako
(for counting theorems) and comment lines to help replacing lines in
the `.tex` by proper begin-end LaTeX environments for theorems.
Should look nice in most formats!

<!-- begin theorem -->
<div id="theorem:fundamental1"></div>

*Theorem 5.*
Let $a=1$ and $b=2$. Then $c=3$.
<!-- end theorem -->

<!-- begin proof -->
*Proof.*
Since $c=a+b$, the result follows from straightforward addition.
$\Diamond$
<!-- end proof -->

As we see, the proof of Theorem 5 is a modest
achievement.

