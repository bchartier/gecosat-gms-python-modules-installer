import platform
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import gms_install_python_modules.toolbelt.log_handler as log_hdlr


class DontContinueException(Exception):
    pass


class NotOnWindowsException(Exception):
    pass


def _install_python_packages_for_qgis_app(qgis_app_path: str) -> str:
    """Install the Python packages:
    - create a temp dir in order to store temporary reachable from OSGeo4W
    - create the requirements.txt file
    - create the .bat file from a template
    - run the .bat file within the OSGeo4W shell

    Args:
        qgis_app (Software): QGIS app description (with name, version, path...)
    """

    output = ""

    # Set the new working directory (root directory of QGIS)
    os.chdir(qgis_app_path)

    try:
        # todo: possible improvement:
        # detect the py3_env.bat file
        # and use a specific template file if not present
        # 2 template files: 1 with py3_env and 1 without

        # Copy config files in temp dir in order to make them accessible from subprocesses

        # Compute path to temp dir and files
        temp_dir = tempfile.TemporaryDirectory()
        temp_install_bat_file_path = Path(temp_dir.name) / "pip-install.bat"
        temp_requirements_file_path = Path(temp_dir.name) / "requirements.txt"

        # Create temp requirements.txt file
        requirements_file_path = Path(__file__) / ".." / "config" / "requirements.txt"
        shutil.copy(requirements_file_path, temp_requirements_file_path)

        # Create temp bat file
        jinja_template_dir_path = Path(__file__) / ".." / "config" / "templates"
        jinja_template_dir_path = jinja_template_dir_path.resolve()
        env = Environment(
            loader=FileSystemLoader(jinja_template_dir_path),
            autoescape=select_autoescape(),
        )
        install_bat_template = env.get_template("pip-install.bat")
        temp_install_bat_content = install_bat_template.render(
            file_path=temp_requirements_file_path,
        )

        with open(temp_install_bat_file_path, "w") as temp_install_bat_file:
            temp_install_bat_file.write(temp_install_bat_content)

        # Install Python packages in the QGIS Python distribution
        # Needs to be done through the OSGeo4W terminal

        command = [r"OSGeo4W.bat", str(temp_install_bat_file_path)]
        subp = subprocess.run(command, capture_output=True, universal_newlines=True)
        output = subp.stdout

    finally:
        temp_dir.cleanup()

    return output


def install_python_packages_in_qgis(qgis_app_path) -> str:
    output = ""

    # Save the current working directory in order to be able to reset it at the end of
    # the function
    last_cwd = os.getcwd()

    try:
        if platform.system() != "Windows":
            raise NotOnWindowsException

        output = _install_python_packages_for_qgis_app(qgis_app_path)

    except DontContinueException:
        pass
    except NotOnWindowsException:
        log_hdlr.PlgLogger.log(
            message="Ce plugin ne peut fonctionner que sous Windows."
        )

    # Set back the current working directory
    if last_cwd:
        os.chdir(last_cwd)

    return output
