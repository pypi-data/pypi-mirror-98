<!-- !split -->
<!-- jupyter-book 02_20_testdoc.md -->
# Example: Examples can be typeset as exercises

<div id="Example"></div>

Examples can start with a subsection heading starting with `Example:`
and then, with the command-line option `--examples_as_exercises` be
typeset as exercises. This is useful if one has solution
environments as part of the example.

!bsubex
State some problem.

!bsol
The answer to this subproblem can be written here.
!esol
!esubex

!bsubex
State some other problem.

*Hint.* 
A hint can be given.



*Hint.* 
Maybe even another hint?



!bsol
The answer to this other subproblem goes here,
maybe over multiple doconce input lines.
!esol
!esubex

