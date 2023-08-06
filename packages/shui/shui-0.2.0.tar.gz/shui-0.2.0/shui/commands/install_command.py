"""Command-line application for installing a particular Spark/Hadoop version"""
from contextlib import suppress
import pathlib3x as pathlib
from cleo import Command
from shui.api import get_versions, install_version


class InstallCommand(Command):
    """
    Install a particular Spark and Hadoop version

    install
        {--latest : Use the latest available version}
        {--spark=any : Spark version}
        {--hadoop=any : Hadoop version}
        {--target=cwd : Directory to install into}
    """

    def handle(self):
        # Get correct Spark/Hadoop version
        if self.option("latest"):
            selected_version = sorted(get_versions())[-1]
        else:
            matching_versions = get_versions()
            if self.option("spark") != "any":
                matching_versions = [
                    v for v in matching_versions if v.spark == self.option("spark")
                ]
            if self.option("hadoop") != "any":
                matching_versions = [
                    v for v in matching_versions if v.hadoop == self.option("hadoop")
                ]
            if not len(matching_versions) == 1:
                self.line(
                    f"Found {len(matching_versions)} versions matching <comment>Spark</comment> <info>{self.option('spark')}</info>; <comment>Hadoop</comment> <info>{self.option('hadoop')}</info>"
                )
                for version in matching_versions:
                    self.line(f"  - Found {version}")
                raise ValueError("Could not identify version to install!")
            selected_version = matching_versions[0]
        # Get installation directory, creating it if necessary
        if self.option("target") != "cwd":
            install_dir = pathlib.Path(self.option("target"))
        else:
            install_dir = pathlib.Path.cwd()
        install_dir = install_dir.expanduser().resolve()
        with suppress(OSError):
            install_dir.mkdir(parents=True, exist_ok=True)
        if not install_dir.is_dir():
            raise ValueError(f"{install_dir} is not a valid installation directory!")
        install_version(self.line, selected_version, install_dir)
