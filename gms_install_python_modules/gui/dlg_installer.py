#! python3

"""
    Install dialog.
"""

# Standard
from pathlib import Path

# PyQGIS
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

# Project
from gms_install_python_modules.toolbelt import PlgLogger, PlgOptionsManager
from gms_install_python_modules.install_modules import install_python_packages_in_qgis
from gms_install_python_modules.__about__ import (
    __title__,
    __version__,
)


class InstallDialog(QDialog):
    def __init__(self, qgis_app_path: Path, parent=None):
        """Dialog for Python modules installation.

        :param parent: parent widget, defaults to None
        :type parent: QObject, optional
        """
        # init module and ui
        super().__init__(parent)
        uic.loadUi(Path(__file__).parent / "{}.ui".format(Path(__file__).stem), self)

        # toolbelt
        self.log = PlgLogger().log
        self.plg_settings_mngr = PlgOptionsManager()
        self.plg_settings = self.plg_settings_mngr.get_plg_settings()

        self.qgis_app_path = qgis_app_path

        self._update_button_status()
        self.lbl_bottom.setText("")
        self.setWindowTitle(f"{__title__} - {__version__}")

    def user_text_changed(self, text):
        self._update_button_status()

    def pwd_text_changed(self, text):
        self._update_button_status()

    def _update_button_status(self) -> None:
        self.button_box.button(QDialogButtonBox.Yes).setEnabled(True)

    def accept(self) -> None:
        self.lbl_bottom.setText("")

        self.log(
            message="Début de l'installation des modules...",
            log_level=0,
            push=False,
        )

        self.lbl_bottom.setText("L'installation des modules est en cours...")

        output = install_python_packages_in_qgis(self.qgis_app_path)

        self.lbl_bottom.setText("L'installation des modules est terminée.")

        self.log(
            message=output,
            log_level=0,
            push=False,
        )

        self.log(
            message="Fin de l'installation des modules...",
            log_level=0,
            push=False,
        )

        super().accept()
