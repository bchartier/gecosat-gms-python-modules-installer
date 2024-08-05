#! python3  # noqa: E265

"""
    Plugin settings form integrated into QGIS 'Options' menu.
"""

# standard
from pathlib import Path

# PyQGIS
from qgis.gui import QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QIcon

# project
from gms_install_python_modules.__about__ import (
    DIR_PLUGIN_ROOT,
    __title__,
    __version__,
)
from gms_install_python_modules.toolbelt import PlgLogger, PlgOptionsManager
from gms_install_python_modules.toolbelt.preferences import PlgSettingsStructure

# ############################################################################
# ########## Globals ###############
# ##################################

FORM_CLASS, _ = uic.loadUiType(
    Path(__file__).parent / "{}.ui".format(Path(__file__).stem)
)


# ############################################################################
# ########## Classes ###############
# ##################################


class ConfigOptionsPage(FORM_CLASS, QgsOptionsPageWidget):
    """Settings form embedded into QGIS 'options' menu."""

    def __init__(self, parent):
        super().__init__(parent)
        self.log = PlgLogger().log
        self.plg_settings = PlgOptionsManager()
        self.setupUi(self)
        self.setObjectName("mOptionsPage{}".format(__title__))
        self.settings = None

        # header
        self.lbl_title.setText(f"{__title__} - Version {__version__}")

        # load previously saved settings
        self.load_settings()

    def apply(self):
        """Called to permanently apply the settings shown in the options page (e.g. \
        save them to QgsSettings objects). This is usually called when the options \
        dialog is accepted."""
        new_settings = PlgSettingsStructure(
            debug_mode=self.opt_debug.isChecked(),
            version=__version__,
        )

        # dump new settings into QgsSettings
        self.plg_settings.save_from_object(new_settings)

        if __debug__:
            self.log(
                message="DEBUG - Settings successfully saved.",
                log_level=4,
            )

    def load_settings(self):
        """Load options from QgsSettings into UI form."""
        self.settings = self.plg_settings.get_plg_settings()

        self.opt_debug.setChecked(self.settings.debug_mode)
        self.lbl_version_saved_value.setText(self.settings.version)


class PlgOptionsFactory(QgsOptionsWidgetFactory):
    """Factory for options widget."""

    def __init__(self):
        super().__init__()

    def icon(self) -> QIcon:
        return QIcon(str(DIR_PLUGIN_ROOT / "resources/images/add.png"))

    def createWidget(self, parent) -> ConfigOptionsPage:
        return ConfigOptionsPage(parent)

    def title(self) -> str:
        return __title__
