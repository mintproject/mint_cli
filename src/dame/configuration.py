import configparser
import os
import pathlib

__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"

import click

DEFAULT_PROFILE = "default"


def get_credentials(profile):
    credentials_file = pathlib.Path(
        os.getenv("MINT_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    credentials = configparser.ConfigParser()
    if credentials_file.exists():
        credentials.read(credentials_file)
        if profile in credentials:
            return credentials[profile]
    elif credentials is None:
        return None
    elif credentials is not None and profile not in credentials and profile != ("%s" % DEFAULT_PROFILE):
        click.secho("WARNING: The profile doesn't exists. To configure it, run:\ndame configure -p {}".format(profile),
                    fg="yellow")
    return None


def configure_credentials(server, username, profile):
    credentials_file = pathlib.Path(
        os.getenv("MINT_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    credentials = configparser.ConfigParser()
    credentials.optionxform = str

    if credentials_file.exists():
        credentials.read(credentials_file)

    credentials[profile] = {
        "server": server,
        "username": username,
    }

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        credentials.write(fh)
