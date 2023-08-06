"""
Systemd utilities to create services for Podman Custodian Transmission module.

The systemd user unit service performs two actions.

- Upon boot (user default.target) the pod starts and updates itself if a new version is present.
- Upon shutdown (execstop) the pod stops (to be started on next boot)

The update process is tied to the system boot for simplicity. This is to piggyback
on expected system reboots after host (rpm-ostree) updates.
"""

from pathlib import Path, PosixPath
from subprocess import run
import importlib.resources as pkg_resources


def create_user_unit_path(create_folder: bool = False):
    """

    We want to add a systemd user unit to run transmission-pod on certain times. In order to do
    this we want to crete a unit at a proper location. According to:
    https://wiki.archlinux.org/index.php/Systemd/User
    our options are:

    * /usr/lib/systemd/user/:

      where units provided by installed packages belong.
    * ~/.local/share/systemd/user/

      where units of packages that have been installed in the home directory belong.
    * /etc/systemd/user/

      where system-wide user units are placed by the system administrator.
    * ~/.config/systemd/user/

      where the user puts their own units.

    We opt to use the latter choice.

    This function constructs the proper systemd user unit path where it will be installed.
    It also creates the necessary folder if it doesn't exist.

    :param create_folder: If true create the folder that the unit service will be installed.
    :returns: Path object for the location the unit service will be installed.

    """

    home = Path.home()
    unit_folder_path = home.joinpath(".config", "systemd", "user")
    if create_folder and not unit_folder_path.exists():
        unit_folder_path.mkdir(parents=True)

    unit_path = unit_folder_path.joinpath("transmission-pod.service")
    return unit_path


def create_service_unit(unit_path: PosixPath):
    """
    Create a systemd user unit for podman cutodian's transmission module.
    Use predefined template and modify where needed.

    We want the service to run when the user logs out so that all the changes
    they made are fixed if needed. We consult the following sources
    to create the appropriate systemd service template:

    * https://wiki.archlinux.org/index.php/Systemd/User
    * https://superuser.com/questions/1037466/
      how-to-start-a-systemd-service-after-user-login-and-stop-it-before-user-logout/1269158
    * https://askubuntu.com/questions/293312/
      execute-a-script-upon-logout-reboot-shutdown-in-ubuntu/796157#796157

    :param unit_path: Path where the common folder is located.
    """

    if not isinstance(unit_path, PosixPath):
        raise TypeError(f"Expected PosixPath object instead of {type(unit_path)}")

    # read package file
    # https://stackoverflow.com/a/20885799/1904901
    # To access a file inside the current module, set the package argument to __package__,
    template = pkg_resources.read_text(__package__, "transmission-pod.service")

    unit_path.write_text(template)
    print("Systemd user service unit installed!")


def activate_service():
    """
    After a transmission-pod setup is run we need to activate the service we installed.
    """

    run(["systemctl", "--user", "enable", "transmission-pod"], check=True)
    run(["systemctl", "--user", "start", "transmission-pod"], check=True)


def deactivate_service():
    """
    Deactivate a running transmission-pod service.
    """

    run(["systemctl", "--user", "stop", "transmission-pod"], check=True)
    run(["systemctl", "--user", "disable", "transmission-pod"], check=True)


def delete_service_unit():
    """
    Delete the systemd user unit for podman cutodian's transmission module.
    """

    # get expected unit's location:
    unit_path: PosixPath = create_user_unit_path(create_folder=False)
    unit_path.unlink()
    print("systemd user unit for podman cutodian's transmission module deleted")
