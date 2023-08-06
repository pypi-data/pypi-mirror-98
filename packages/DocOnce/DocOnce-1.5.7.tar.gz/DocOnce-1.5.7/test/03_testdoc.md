<!-- !split -->
<!-- jupyter-book 03_testdoc.md -->
# LaTeX Mathematics

Here is an equation without label using backslash-bracket environment:
$$
 a = b + c 
$$

or with number and label, as in ([my:eq1](my:eq1.html#my:eq1)), using the equation environment:

$$
\begin{equation}
{\partial u\over\partial t} = \nabla^2 u \label{my:eq1}
\end{equation}
$$

We can refer to this equation by ([my:eq1](my:eq1.html#my:eq1)).

Here is a system without equation numbers, using the align-asterisk environment:

$$
\begin{align*}
\pmb{a} &= \pmb{q}\times\pmb{n} \\ 
b &= \nabla^2 u + \nabla^4 v
\end{align*}
$$

And here is a system of equations with labels in an align environment:

$$
\begin{align}
a &= q + 4 + 5+ 6 \label{eq1} \\ 
b &= \nabla^2 u + \nabla^4 x \label{eq2}
\end{align}

$$
We can refer to ([eq1](eq1.html#eq1))-([eq2](eq2.html#eq2)). They are a bit simpler than
the Navier&ndash;Stokes equations. And test LaTeX hyphen in `CG-2`.
Also test $a_{i-j}$ as well as $kx-wt$.

Testing `alignat` environment:

$$
\begin{alignat}{2}
a &= q + 4 + 5+ 6\qquad & \mbox{for } q\geq 0 \label{eq1a} \\ 
b &= \nabla^2 u + \nabla^4 x & x\in\Omega \label{eq2a}
\end{alignat}
$$

More mathematical typesetting is demonstrated in the coming exercises.

Below, we have [Problem: Flip a Coin](demo:ex:1.html#demo:ex:1) and [demo:ex:2](04_04_testdoc.html#demo:ex:2),
as well as [Project: Explore Distributions of Random Circles](proj:circle1.html#proj:circle1) and [Project: References to Project [demo:ex:2](04_04_testdoc.html#demo:ex:2) in a heading works for pandoc](#exer:you), and in
between there we have [Exercise: Make references to projects and problems](06_01_testdoc.html#exer:some:formula).

