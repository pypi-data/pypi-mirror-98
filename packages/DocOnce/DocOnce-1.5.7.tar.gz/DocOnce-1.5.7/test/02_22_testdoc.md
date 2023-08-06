<!-- !split -->
<!-- jupyter-book 02_22_testdoc.md -->
# URLs

<div id="subsubsec:ex"></div>

Testing of URLs: hpl's home page [hpl](https://folk.uio.no/hpl), or
the entire URL if desired, <https://folk.uio.no/hpl>.  Here is a
plain file link <testdoc.do.txt>, or <testdoc.do.txt>, or
<testdoc.do.txt> or <testdoc.do.txt> or [a link with
newline](testdoc.do.txt). Can test spaces with the link with word
too: [hpl](https://folk.uio.no/hpl) or [hpl](https://folk.uio.no/hpl). Also `file:///` works: [link to a
file](file:///home/hpl/vc/doconce/doc/demos/manual/manual.html) is
fine to have. Moreover, "loose" URLs work, i.e., no quotes, just
the plain URL as in <https://folk.uio.no/hpl>, if followed by space, comma,
colon, semi-colon, question mark, exclamation mark, but not a period
(which gets confused with the periods inside the URL).

Mail addresses can also be used: [`hpl@simula.no`](mailto:hpl@simula.no), or just a [mail link](mailto:hpl@simula.no), or a raw <mailto:hpl@simula.no>.

Here are some tough tests of URLs, especially for the `latex` format:
[Newton-Cotes](https://en.wikipedia.org/wiki/Newton%E2%80%93Cotes_formulas) formulas
and a [good book](https://www.springer.com/mathematics/computational+science+%26+engineering/book/978-3-642-23098-1). Need to test
Newton-Cotes with percentage in URL too:
<https://en.wikipedia.org/wiki/Newton%E2%80%93Cotes_formulas>
and <https://en.wikipedia.org/wiki/Newton-Cotes#Open_Newton.E2.80.93Cotes_formulae> which has a shebang.

For the `--device=paper` option it is important to test that URLs with
monospace font link text get a footnote
(unless the `--latex_no_program_footnotelink`
is used), as in this reference to
[`decay_mod`](https://github.com/hplgit/INF5620/tree/gh-pages/src/decay/experiments/decay_mod.py), [`ball1.py`](https://tinyurl.com/pwyasaa/formulas.ball1.py),
and [`ball2.py`](https://tinyurl.com/pwyasaa/formulas.ball2.py).

<!-- Comments should be inserted outside paragraphs (because in the rst -->
<!-- format extra blanks make a paragraph break). -->

<!-- Note that when there is no https: or file:, it can be a file link -->
<!-- if the link name is URL, url, "URL", or "url". Such files should, -->
<!-- if rst output is desired, but placed in a `_static*` folder. -->

More tough tests: repeated URLs whose footnotes when using the
`--device=paper` option must be correct. We have
[google](https://google.com), [google](https://google.com), and
[google](https://google.com), which should result in exactly three
footnotes.

<!-- !split and check if these extra words are included properly in the comment -->

