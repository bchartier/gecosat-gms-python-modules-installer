#! python3  # noqa: E265

"""
    Plugin main module.
"""

from pathlib import Path

# PyQGIS
from qgis.core import QgsApplication
from qgis.gui import QgisInterface

# from qgis.PyQt.QtCore import QCoreApplication
# from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar

# from qgis.utils import showPluginHelp

# project
from gms_install_python_modules.__about__ import __title__
from gms_install_python_modules.gui.dlg_settings import PlgOptionsFactory

from gms_install_python_modules.toolbelt import PlgLogger

from gms_install_python_modules.gui.dlg_installer import InstallDialog


class GmsInstallModules:
    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.log = PlgLogger().log
        self.__plugin_menu_label = "&Outils de contrôle GMS"

        # dialogs
        self.installer_dlg = None
        self.installer_dlg = None

        # actions
        self.action_help = None
        self.action_settings = None
        self.action_main_dialog = None

    def initGui(self) -> None:
        """Set up plugin UI elements."""

        # settings page within the QGIS preferences menu
        self.options_factory = PlgOptionsFactory()
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        # -- Actions
        self.action_main_dialog = QAction(
            self.options_factory.icon(),
            "Installeur de modules Python...",
            self.iface.mainWindow(),
        )
        self.action_main_dialog.triggered.connect(self.show_installer_triggered)

        # self.action_settings = QAction(
        #     QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
        #     "Paramètres...",
        #     self.iface.mainWindow(),
        # )
        # self.action_settings.triggered.connect(
        #     lambda: self.iface.showOptionsDialog(
        #         currentPage="mOptionsPage{}".format(__title__)
        #     )
        # )

        # -- Menu
        if self.action_main_dialog:
            self.iface.addPluginToMenu(
                self.__plugin_menu_label, self.action_main_dialog
            )

        # -- Toolbar
        if self.action_main_dialog:
            self.toolbar = QToolBar("Installeur de modules Python")
            self.iface.addToolBar(self.toolbar)
            self.toolbar.addAction(self.action_main_dialog)

    def show_installer_triggered(self) -> None:
        self.show_installer()

    def show_installer(self) -> None:
        """Create and show installer_dlg"""
        qgis_app_path = Path(QgsApplication.applicationDirPath()).parent.resolve()

        if self.installer_dlg is None:
            self.installer_dlg = InstallDialog(qgis_app_path, self.iface.mainWindow())
            self.installer_dlg.finished.connect(self._del_installer_dlg)

        self.installer_dlg.show()

    def _del_installer_dlg(self) -> None:
        """Delete installer_dlg"""
        if self.installer_dlg is not None:
            self.installer_dlg.deleteLater()
            self.installer_dlg = None

    def unload(self) -> None:
        """Cleans up when plugin is disabled/uninstalled."""
        # Clean up menu
        if self.action_main_dialog:
            self.iface.removePluginMenu(
                self.__plugin_menu_label, self.action_main_dialog
            )
        if self.action_main_dialog:
            self.iface.removePluginMenu(
                self.__plugin_menu_label, self.action_main_dialog
            )
        if self.action_help:
            self.iface.removePluginMenu(self.__plugin_menu_label, self.action_help)
        if self.action_settings:
            self.iface.removePluginMenu(self.__plugin_menu_label, self.action_settings)

        # Clean up preferences panel in QGIS settings
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

        # Remove toolbar
        if self.toolbar:
            self.toolbar.deleteLater()

        # Remove actions
        if self.action_settings:
            del self.action_settings
        if self.action_main_dialog:
            del self.action_main_dialog
        if self.action_help:
            del self.action_help
