"""
Custodian Class for Transmission container.

This module is responsible for setting up and maintaining the container.

The container is intended to live inside the users home directory, in a hardcoded
location. Namely ``$HOME/transmission/``. The container is deployed within a pod
named transmission.
"""

# from typing import List
from shutil import rmtree
import subprocess
import getpass
from pathlib import Path
import importlib.resources as pkg_resources
from podcust.tools import get_user_input


class TransmissionCust:
    """
    Main class for handling the transmission container.

    :param name: The full repository name of the image this class is custodian for.
    """

    name: str
    image_id: str
    username: str

    def __init__(self, name: str = "ghcr.io/linuxserver/transmission"):
        """
        Initialize TransmissionCust class.
        """
        self.name = name
        self.image_id = ""
        self.username = getpass.getuser()
        # Main path we 'll use for the container
        self.main_path: Path = Path.home().joinpath("transmission")

    def pull_latest_transmission_image(self):
        """
        Pull latest transmission container image from linuxserver.io

        The relevant shell command is::

        $ podman pull ghcr.io/linuxserver/transmission

        """

        command_text = "podman pull $name"
        command_text = command_text.replace("$name", self.name)

        try:
            p = subprocess.run(
                command_text,
                text=True,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            print(p.stdout)

        except Exception as e:
            print(e)

    def clear_location(self):
        """
        Delete all files within the (hard-coded) path used by the transmission image under the
        podman custodian.
        """

        try:
            if self.main_path.exists():
                rmtree(self.main_path)
        except PermissionError as err:
            print(
                f"Please manually delete folder {str(self.main_path)} with required permissions."
            )
            raise err

    def deploy(self):
        """
        Create a pod named transmission to deploy our container.
        The steps taken during deployment are the following:

        - Delete path we 'll use to ensure a clean start.
        - Create the necessary folders, and give them proper permissions.
        - Write the proper kube yaml file that we 'll use to deploy the container.
        - Open the necessary firewall port.
        - Execute the podman play command to start the pod with the transmission container.
        """

        # Let's delete everything allready present on the space we want to use:
        self.clear_location()

        # let's recreate the directory now
        print("Creating key directories:")
        self.main_path.mkdir()
        # let's create additional needed directories
        config_dir = self.main_path.joinpath("config")
        config_dir.mkdir()
        watch_dir = self.main_path.joinpath("watch")
        watch_dir.mkdir()
        downloads_dir = self.main_path.joinpath("downloads")
        downloads_dir.mkdir()

        # We also need to change the SELinux security context of the new directories:
        print("Setting proper directory permissions:")
        command_text = "chcon -u system_u " + str(config_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -u system_u " + str(watch_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -u system_u " + str(downloads_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -r object_r " + str(config_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -r object_r " + str(watch_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -r object_r " + str(downloads_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -t container_file_t " + str(config_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -t container_file_t " + str(watch_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "chcon -t container_file_t " + str(downloads_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "podman unshare chown -R 1000:1000 " + str(config_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "podman unshare chown -R 1000:1000 " + str(watch_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )
        command_text = "podman unshare chown -R 1000:1000 " + str(downloads_dir)
        subprocess.run(
            command_text,
            text=True,
            shell=True,
            check=True,
        )

        # read package file
        # https://stackoverflow.com/a/20885799/1904901
        # To access a file inside the current module, set the package argument to __package__,
        yaml_template = pkg_resources.read_text(
            __package__, "transmission-kube-template.yml"
        )

        # populate template with proper entries:
        usnmae = get_user_input("Enter transmission username:")
        yaml_template = yaml_template.replace("$SET_USER", usnmae)
        password = get_user_input("Enter transmission password:")
        yaml_template = yaml_template.replace("$SET_PASSWD", password)
        yaml_template = yaml_template.replace("$LOCAL_USER", self.username)

        # write kubernetes template
        kube_yaml_path = self.main_path.joinpath("transmission-kube.yml")
        kube_yaml_path.write_text(yaml_template)

        subprocess.run(
            "podman play kube " + str(kube_yaml_path),
            text=True,
            shell=True,
            check=True,
        )

        # open necessary firewall port
        # sudo firewall-cmd --permanent --add-port=9091/tcp
        # There is a bug in Fedora IoT that requires this command to be run under sudo
        # Fedora docs for handling firewalld commands:
        # https://docs.fedoraproject.org/en-US/quick-docs/firewalld/
        subprocess.run(
            "sudo firewall-cmd --permanent --add-port=9091/tcp",
            text=True,
            shell=True,
            check=True,
        )
        # I don't like sudo been required but until there's a fix :(

    def stop(self):
        """
        Stop transmission pod
        """
        subprocess.run(
            "podman pod stop transmission",
            text=True,
            shell=True,
            check=True,
        )

    def rm(self):
        """
        Delete transmission pod.
        """
        subprocess.run(
            "podman pod rm transmission",
            text=True,
            shell=True,
            check=True,
        )

    def start(self):
        """
        Start transmission pod.
        """
        subprocess.run(
            "podman pod start transmission",
            text=True,
            shell=True,
            check=True,
        )

    def check_if_new_version_is_available(self) -> bool:
        """
        Check if there is a new version of the transmission docker image from linuxserver io.
        """

        deployed_image_check = subprocess.run(
            """podman inspect -f '{{ index .Config.Labels "build_version" }}' transmission-main""",
            text=True,
            shell=True,
            check=True,
            capture_output=True,
        )
        print(f"deployed image version is:\n{deployed_image_check.stdout}")

        self.pull_latest_transmission_image()
        remote_image_check = subprocess.run(
            """podman inspect -f '{{ index .Config.Labels "build_version" }}' ghcr.io/linuxserver/transmission""",  # noqa: E501
            text=True,
            shell=True,
            check=True,
            capture_output=True,
        )
        print(f"remote image version is:\n{remote_image_check.stdout}")

        return not deployed_image_check.stdout == remote_image_check.stdout

    def update_running_image(self):
        """
        Checks if a new image is available and if so, rebuilds the container.
        """

        to_update = self.check_if_new_version_is_available()

        if to_update:
            self.stop()
            self.rm()

            kube_yaml_path = self.main_path.joinpath("transmission-kube.yml")

            subprocess.run(
                "podman play kube " + str(kube_yaml_path),
                text=True,
                shell=True,
                check=True,
            )
            print("Deployed new image!")

        else:
            print("Current image is latest available")
