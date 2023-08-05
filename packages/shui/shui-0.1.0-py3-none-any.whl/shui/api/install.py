"""Functions for downloading a particular version from the remote repository"""
import tarfile
import requests


def install_version(logger, version, install_dir):
    """Download and install a particular Spark/Hadoop version"""
    # Download tarball
    logger(f"Installing {version} to <info>{install_dir}</info>")
    logger(f"Downloading from <info>{version.url}</info>...")
    tarball_path = install_dir / version.filename
    response = requests.get(version.url, stream=True)
    if response.status_code == 200:
        with open(tarball_path, "wb") as f_tarball:
            f_tarball.write(response.raw.read())
    # Extract tarball
    if not tarball_path.is_file():
        raise ValueError(f"Could not download {version} to <info>{install_dir}</info>!")
    with tarfile.open(tarball_path, "r:gz") as f_tarball:
        f_tarball.extractall(install_dir)
    # Remove tarball
    tarball_path.unlink()
