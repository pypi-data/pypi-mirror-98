.. highlight:: python

.. _Representations:

===============
Representations
===============

One of the painful parts of developing an app that modifies glyphs is managing the visual representation of the glyphs. When the glyph changes, all representations of it in cached data, the user interface, etc. need to change. There are several ways to handle this, but they are all cumbersome. defcon gives you a very simple way of dealing with this: *representations* and *representation factories*.

.. note::

   Representations have been extended to allow other font object classes, so that fonts, layers, glyphs, contours, etc. can have representations too.

Representations and Representation Factories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A *representation* is an object that represents a glyph. As mentioned above, it can be a visual representation of a glyph, such as a NSBezierPath. Representations aren't just limited to visuals, they can be any type of data that describes a glyph or something about a glyph, for example a string of GLIF text, a tree of point location tuples or anything else you can imagine. A *representation factory* is a function that creates a representation. You don't manage the representations yourself. Rather, you register the factory and then ask the glyphs for the representations you need. When the glyphs change, the related representations are destroyed and recreated as needed.

Example
^^^^^^^

As an example, here is a representation factory that creates a NSBezierPath representation::

  def NSBezierPathFactory(glyph):
      from fontTools.pens.cocoaPen import CocoaPen
      pen = CocoaPen(glyph.getParent())
      glyph.draw(pen)
      return pen.path

To register this factory, you do this::

  from defcon import Glyph, registerRepresentationFactory
  registerRepresentationFactory(Glyph, "NSBezierPath", NSBezierPathFactory)

Now, when you need a representation, you simply do this::

  path = glyph.getRepresentation("NSBezierPath")

Not only do you only have to register this *once* to be able get the representation for *all* glyphs, the representation is always up to date. So, if you change the outline in the glyph, all you have to do to get the updated representation is::

  path = glyph.getRepresentation("NSBezierPath")


Implementation Details
^^^^^^^^^^^^^^^^^^^^^^

Representation Factories
""""""""""""""""""""""""

Representation factories should be functions that accept a font object class (such as  :class:`~defcon.Glyph`, :class:`~defcon.Font`, :class:`~defcon.Contour` etc.) as first argument. After that, you are free to define any keyword arguments you need. You must register the factory with the ``registerRepresentationFactory`` function. When doing this, you must define a unique name for your representation. The recommendation is that you follow the format of "applicationOrPackageName.representationName" to prevent conflicts. Some examples::

  registerRepresentationFactory(Glyph, "MetricsMachine.groupEditorGlyphCellImage", groupEditorGlyphCellImageFactory)
  registerRepresentationFactory(Glyph, "Prepolator.previewGlyph", previewGlyphFactory)

Representations
""""""""""""""""

Once the factory has been registered, glyphs will be able to serve the images. You can get the representation like this::

  image = glyph.getRepresentation("MetricsMachine.groupEditorGlyphCellImage")

You can also pass keyword arguments when you request the representation. For example::

  image = glyph.getRepresentation("MetricsMachine.groupEditorGlyphCellImage", cellSize=(40, 40))

These keyword arguments will be passed along to the representation factory. This makes it possible to have very dynamic factories.

All of this is highly optimized. The representation will be created the first time you request it and then it will be cached within the glyph. The next time you request it, the cached representation will be returned. If the glyph is changed, the representation will automatically be destroyed. When this happens, the representation will not be recreated automatically. It will be recreated the next time you ask for it.

Destroying representations
""""""""""""""""""""""""""

You can now also specify which notifications should destroy representations. (Previously, any change to a glyph would destroy all representations. That wasn't ideal. Changing the glyph.note would destroy the expensive-to-calculate bounding box representation.)

Each class has a list of notifications that it posts. When you register a factory, you can give a list of notification names that should destroy representations created by the factory you are registering. Here's an example::

  def layerCMAPRepresentationFactory(layer):
     cmap = {}
     for g in layer:
         if g.unicode is not None:
             cmap[chr(g.unicode)] = g.name
     return cmap

  registerRepresentationFactory(Layer, "CMAP", layerCMAPRepresentationFactory, destructiveNotifications=["Layer.GlyphUnicodesChanged"])
