.. Automatically generated Sphinx-extended reStructuredText file from DocOnce source
   (https://github.com/doconce/doconce/)

.. Text with wrong doconce format

.. TODO: fix this

A list followed by a code block works okay:

  * Third point

  * Fourth point

.. code-block:: python

    some verbatime stuff

.. _my:

Section heading before code is caught by the syntax check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: failure

Hello

.. code-block:: text

    more verbatime stuff

Next we see if backslashes are detected: 
.. index:: youridx

And a reference to [Ref1]_.

.. code-block:: text

    More verbatim stuff.

Can we successfully say ``__call__`` and ``__add__`` and avoid having them as
bad paragraphs?

Figure with just an image and no caption must be handled.

.. figure:: ../doc/src/manual/fig/wave1D.png

Figure with label, but no caption.

.. _myl1:

.. figure:: ../doc/src/manual/fig/wave1D.png

Figure with no comma between filename and options, and wrong path must
give error.

.. figure:: ../doc/src/manual/fig/wave1D.png
   :width: 800

Figure with math only in the caption, which causes sphinx to use an
empty figure name, is problematic.

.. figure:: ../doc/src/manual/fig/wave1D.png
   :width: 800

   :math:`a=50`

Figure with hyperlink in caption creates problems with latex and --device=paper
because the link becomes a footnote inside the caption.

.. figure:: ../doc/src/manual/fig/wave1D.png
   :width: 800

   `Google <https://google.com>`__

.. `<https://hplgit.github.io/INF5620/doc/pub/mov-wave/pulse2_in_two_media/movie.webm>`_

Movie/figure with nonexistent URL must give error messages.

.. raw:: html
        
        <div>
        <video  loop controls width='800' height='365' preload='none'>
            <source src='https://hplgit.github.io/INF5620/doc/pub/mov-wave/pulse2_in_two_media/movie.webm' type='video/webm; codecs="vp8, vorbis"'>
            <source src='https://hplgit.github.io/INF5620/doc/pub/mov-wave/pulse2_in_two_media/movie.ogg'  type='video/ogg;  codecs="theora, vorbis"'>
        </video>
        </div>
        <p><em>:math:`a=50`</em></p>
        
        <!-- Issue warning if in a Safari browser -->
        <script language="javascript">
        if (!!(window.safari)) {
          document.write("<div style=\"width: 95%%; padding: 10px; border: 1px solid #100; border-radius: 4px;\"><p><font color=\"red\">The above movie will not play in Safari - use Chrome, Firefox, or Opera.</font></p></div>")}
        </script>
        

.. figure:: https://hplgit.github.io/INF5620/doc/pub/fig-wave/pulse2_in_two_media.png
   :width: 800

   :math:`a=50`

Links with mix of verbatim and plain text is not good: `myfile.py <https://some.where.net/myfile.py>`__.

More text...

.. Comment before math is ok

.. math::
   :label: eq1

        
        a = b,  
        

.. math::
   :label: eq2

         
        a = b,  
        

 * A1

 * A2

Normal text.

Normal section with exercise envirs are detected by syntax checks
-----------------------------------------------------------------

Normal text.

Just a loner subexercise begin.

Normal text.

Links to local files shall give warning
---------------------------------------

Try this `link <_static/doconce.py>`__.

Failure of tables
-----------------

===========  ===================  
  heading1         heading2       
===========  ===================  
``%s``       ``%e``               
:math:`a=b`  :math:`\mbox{math}`  
===========  ===================  
