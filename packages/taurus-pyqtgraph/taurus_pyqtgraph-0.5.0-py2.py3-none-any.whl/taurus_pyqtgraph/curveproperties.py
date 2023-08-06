#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""
A Qt dialog for choosing plot appearance (symbols and lines)
for a Pyqtgraph.PlotDataItem or taurus-derived class
like TaurusPlotDataItem

.. warning:: this is Work-in-progress. The API from this module may still
             change. Please
"""
from __future__ import absolute_import

# TODO: WIP

from builtins import str
from builtins import object

__all__ = [
    "CurveAppearanceProperties",
    "CurvesAppearanceChooser",
    "serialize_opts",
    "deserialize_opts",
    "get_properties_from_curves",
    "set_properties_on_curves",
    "set_y_axis_for_curve",
    "CURVE_COLORS",
]

import copy

from taurus import warning
from taurus.external.qt import Qt
from taurus.qt.qtgui.util.ui import UILoadable
from .y2axis import Y2ViewBox, set_y_axis_for_curve
import pyqtgraph


class CONFLICT(object):
    """
    This is just a do-nothing class to be used to indicate that there are
    conflicting values when merging properties from different curves
    """

    pass


NamedLineStyles = {
    CONFLICT: "",
    Qt.Qt.NoPen: "No line",
    Qt.Qt.SolidLine: "_____",
    Qt.Qt.DashLine: "_ _ _",
    Qt.Qt.DotLine: ".....",
    Qt.Qt.DashDotLine: "_._._",
    Qt.Qt.DashDotDotLine: ".._..",
}

ReverseNamedLineStyles = {}
for k, v in NamedLineStyles.items():
    ReverseNamedLineStyles[v] = k

# TODO:allow the dialog to use this curve styles
NamedStepMode = {
    CONFLICT: "",
    None: "No step",
    "left": "Left step",
    "right": "Right step",
}

ReverseNamedStepMode = {}
for k, v in NamedStepMode.items():
    ReverseNamedStepMode[v] = k

NamedSymbolStyles = {
    CONFLICT: "",
    None: "No symbol",
    "o": "Circle",
    "s": "Square",
    "d": "Diamond",
    "t": "Down Triangle",
    "t1": "Up triangle",
    "t3": "Left Triangle",
    "t2": "Right Triangle",
    "+": "Cross",
    "star": "Star",
    "p": "Pentagon",
    "h": "Hexagon",
}

ReverseNamedSymbolStyles = {}
for k, v in NamedSymbolStyles.items():
    ReverseNamedSymbolStyles[v] = k

NamedColors = [
    "Red",
    "Blue",
    "Green",
    "Magenta",
    "Cyan",
    "Yellow",
    "Orange",
    "greenyellow",
    "Gray",
    "White",
    "Black",
]

kelly_colors_hex = [  # https://stackoverflow.com/a/4382138
    0xFFB300,  # Vivid Yellow
    0x803E75,  # Strong Purple
    0xFF6800,  # Vivid Orange
    0xA6BDD7,  # Very Light Blue
    0xC10020,  # Vivid Red
    0xCEA262,  # Grayish Yellow
    0x817066,  # Medium Gray
    # The following don't work well for people with defective color vision
    0x007D34,  # Vivid Green
    0xF6768E,  # Strong Purplish Pink
    0x00538A,  # Strong Blue
    # 0xFF7A5C, # Strong Yellowish Pink
    # 0x53377A, # Strong Violet
    # 0xFF8E00, # Vivid Orange Yellow
    0xB32851,  # Strong Purplish Red
    # 0xF4C800, # Vivid Greenish Yellow
    # 0x7F180D, # Strong Reddish Brown
    0x93AA00,  # Vivid Yellowish Green
    0x593315,  # Deep Yellowish Brown
    # 0xF13A13, # Vivid Reddish Orange
    # 0x232C16, # Dark Olive Green
]

CURVE_COLORS = [Qt.QColor(n) for n in NamedColors[:-2]]
# CURVE_COLORS = [Qt.QColor(n) for n in kelly_colors_hex]


@UILoadable
class CurvesAppearanceChooser(Qt.QWidget):
    """
    A widget for choosing plot appearance for one or more curves.
    The current curves properties are passed using the setCurvesProps()
    method using a dictionary with the following structure::

        curvePropDict={name1:prop1, name2:prop2,...}

    where propX is an instance of :class:`CurveAppearanceProperties`
    When applying, a signal is emitted and the chosen properties are made
    available in a similar dictionary. """

    NAME_ROLE = Qt.Qt.UserRole

    controlChanged = Qt.pyqtSignal()
    curveAppearanceChanged = Qt.pyqtSignal(object, list)
    CurveTitleEdited = Qt.pyqtSignal("QString", "QString")

    def __init__(
        self,
        parent=None,
        curvePropDict=None,
        showButtons=False,
        autoApply=False,
        curvesDict=None,
        plotItem=None,
        Y2Axis=None,
    ):
        super(CurvesAppearanceChooser, self).__init__(parent)
        self.loadUi()
        self.autoApply = autoApply
        self._curvesDict = curvesDict
        self.plotItem = plotItem
        self.Y2Axis = Y2Axis

        self.sStyleCB.insertItems(0, sorted(NamedSymbolStyles.values()))
        self.lStyleCB.insertItems(0, list(NamedLineStyles.values()))
        self.stepModeCB.insertItems(0, list(NamedStepMode.values()))
        self.sColorCB.addItem("")
        self.lColorCB.addItem("")
        self.cAreaDSB.setRange(float("-inf"), float("inf"))
        if not showButtons:
            self.applyBT.hide()
            self.resetBT.hide()
        for color in CURVE_COLORS:
            icon = self._colorIcon(color)
            self.sColorCB.addItem(icon, "", Qt.QColor(color))
            self.lColorCB.addItem(icon, "", Qt.QColor(color))
        self.setCurvesProps(curvePropDict)

        if self.plotItem is None:
            self.bckgndBT.setVisible(False)

        # connections.
        self.curvesLW.itemSelectionChanged.connect(
            self._onSelectedCurveChanged
        )
        self.applyBT.clicked.connect(self.onApply)
        self.resetBT.clicked.connect(self.onReset)
        self.sStyleCB.currentIndexChanged.connect(self._onSymbolStyleChanged)

        self.curvesLW.itemChanged.connect(self._onControlChanged)
        self.sStyleCB.currentIndexChanged.connect(self._onControlChanged)
        self.lStyleCB.currentIndexChanged.connect(self._onControlChanged)
        self.sColorCB.currentIndexChanged.connect(self._onControlChanged)
        self.lColorCB.currentIndexChanged.connect(self._onControlChanged)
        self.stepModeCB.currentIndexChanged.connect(self._onControlChanged)
        self.sSizeSB.valueChanged.connect(self._onControlChanged)
        self.lWidthSB.valueChanged.connect(self._onControlChanged)
        self.cAreaDSB.valueChanged.connect(self._onControlChanged)
        self.sFillCB.stateChanged.connect(self._onControlChanged)
        self.cFillCB.stateChanged.connect(self._onControlChanged)

        self.assignToY1BT.toggled[bool].connect(self.__onY1Toggled)
        self.assignToY2BT.toggled[bool].connect(self.__onY2Toggled)

        self.bckgndBT.clicked.connect(self.changeBackgroundColor)

        # Disabled button until future implementations
        self.changeTitlesBT.setVisible(False)

        # disable the group box with the options for swap curves between Y axes
        if Y2Axis is None or plotItem is None:
            self.groupBox.setEnabled(False)

        self._onSelectedCurveChanged()
        self.axis = None

    def __onY1Toggled(self, checked):
        if checked:
            self.assignToY2BT.setChecked(False)

    def __onY2Toggled(self, checked):
        if checked:
            self.assignToY1BT.setChecked(False)

    def __findCurveListItem(self, key, role=None):
        if role is None:
            role = self.NAME_ROLE
        for i in range(self.curvesLW.count()):
            item = self.curvesLW.item(i)
            if item.data(role) == key:
                return item

    def changeBackgroundColor(self):
        """Launches a dialog for choosing the plot widget background color
        """
        color = Qt.QColorDialog.getColor(
            initial=self.plotItem.scene().parent().backgroundBrush().color(),
            parent=self,
        )
        if Qt.QColor.isValid(color):
            self.plotItem.scene().parent().setBackground(color)

    def setCurvesProps(self, curvePropDict):
        """Populates the list of curves from the properties dictionary. It uses
        the curve title for display, and stores the curve name as the item data
        (with role=CurvesAppearanceChooser.NAME_ROLE)

        :param curvePropDict:  (dict) a dictionary whith keys=curvenames and
                               values= :class:`CurveAppearanceProperties`
                               object
        """
        self.curvePropDict = curvePropDict
        self._curvePropDictOrig = copy.deepcopy(curvePropDict)
        self.curvesLW.clear()
        for name, prop in self.curvePropDict.items():
            # create and insert the item
            item = Qt.QListWidgetItem(prop.title, self.curvesLW)
            item.setData(self.NAME_ROLE, name)
            item.setFlags(
                Qt.Qt.ItemIsEnabled
                | Qt.Qt.ItemIsSelectable
                | Qt.Qt.ItemIsUserCheckable
                | Qt.Qt.ItemIsDragEnabled
                | Qt.Qt.ItemIsEditable
            )
        self.curvesLW.setCurrentRow(0)

    def getSelectedCurveNames(self):
        """Returns the curve names for the curves selected at the curves list.

        *Note*: The names may differ from the displayed text, which
        corresponds to the curve titles (this method is what you likely need if
        you want to get keys to use in curves or curveProp dicts).

        :return: (string_list) the names of the selected curves
        """
        return [
            item.data(self.NAME_ROLE) for item in self.curvesLW.selectedItems()
        ]

    def showProperties(self, prop=None):
        """Updates the dialog to show the given properties.

        :param prop: (CurveAppearanceProperties) the properties object
                     containing what should be shown. If a given property is
                     set to CONFLICT, the corresponding plot_item will show a
                     "neutral" display
        """

        if prop is None:
            prop = self._shownProp
        # set the Style comboboxes
        self.sStyleCB.setCurrentIndex(
            self.sStyleCB.findText(NamedSymbolStyles[prop.sStyle])
        )
        self.lStyleCB.setCurrentIndex(
            self.lStyleCB.findText(NamedLineStyles[prop.lStyle])
        )
        self.stepModeCB.setCurrentIndex(
            self.stepModeCB.findText(NamedStepMode[prop.stepMode])
        )

        if prop.y2 is CONFLICT:
            self.assignToY1BT.setChecked(False)
            self.assignToY2BT.setChecked(False)
        elif prop.y2:
            self.assignToY2BT.setChecked(True)
        else:
            self.assignToY1BT.setChecked(True)

        # set sSize and lWidth spinboxes. if prop.sSize is None, it puts -1
        # (which is the special value for these switchhboxes)
        if prop.sSize is CONFLICT or prop.sStyle is None:
            self.sSizeSB.setValue(-1)
        else:
            self.sSizeSB.setValue(max(prop.sSize, -1))
        if prop.lWidth is CONFLICT:
            self.lWidthSB.setValue(-1)
        else:
            self.lWidthSB.setValue(max(prop.lWidth, -1))

        # Set the Color combo boxes. The item at index 0 is the empty one in
        # the comboboxes Manage unknown colors by including them
        if prop.sColor in (None, CONFLICT) or prop.sStyle is None:
            index = 0
        else:
            index = self.sColorCB.findData(Qt.QColor(prop.sColor))
        if index == -1:  # if the color is not supported, add it to combobox
            index = self.sColorCB.count()
            self.sColorCB.addItem(
                self._colorIcon(Qt.QColor(prop.sColor)),
                "",
                Qt.QColor(prop.sColor),
            )
        self.sColorCB.setCurrentIndex(index)
        if prop.lColor is None or prop.lColor is CONFLICT:
            index = 0
        else:
            index = self.lColorCB.findData(Qt.QColor(prop.lColor))
        if index == -1:  # if the color is not supported, add it to combobox
            index = self.lColorCB.count()
            self.lColorCB.addItem(
                self._colorIcon(Qt.QColor(prop.lColor)),
                "",
                Qt.QColor(prop.lColor),
            )
        self.lColorCB.setCurrentIndex(index)
        # set the Fill Checkbox. The prop.sFill value can be in 3 states: True,
        # False and None
        if prop.sFill is None or prop.sFill is CONFLICT:
            checkState = Qt.Qt.PartiallyChecked
        elif prop.sFill:
            checkState = Qt.Qt.Checked
        else:
            checkState = Qt.Qt.Unchecked
        self.sFillCB.setCheckState(checkState)
        # set the Area Fill Checkbox. The prop.cFill value can be in 3 states:
        # True, False and None
        if prop.cFill is CONFLICT:
            checkState = Qt.Qt.PartiallyChecked
            self.cAreaDSB.setValue(0.0)
        elif prop.cFill is None:
            checkState = Qt.Qt.Unchecked
            self.cAreaDSB.setValue(0.0)
        else:
            checkState = Qt.Qt.Checked
            self.cAreaDSB.setValue(prop.cFill)
        self.cFillCB.setCheckState(checkState)

    def _onControlChanged(self, *args):
        """
        Slot to be called whenever a control plot_item is changed. It emits a
        `controlChanged` signal and applies the change if in autoapply mode.
        It ignores any arguments passed
        """

        self.controlChanged.emit()
        if self.autoApply:
            self.onApply()

    def _onSelectedCurveChanged(self):
        """Updates the shown properties when the curve selection changes"""
        plist = [
            self.curvePropDict[name] for name in self.getSelectedCurveNames()
        ]
        if len(plist) == 0:
            plist = [CurveAppearanceProperties()]
            self.lineGB.setEnabled(False)
            self.symbolGB.setEnabled(False)
            self.otherGB.setEnabled(False)
        else:
            self.lineGB.setEnabled(True)
            self.symbolGB.setEnabled(True)
            self.otherGB.setEnabled(True)

        self._shownProp = CurveAppearanceProperties.merge(plist)
        self.showProperties(self._shownProp)

    def _onSymbolStyleChanged(self, text):
        """Slot called when the Symbol style is changed, to ensure that symbols
        are visible if you choose them

        :param text: (str) the new symbol style label
        """
        text = str(text)
        if self.sSizeSB.value() < 2 and text not in ["", "No symbol"]:
            self.sSizeSB.setValue(3)

    def getShownProperties(self):
        """Returns a copy of the currently shown properties and updates
        self._shownProp

        Note: the title property is left as CONFLICT since all are shown

        :return: (CurveAppearanceProperties)
        """
        prop = CurveAppearanceProperties()

        # get the values from the Style comboboxes. Note that the empty string
        # ("") translates into CONFLICT
        prop.sStyle = ReverseNamedSymbolStyles[
            str(self.sStyleCB.currentText())
        ]
        prop.lStyle = ReverseNamedLineStyles[str(self.lStyleCB.currentText())]
        prop.stepMode = ReverseNamedStepMode[
            str(self.stepModeCB.currentText())
        ]
        # get sSize and lWidth from the spinboxes (-1 means conflict)
        v = self.sSizeSB.value()
        if v == -1:
            prop.sSize = CONFLICT
        else:
            prop.sSize = v
        v = self.lWidthSB.value()
        if v == -1:
            prop.lWidth = CONFLICT
        else:
            prop.lWidth = v
        # Get the Color combo boxes. The item at index 0 is the empty one in
        # the comboboxes
        index = self.sColorCB.currentIndex()
        if index == 0:
            prop.sColor = CONFLICT
        else:
            prop.sColor = Qt.QColor(self.sColorCB.itemData(index))
        index = self.lColorCB.currentIndex()
        if index == 0:
            prop.lColor = CONFLICT
        else:
            prop.lColor = Qt.QColor(self.lColorCB.itemData(index))
        # get the sFill from the Checkbox.
        checkState = self.sFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.sFill = CONFLICT
        else:
            prop.sFill = bool(checkState)
        # get the cFill from the Checkbox.
        checkState = self.cFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.cFill = CONFLICT
        elif checkState == Qt.Qt.Checked:
            prop.cFill = self.cAreaDSB.value()
        else:
            prop.cFill = None

        # get the y2 state from the buttons
        y1 = self.assignToY1BT.isChecked()
        y2 = self.assignToY2BT.isChecked()
        if not y1 and not y2:
            prop.y2 = CONFLICT
        elif y1:
            prop.y2 = False
        elif y2:
            prop.y2 = True
        else:
            # both buttons should never be checked simultaneously
            raise RuntimeError("Inconsistent state of Y-axis buttons")

        # store the props
        self._shownProp = copy.deepcopy(prop)
        return copy.deepcopy(prop)

    def onApply(self):
        """Apply does 3 things:

            - It updates `self.curvePropDict` using the current values
              chosen in the dialog
            - It applies the properties to the curves (if the Chooser was
              initialized with the appropriate curvesDict)
            - It emits a curveAppearanceChanged signal that indicates the names
              of the curves that changed and the new properties.  (TODO)

        :return: (tuple<CurveAppearanceProperties,list>) a tuple containing the
                 curve properties and a list of the selected curve names (as a
                 list<str>)
        """
        names = self.getSelectedCurveNames()
        prop = self.getShownProperties()
        # Update self.curvePropDict for selected properties
        for n in names:
            self.curvePropDict[n] = CurveAppearanceProperties.merge(
                [self.curvePropDict[n], prop],
                conflict=CurveAppearanceProperties.inConflict_update_a,
            )
            # update the title with whatever is now written in the curvesLW
            self.curvePropDict[n].title = self.__findCurveListItem(n).text()
        # emit a (PyQt) signal telling what properties (first argument) need to
        # be applied to which curves (second argument)
        # self.curveAppearanceChanged.emit(prop, names)
        # return both values

        if self._curvesDict is not None:
            set_properties_on_curves(
                self.curvePropDict,
                self._curvesDict,
                plotItem=self.plotItem,
                y2Axis=self.Y2Axis,
            )
        return prop, names

    def onReset(self):
        """slot to be called when the reset action is triggered. It reverts to
        the original situation"""
        self.setCurvesProps(self._curvePropDictOrig)
        self.curvesLW.clearSelection()

    def _colorIcon(self, color, w=10, h=10):
        # to do: create a border
        pixmap = Qt.QPixmap(w, h)
        pixmap.fill(Qt.QColor(color))
        return Qt.QIcon(pixmap)


def get_properties_from_curves(curves):
    """Returns a dictionary of properties corresponding to the curves given
    in the `curves` dict.
    :param curves: dict whose values are :class:`PlotDataItem` instances
                   and whose keys arbitrarily identify a given curve
    :return: properties dict containing :class:`CurveAppearanceProperties`
             instances and whose keys match those in the `curves` dict
    """
    curves_prop = {}
    for key, item in curves.items():
        y2 = isinstance(item.getViewBox(), Y2ViewBox)

        opts = item.opts
        pen = pyqtgraph.mkPen(opts["pen"])
        # symbol_pen = pyqtgraph.mkPen(opts["symbolPen"])
        symbol_brush = pyqtgraph.mkBrush(opts["symbolBrush"])
        title = opts.get("name")
        sStyle = opts["symbol"]
        sSize = opts["symbolSize"]

        if sStyle is None:
            sColor = None
            sSize = -1
        else:
            sColor = symbol_brush.color()

        sFill = symbol_brush.color()
        if sFill is None or sStyle is None:
            sFill = False
        else:
            sFill = True

        lStyle = pen.style()
        lWidth = pen.width()
        lColor = pen.color()
        stepMode = opts.get("stepMode", None)

        cFill = opts["fillLevel"]

        curve_appearance_properties = CurveAppearanceProperties(
            sStyle=sStyle,
            sSize=sSize,
            sColor=sColor,
            sFill=sFill,
            lStyle=lStyle,
            lWidth=lWidth,
            lColor=lColor,
            stepMode=stepMode,
            cFill=cFill,
            y2=y2,
            title=title,
        )
        curves_prop[key] = curve_appearance_properties
    return curves_prop


def set_properties_on_curves(properties, curves, plotItem=None, y2Axis=None):
    """
    Sets properties provided in the `properties` dict to curves provided in
    the `curves` dict. The association of a given curve with a property is
    done by matching the keys in the respective dictionaries.
    If both `plotItem` and `y2Axis` are passed, the curve will be moved to the
    ViewBox defined in the .y2 property
    :param properties: dict whose values are :class:`CurveAppearanceProperties`
                       instances and whose keys arbitrarily identify a
                       given curve
    :param curves: dict whose values are :class:`PlotDataItem` instances
                   and whose keys match those of properties (if a key in
                   `curves` does not exist in `properties`, it will be ignored)
    :param plotItem: The :class:`PlotItem` containing the dataItem.
    :param y2Axis: The :class:`Y2ViewBox` instance
 e skipp   """

    for key, dataItem in curves.items():
        try:
            prop = properties[key]
        except KeyError:
            warning("Cannot restore curve '%s' (no known properties)", key)
            continue
        sStyle = prop.sStyle
        sSize = prop.sSize
        sColor = prop.sColor
        sFill = prop.sFill
        lStyle = prop.lStyle
        lWidth = prop.lWidth
        lColor = prop.lColor
        cFill = prop.cFill
        stepMode = prop.stepMode
        y2 = prop.y2
        title = prop.title

        dataItem.setPen(dict(style=lStyle, width=lWidth, color=lColor))
        if cFill is not None:
            dataItem.setFillLevel(cFill)
            try:
                cFillColor = Qt.QColor(lColor)
                cFillColor.setAlphaF(0.5)  # set to semitransparent
            except Exception:
                cFillColor = lColor
            dataItem.setFillBrush(cFillColor)
        else:
            dataItem.setFillLevel(None)

        dataItem.setSymbol(sStyle)
        # dataItem.setSymbolPen(pyqtgraph.mkPen(color=sColor))
        if sStyle is None or sSize < 0:
            dataItem.setSymbolSize(0)
        else:
            dataItem.setSymbolSize(sSize)

        if sFill:
            dataItem.setSymbolBrush(pyqtgraph.mkColor(sColor))
        else:
            dataItem.setSymbolBrush(None)

        dataItem.opts["stepMode"] = stepMode
        dataItem.updateItems()

        if title is not None:
            # set the title of the curve
            dataItem.setData(name=title)
            # update the corresponding label in the legend
            if plotItem is not None and plotItem.legend is not None:
                if hasattr(plotItem.legend, "getLabel"):
                    plotItem.legend.getLabel(dataItem).setText(title)
                else:
                    # workaround for pyqtgraph<=0.11 (getLabel not implemented)
                    for sample, label in plotItem.legend.items:
                        if sample.item == dataItem:
                            label.setText(title)
                            break

        # act on the ViewBoxes only if plotItem and y2Axis are given
        if plotItem and y2Axis:
            set_y_axis_for_curve(y2, dataItem, plotItem, y2Axis)


class CurveAppearanceProperties(object):
    """An object describing the appearance of a TaurusCurve"""

    propertyList = [
        "sStyle",
        "sSize",
        "sColor",
        "sFill",
        "lStyle",
        "lWidth",
        "lColor",
        "stepMode",
        "cFill",
        "y2",
        "title",
        "visible",
    ]

    def __init__(
        self,
        sStyle=CONFLICT,
        sSize=CONFLICT,
        sColor=CONFLICT,
        sFill=CONFLICT,
        lStyle=CONFLICT,
        lWidth=CONFLICT,
        lColor=CONFLICT,
        stepMode=CONFLICT,
        y2=CONFLICT,
        cFill=CONFLICT,
        title=CONFLICT,
        visible=CONFLICT,
    ):
        """
        Possible keyword arguments are:
            - sStyle= symbolstyle
            - sSize= int
            - sColor= color
            - sFill= bool
            - lStyle= linestyle
            - lWidth= int
            - lColor= color
            - stepMode= stepmode
            - cFill= float or None
            - y2= bool
            - visible = bool
            - title= str

        Where:
            - color is a color that QColor() understands (i.e. a
              Qt.Qt.GlobalColor, a color name, or a Qt.Qcolor)
            - symbolstyle is a key of NamedSymbolStyles
            - linestyle is a key of Qt.Qt.PenStyle
            - stepMode is a key of NamedStepMode
            - cFill can either be None (meaning not to fill) or a float that
              indicates the baseline from which to fill
            - y2 is True if the curve is associated to the y2 axis
        """
        self.sStyle = sStyle
        self.sSize = sSize
        self.sColor = sColor
        self.sFill = sFill
        self.lStyle = lStyle
        self.lWidth = lWidth
        self.lColor = lColor
        self.stepMode = stepMode
        self.cFill = cFill
        self.y2 = y2
        self.title = title
        self.visible = visible

    def __repr__(self):
        ret = "<CurveAppearanceProperties:"
        for p in self.propertyList:
            ret += " {}={}".format(p, getattr(self, p))
        ret += ">"
        return ret

    @staticmethod
    def inConflict_update_a(a, b):
        """
        This  function can be passed to CurvesAppearance.merge()
        if one wants to update prop1 with prop2 except for those
        attributes of prop2 that are set to CONFLICT
        """
        if b is CONFLICT:
            return a
        else:
            return b

    @staticmethod
    def inConflict_CONFLICT(a, b):
        """In case of conflict, returns CONFLICT"""
        return CONFLICT

    def conflictsWith(self, other, strict=True):
        """
        Compares itself with another CurveAppearanceProperties object
        and returns (a list of then names of) the attributes that are in
        conflict between the two
        """
        result = []
        for aname in self.propertyList:
            vself = getattr(self, aname)
            vother = getattr(other, aname)
            if vself != vother and (
                strict or not (CONFLICT in (vself, vother))
            ):
                result.append(aname)
        return result

    @classmethod
    def merge(cls, plist, attributes=None, conflict=None):
        """
        returns a CurveAppearanceProperties object formed by merging a list
        of other CurveAppearanceProperties objects

        :param plist: (sequence<CurveAppearanceProperties>) objects to be
        merged
        :param attributes: (sequence<str>) the name of the attributes to
                           consider for the merge. If None, all the attributes
                           will be merged
        :param conflict: (callable) a function that takes 2 objects (having a
                         different attribute) and returns a value that solves
                         the conflict. If None is given, any conflicting
                         attribute will be set to CONFLICT.

        :return: (CurveAppearanceProperties) merged properties
        """
        n = len(plist)
        if n < 1:
            raise ValueError("plist must contain at least 1 member")
        plist = copy.deepcopy(plist)
        if n == 1:
            return plist[0]
        if attributes is None:
            attributes = cls.propertyList
        if conflict is None:
            conflict = CurveAppearanceProperties.inConflict_CONFLICT
        p = CurveAppearanceProperties()
        for a in attributes:
            alist = [p.__getattribute__(a) for p in plist]
            p.__setattr__(a, alist[0])
            for ai in alist[1:]:
                if alist[0] != ai:
                    # print "MERGING:",a,alist[0],ai,conflict(alist[0],ai)
                    p.__setattr__(a, conflict(alist[0], ai))
                    break
        return p


def deserialize_opts(opts):
    """
    Deserialize opts dict to pass it to a PlotDataItem

    :param opts: (dict) serialized properties (as the output of
                 :meth:`deserialize_opts`)

    :return: (dict) deserialized properties (acceptable by PlotDataItem)
    """
    # pen property
    if opts["pen"] is not None:
        opts["pen"] = _unmarshallingQPainter(opts, "pen", "pen")

    # shadowPen property
    if opts["shadowPen"] is not None:
        opts["shadowPen"] = _unmarshallingQPainter(opts, "shadowPen", "pen")

    # symbolPen property
    if opts["symbolPen"] is not None:
        opts["symbolPen"] = _unmarshallingQPainter(opts, "symbolPen", "pen")

    # fillBrush property
    if opts["fillBrush"] is not None:
        opts["fillBrush"] = _unmarshallingQPainter(opts, "fillBrush", "brush")

    # symbolBrush property
    if opts["symbolBrush"] is not None:
        opts["symbolBrush"] = _unmarshallingQPainter(
            opts, "symbolBrush", "brush"
        )

    return opts


def serialize_opts(opts):
    """
    Serialize all properties from PlotDataItem.

    :param opts: (dict) PlotDataItem opts (may include non-serializable
                 objects)

    :return: (dict) serialized properties (can be pickled)
    """
    # pen property (QPen object)
    if opts["pen"] is not None:
        _marshallingQPainter(opts, "pen", "pen")

    # shadowPen property (QPen object)
    if opts["shadowPen"] is not None:
        _marshallingQPainter(opts, "shadowPen", "pen")

    # symbolPen property (QPen object)
    if opts["symbolPen"] is not None:
        _marshallingQPainter(opts, "symbolPen", "pen")

    # fillBrush property (QBrush object)
    if opts["fillBrush"] is not None:
        _marshallingQPainter(opts, "fillBrush", "brush")

    # symbolBrush property (QBrush object)
    if opts["symbolBrush"] is not None:
        _marshallingQPainter(opts, "symbolBrush", "brush")

    return opts


def _marshallingQPainter(opts, prop_name, qPainter):
    if qPainter == "pen":
        painter = pyqtgraph.mkPen(opts[prop_name])
        opts[prop_name + "_width"] = painter.width()
        opts[prop_name + "_dash"] = painter.dashPattern()
        opts[prop_name + "_cosmetic"] = painter.isCosmetic()
    elif qPainter == "brush":
        painter = pyqtgraph.mkBrush(opts[prop_name])
    else:
        return

    color = pyqtgraph.colorStr(painter.color())
    opts[prop_name] = color
    opts[prop_name + "_style"] = painter.style()


def _unmarshallingQPainter(opts, prop_name, qPainter):
    color = opts[prop_name]
    style = opts[prop_name + "_style"]
    del opts[prop_name + "_style"]

    if qPainter == "pen":
        width = opts[prop_name + "_width"]
        dash = opts[prop_name + "_dash"]
        cosmetic = opts[prop_name + "_cosmetic"]
        del opts[prop_name + "_width"]
        del opts[prop_name + "_dash"]
        del opts[prop_name + "_cosmetic"]
        painter = pyqtgraph.mkPen(
            color=color, style=style, width=width, dash=dash, cosmetic=cosmetic
        )
    elif qPainter == "brush":
        painter = pyqtgraph.mkBrush(color=color)
        painter.setStyle(style)
    else:
        return

    return painter
