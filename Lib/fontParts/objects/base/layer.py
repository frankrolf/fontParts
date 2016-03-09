import weakref
from base import BaseObject, dynamicProperty, FontPartsError
import validators
from color import Color


class BaseLayer(BaseObject):

    """
    XXX

    Add some tips on how to make this object when the
    editor has a glyph level layer model instead of
    a font level layer model.

    In fact, the base behavior should be built for
    a glyph level layer model.

    XXX
    """

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.font

    # Font

    _font = None

    font = dynamicProperty("font", "The layer's parent font.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        assert self._font is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

    # --------------
    # Identification
    # --------------

    # name

    name = dynamicProperty("base_name", "The name of the layer.")

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = validators.validateLayerName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        if value is not None:
            value = validators.validateLayerName(value)
            existing = self.font.layerOrder
            if value in existing:
                raise FontPartsError("A layer with the name %r already exists." % value)
        self._set_name(value)

    def _get_name(self):
        """
        Get the name of the layer.
        This must return a unicode string or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value, **kwargs):
        """
        Set the name of the layer.
        This will be a unicode string or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty("base_color", "The layer's color.")

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = validators.validateColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = validators.validateColor(value)
        self._set_color(value)

    def _get_color(self):
        """
        Get the color of the layer.
        This must return a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value, **kwargs):
        """
        Set the color of the layer.
        This will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    lib = dynamicProperty("lib", "The layer's lib object.")

    def _get_lib(self):
        self.raiseNotImplementedError()

    # -----------------
    # Glyph Interaction
    # -----------------

    def __len__(self):
        """
        The number of glyphs in the layer.
        """
        return self._len()

    def _len(self, **kwargs):
        """
        This must return an integer.

        Subclasses may override this method.
        """
        return len(self.keys())

    def __iter__(self):
        """
        Iterate through the glyphs in the layer.
        """
        return self._iter()

    def _iter(self, **kwargs):
        """
        This must return an iterator that returns wrapped glyphs.

        Subclasses may override this method.
        """
        names = self.keys()
        while names:
            name = names[0]
            yield self[name]
            names = names[1:]

    def __getitem__(self, name):
        """
        Get the glyph with name from the  layer.
        """
        name = validators.validateGlyphName(name)
        if name not in self:
            raise FontPartsError("No glyph named %r." % name)
        return self._getItem(name)

    def _getItem(self, name, **kwargs):
        """
        This must return a wrapped glyph.

        name will be a valid glyph name that is in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def keys(self):
        """
        Get a list of all glyphs in the layer of the font.
        The order of the glyphs is undefined.
        """
        return self._keys()

    def _keys(self, **kwargs):
        """
        This must return a list of all glyph names in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __contains__(self, name):
        """
        Test if the layer contains a glyph with name.
        """
        name = validators.validateGlyphName(name)
        return self._contains(name)

    def _contains(self, name, **kwargs):
        """
        This must return an boolean.

        Subclasses may override this method.
        """
        return name in self.keys()

    has_key = __contains__

    def newGlyph(self, name, clear=True):
        """
        Make a new glyph in the layer. The glyph will
        be returned.

        clear indicates if the data in an existing glyph
        with the same name should be cleared. If so,
        the clear method of the glyph should be called.
        """

    def removeGlyph(self, name):
        """
        Remove the glyph with name from the layer.
        """

    def insertGlyph(self, glyph, name=None):
        """
        Insert a new glyph into the layer. The glyph will
        be returned.

        name indicates the name that should be assigned to
        the glyph after insertion. If name is not given,
        the glyph's original name must be used. If the glyph
        does not have a name, an error must be raised.

        This does not insert the given glyph object. Instead,
        a new glyph is created and the data from the given
        glyph is recreated in the new glyph.
        """

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers. This is the
        equivalent of calling the round method on each object
        within the layer.
        """

    def autoUnicodes(self):
        """
        Use heuristics to determine Unicode values to all glyphs
        and set the values in the glyphs. Environments will define
        their own heuristics for automatically determining values.
        """

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minLayer, maxLayer, suppressError=True, analyzeOnly=False, showProgress=False):
        """
        Interpolate all possible data in the layer. The interpolation
        occurs on a 0 to 1.0 range where minLayer is located at
        0 and maxLayer is located at 1.0.

        factor is the interpolation value. It may be less than 0
        and greater than 1.0. It may be a number (integer, float)
        or a tuple of two numbers. If it is a tuple, the first
        number indicates the x factor and the second number
        indicates the y factor.

        suppressError indicates if incompatible data should be ignored
        or if an error should be raised when such incompatibilities are found.

        analyzeOnly indicates if the intrpolation should only be a
        compatibiltiy check with no interpolation actually performed.
        If this is True, a dict of compatibility problems will
        be returned.
        """

    # ------------------
    # Reference Mappings
    # ------------------

    def getCharacterMapping(self):
        """
        Get a dictionary showing unicode to glyph mapping.

            {
                unicode value : [glyph names]
            }
        """

    def getReverseComponentMapping(self):
        """
        Get a dictionary showing component references.

            {
                base glyph name : [glyph names]
            }
        """