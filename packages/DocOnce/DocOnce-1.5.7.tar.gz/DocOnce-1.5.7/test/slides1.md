% Document for Testing Some Basic and Some Challenging Constructs in DocOnce Slides
% **Hans Petter Langtangen** at Simula Research Laboratory and University of Oslo
% Mar 16, 2021

Made with DocOnce



<!-- !split -->
## This is the first section
<!-- Short title: First -->

<!-- !split -->
### Figure and bullet list

<!-- !bslidecell 00  0.60 -->
<!-- !bpop -->
*Title with comma, and brackets: $[a,b]$* 
  * Here is a *wave signal* $f(x-ct)$
  * It moves with velocity $c$
  * But here it is just a figure


<!-- !epop -->
<!-- !eslidecell -->

<!-- !bslidecell 01 -->
<!-- <img src="../doc/src/manual/fig/wave1D.png" width=300> -->
![](../doc/src/manual/fig/wave1D.png)


<!-- !eslidecell -->

<!-- !split -->
### Slide with pop-ups in red and notes

[hpl 1: Comments are typeset as usual in DocOnce.]

<!-- !bpop highlight-red -->
Here we have a paragraph to pop up in red.<br />
And a line more
<!-- !epop -->

<!-- !bnotes -->
One can also have ordinary notes.
Over multiple lines.
<!-- !enotes -->

<!-- !split -->
### A LaTeX document

<!-- !bpop -->

```
\documentclass[11pt]{article}
\usepackage{fancyvrb}
\begin{document}

\title{Here goes the title...}
\author{John Doe \and
Jane Doe\footnote{\texttt{jane.doe@cyber.net}.}}
\date{\today}
\maketitle
```

<!-- !epop -->

<!-- !bpop -->
*Notice.* 
LaTeX has a lot of backslashes.


<!-- !epop -->

<!-- !bpop -->

```
\section{Heading}
bla-bla
\end{document}
```

<!-- !epop -->

<!-- !split -->
### An HTML document


```html
<html><head></head><body bgcolor="red">
<title>Here goes the title...<title>
<h1>Section heading</h1>
</body>
</html>
```

<!-- !split -->
## Second section

<!-- <img src="../doc/src/manual/fig/wave1D.png" width=600> -->
![](../doc/src/manual/fig/wave1D.png)



<!-- !split -->
### Some math and computer code

*A simple, mathematical formula where $t\in [0,\pi]$:* 
$$
 f(x,y,t) = e^{-xt}\sin\pi y 
$$



*Bash demanded more of DocOnce than Python, so let's do Bash:* 
First, inline `$? != 0`, then comments with dollar variables (and minted
style):


```shell
var=10
# $1, $2, ... are command-line args
if [ $? -eq 0 ]; then   # $? reflects success or not
  echo "Great!"
fi
```



<!-- !split -->
### Pop ups inside code blocks (for Beamer slides only)


```python
def f(x):
    return 42 + x

def g(x):
    return f(42)

print(g(13))
```

<!-- !split -->
### Various admon blocks

Can use admons to simulate blocks:

<!-- !bpop -->
*Key PDE (with large title and math font):* 
$$
 \frac{\partial u}{\partial t} = \nabla^2 u 
$$


<!-- !epop -->

<!-- !bpop -->
*None* 
Just some block with text and a conclusion that something is important.
This one pops up after the rest of the slide.


<!-- !epop -->

<!-- !bpop -->
Can use, e.g., a warning admon to have my own notes, preferably
inside preprocess/mako if statements to turn notes on and off.
This one is typeset in a small font and with the default
title (Warning) since no title is specified.


<!-- !epop -->

