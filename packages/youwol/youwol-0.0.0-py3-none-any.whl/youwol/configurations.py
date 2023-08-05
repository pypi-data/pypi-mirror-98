import asyncio
import zipfile

from cowpy import cow
from dataclasses import dataclass

from youwol.main_args import get_main_arguments, MainArguments


@dataclass(frozen=False)
class Configuration:

    open_api_prefix: str
    http_port: int
    base_path: str


async def welcome():
    print("""Seems you are a newcomer, Welcome :) 
Just a few post install actions to take care of and you are good to go.""")


async def post_install_initialization(main_args: MainArguments):

    path_db = main_args.system_path / 'databases'

    if not path_db.exists():
        await welcome()

    if not path_db.exists():
        print("post install action: unzipping default databases...")
        with zipfile.ZipFile(path_db.parent/'databases.zip', 'r') as zip_ref:
            zip_ref.extractall(path_db.parent)
        print("done")


async def get_full_local_config() -> Configuration:

    main_args = get_main_arguments()
    await post_install_initialization(main_args)

    return Configuration(
        open_api_prefix='',
        http_port=main_args.port,
        base_path=""
        )


configuration: Configuration = asyncio.get_event_loop().run_until_complete(get_full_local_config())


def print_invite(main_args: MainArguments):

    msg = cow.milk_random_cow(f"""
Running with configuration file: {main_args.config_path}

To start youwol please follow this link: 
http://localhost:{main_args.port}/ui/assets-browser-ui/

To create and manage assets on your computer please follow this link: 
http://localhost:{main_args.port}/ui/local-dashboard/
""")
    print(msg)

