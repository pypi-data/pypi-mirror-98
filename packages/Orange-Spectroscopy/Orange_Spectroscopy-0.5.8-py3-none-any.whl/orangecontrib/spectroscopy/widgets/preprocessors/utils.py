from AnyQt.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QDoubleSpinBox, QLayout

from Orange.widgets.data.utils.preprocess import BaseEditor
from Orange.widgets.gui import OWComponent
from Orange.widgets.utils.messages import WidgetMessagesMixin
from Orange.widgets.widget import Msg
from orangecontrib.spectroscopy.data import getx


class BaseEditor(BaseEditor):

    def set_preview_data(self, data):
        """Handle the preview data (initialize parameters).

        Here, editors can check if preview data corresponds to the settings
        and warn users.
        """
        pass

    def set_reference_data(self, data):
        """Set the reference data"""
        pass


class BaseEditorOrange(BaseEditor, OWComponent, WidgetMessagesMixin):
    """
    Base widget for editing preprocessor's parameters that works with Orange settings.
    """
    # the following signals need to defined for WidgetMessagesMixin
    messageActivated = Signal(Msg)
    messageDeactivated = Signal(Msg)

    class Error(WidgetMessagesMixin.Error):
        exception = Msg("{}")

    def __init__(self, parent=None, **kwargs):
        BaseEditor.__init__(self, parent, **kwargs)
        OWComponent.__init__(self, parent)
        WidgetMessagesMixin.__init__(self)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.controlArea = QWidget(self)
        self.controlArea.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.controlArea)

        self.insert_message_bar()  # from WidgetMessagesMixin

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

    def parameters(self):
        return {k: getattr(self, k) for k in self.controlled_attributes}


class SetXDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def focusInEvent(self, *e):
        self.focusIn()
        return super().focusInEvent(*e)


class PreviewMinMaxMixin:
    """ Classes extending the mixin need to set preview_data
    """

    MINLIM_DEFAULT = 0.
    MAXLIM_DEFAULT = 1.

    def preview_min_max(self):
        if self.preview_data is not None:
            x = getx(self.preview_data)
            if len(x):
                return min(x), max(x)
        return self.MINLIM_DEFAULT, self.MAXLIM_DEFAULT


def layout_widgets(layout):
    if not isinstance(layout, QLayout):
        layout = layout.layout()
    for i in range(layout.count()):
        yield layout.itemAt(i).widget()


REFERENCE_DATA_PARAM = "_reference_data"