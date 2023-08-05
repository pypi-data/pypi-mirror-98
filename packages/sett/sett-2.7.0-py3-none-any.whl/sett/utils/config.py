import os
import platform
import json
import tempfile
import dataclasses
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

from libbiomedit.lib.deserialize import deserialize

from .log import exception_to_message, get_default_log_dir, create_logger
from ..core.crypt import open_gpg_dir, get_default_gpg_config_dir
from ..core.error import UserError
from ..core.portal_api import PortalApi
from .. import APP_NAME_SHORT


CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_ENVIRON_VAR = "SETT_CONFIG_FILE"

conf_sub_dir_by_os: Dict[str, Tuple[str, ...]] = {
    "Linux": (".config",),
    "Darwin": (".config",),
    "Windows": ("AppData", "Roaming"),
}

logger = create_logger(__name__)


@dataclass(frozen=True)
class Connection:
    """dataclass holding config fo a connection (sftp / liquid files)"""

    protocol: str
    parameters: Dict[str, Any]


TMP_DIR = tempfile.gettempdir()


@dataclass
class Config:
    """dataclass holding config data"""

    dcc_portal_url: str = "https://portal.dcc.sib.swiss"
    keyserver_url: Optional[str] = "keyserver.dcc.sib.swiss"
    gpg_config_dir: str = get_default_gpg_config_dir()
    key_validation_authority_keyid: Optional[str] = "881685B5EE0FCBD3"
    sign_encrypted_data: bool = True
    always_trust_recipient_key: bool = True
    repo_url: str = "https://pypi.org"
    check_version: bool = True
    offline: bool = False
    log_dir: str = get_default_log_dir()
    log_max_file_number: int = 1000
    connections: Dict[str, Connection] = dataclasses.field(default_factory=lambda: {})
    temp_dir: str = TMP_DIR
    output_dir: Optional[str] = None
    ssh_password_encoding: str = "utf_8"
    default_sender: Optional[str] = None
    gui_quit_confirmation: bool = True
    compression_level: int = 5

    def __post_init__(self):
        for url in ("dcc_portal_url", "repo_url"):
            setattr(self, url, getattr(self, url).rstrip("/"))

    @property
    def portal_api(self):
        return PortalApi(self.dcc_portal_url)

    @property
    def gpg_store(self):
        return exception_to_message(UserError, logger)(open_gpg_dir)(
            self.gpg_config_dir
        )


class ConnectionStore:
    """Connection configuration storage manager"""

    config_field_name = "connections"

    def __init__(self, config_path: Optional[str] = None):
        self.path = get_config_file() if config_path is None else config_path

    def _read(self) -> Dict:
        """Load data from config file"""
        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _write(self, data: Dict):
        """Write data to config file"""
        save_config(data, self.path)

    def save(self, name: str, connection: Connection, exclude: str = "pass"):
        """Save a new connection in the config file

        :param name: name of the new connection.
        :param connection: new connection object.
        :param exclude: exclude all connection fields containing `exclude` substring.
        """
        data = self._read()
        connections = data.setdefault(self.config_field_name, {})
        c = dataclasses.asdict(connection)
        pass_fields = {k for k in c["parameters"] if exclude in k}
        for f in pass_fields:
            del c["parameters"][f]
        connections[name] = c
        self._write(data)

    def delete(self, name: str):
        """Delete a new connection from the config file"""
        data = self._read()
        try:
            data.get(self.config_field_name, {}).pop(name)
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{name}' does not exist.") from e

    def rename(self, old: str, new: str):
        """Rename an existing connection from the config file"""
        data = self._read()
        try:
            connection = data.get(self.config_field_name, {}).pop(old)
            data[self.config_field_name][new] = connection
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{new}' does not exist.") from e


def load_config() -> Config:
    """Loads the config, returning a Config object"""
    cfg_dct = {}
    try:
        cfg_dct = sys_config_dict()
        cfg_dct.update(load_config_dict(get_config_file()))
    except UserError as e:
        warnings.warn(format(e))
    return deserialize(Config)(cfg_dct)


def save_config(config: Dict, path: Optional[str] = None) -> str:
    """Save config to a file
    :return: path of the created config file.
    """
    config_file = Path(get_config_file() if path is None else path)
    if not config_file.parent.is_dir():
        config_file.parent.mkdir(parents=True)

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2, sort_keys=True)
    return config_file.as_posix()


def create_config() -> str:
    """Creates a new config file in the home directory's config folder
    :return: path of the created config file.
    """
    return save_config(config_to_dict(default_config()))


def config_to_dict(config: Config) -> dict:
    """Converts a Config object into a dict"""
    return dataclasses.asdict(config)


def default_config() -> Config:
    """Creates a new Config object with default values"""
    return deserialize(Config)(sys_config_dict())


def sys_config_dict() -> dict:
    """On linux only: try to load global sys config.
    If the env variable `SYSCONFIG` is set search there, else in
    `/etc/{APP_NAME_SHORT}`"""
    if platform.system() == "Linux":
        sys_cfg_dir = os.environ.get("SYSCONFIG", os.path.join("/etc", APP_NAME_SHORT))
        return load_config_dict(os.path.join(sys_cfg_dir, CONFIG_FILE_NAME))
    return {}


def load_config_dict(path: str) -> dict:
    """Load raw config as a dict"""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError as e:
        raise UserError(f"Failed to load configuration from '{path}'. {e}") from e


def get_config_file() -> str:
    """Retrieve the platform-specific path of the config file. If the user has
    the correct config file path environmental variable defined in their
    current environment, this file gets used instead.

    :return: path of the config.
    :raises UserError:
    """
    # Case 1: a config file path environmental variable is defined.
    if CONFIG_FILE_ENVIRON_VAR in os.environ:
        config_file = os.environ[CONFIG_FILE_ENVIRON_VAR]
        if os.path.isdir(config_file):
            raise UserError(
                f"Environmental variable {CONFIG_FILE_ENVIRON_VAR} "
                f"must point to a file, not a directory "
                f"[{config_file}]."
            )
        return config_file

    # Case 2: use the default platform-specific config file.
    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)


def get_config_dir() -> str:
    """Return platform specific default config direcory."""
    return os.path.join(
        os.path.expanduser("~"), *conf_sub_dir_by_os[platform.system()], APP_NAME_SHORT
    )
