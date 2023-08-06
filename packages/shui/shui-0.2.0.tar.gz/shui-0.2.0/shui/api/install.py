"""Functions for downloading a particular version from the remote repository"""
import hashlib
import tarfile
from tqdm import tqdm
import requests


def install_version(logger, version, install_dir):
    """Download and install a particular Spark/Hadoop version"""
    # Construct local paths
    logger(f"Installing {version} to <info>{install_dir}</info>")
    tarball_path = install_dir / version.filename
    sha512_path = tarball_path.append_suffix(".sha512")
    # Download tarball and SHA512 sum
    download(logger, version.url, tarball_path)
    download(logger, f"{version.url}.sha512", sha512_path)
    # Verify tarball
    if verify_tarball(tarball_path, sha512_path):
        logger(f"Verified SHA512 hash for <info>{version.filename}</info>")
    else:
        raise IOError(f"Could not verify {version} using SHA512!")
    # Extract tarball
    if not tarball_path.is_file():
        raise ValueError(f"Could not download {version} to <info>{install_dir}</info>!")
    with tarfile.open(tarball_path, "r:gz") as f_tarball:
        f_tarball.extractall(install_dir)
    # Remove tarball
    tarball_path.unlink()


def download(logger, remote_url, local_path):
    """Download from a remote URL to a local path"""
    logger(f"Downloading from <info>{remote_url}</info>...")
    response = requests.get(remote_url, stream=True, allow_redirects=True)
    total_size = int(response.headers.get("content-length"))
    with open(local_path, "wb") as output_file:
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output_file.write(chunk)
                    progress_bar.update(len(chunk))


def verify_tarball(file_path, sha512_path):
    """Verify that a file matches its SHA512 hash"""
    # Get the file hash
    file_hash = hashlib.sha512()
    buffer_size = 524288  # read in chunks of 512kb
    with open(file_path, "rb") as input_file:
        while input_bytes := input_file.read(buffer_size):
            file_hash.update(input_bytes)
    calculated_hash = file_hash.hexdigest().lower()
    # Read the reference hash
    with open(sha512_path, "r") as input_hash:
        reference_hash = (
            "".join(input_hash.readlines())
            .replace("\n", " ")
            .replace(" ", "")
            .split(":")[1]
            .strip()
            .lower()
        )
    return calculated_hash == reference_hash
