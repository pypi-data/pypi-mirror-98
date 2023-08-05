import argparse
from pathlib import Path
from typing import NamedTuple
import youwol

parser = argparse.ArgumentParser()

parser.add_argument('--port', help='Specify the port')
parser.add_argument('--env', help='Option to pass a user defined environment id (e.g. dev, prod, etc)')
parser.add_argument('--conf', help='Path to a configuration file. Default to "system_path/default_config_yw.py".')

args = parser.parse_args()


class MainArguments(NamedTuple):
    port: int
    env: str
    config_path: Path
    youwol_path: Path = Path(youwol.__file__).parent
    system_path = youwol_path.parent / "youwol_data"


def get_main_arguments() -> MainArguments:
    return MainArguments(
        port=int(args.port) if args.port else 2000,
        env=args.env,
        config_path=Path(args.conf) if args.conf else MainArguments.system_path / "default_config_yw.py"
        )
