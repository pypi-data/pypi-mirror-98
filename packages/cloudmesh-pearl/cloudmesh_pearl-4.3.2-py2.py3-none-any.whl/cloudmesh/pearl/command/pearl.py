from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.pearl.Pearl import Pearl
from cloudmesh.common.util import yn_choice
from cloudmesh.common.Shell import Shell
import os

PYTHON="python3"

class PearlCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_pearl(self, args, arguments):
        """
        ::

          Usage:
                pearl user USER
                pearl key KEY
                pearl queue
                pearl ssh [COMMAND...]
                pearl batch SCRIPT
                pearl run [--cpu=CPU] [--gpu=GPU] [--output=OUTPUT]
                pearl sync put [DIR]
                pearl sync get [DIR]
                pearl fuse DIR
                pearl venv [VENV] [--python=PYTHON] [-y|-n]
                pearl install
                pearl notebook NAME [--cpu=CPU] [--gpu=GPU] [--duration=DURATION] [--force]
                pearl doc
                pearl module
                pearl info
                pearl verbose [ON]

          Interfacing with pearl

          Arguments:
              USER     the username
              SCRIPT   script to be executed
              DIR      the DIRECTORY to be synced to pearl
              OPTIONS  options
              VENV     The virtual python env

        """

        pearl = Pearl()

        arguments.yes = arguments["-y"]
        arguments.no  = arguments["-n"]
        arguments.python = arguments["--python"] or "python"
        arguments.gpu = arguments["--gpu"]
        arguments.cpu = arguments["--cpu"]
        arguments.VENV = arguments.VENV or "PEARL"
        arguments.FORCE = arguments["--force"]
        arguments.DIR = arguments.DIR or "."

        VERBOSE(arguments)
        if arguments.doc:

            Shell.browser('https://pearl-cluster.readthedocs.io/en/latest/')

        elif arguments.user:

            pearl.set_user(arguments.USER)
            return

        try:
            pearl.check_user()
        except ValueError:
            Console.error("Please set the user with\n")
            Console.msg("   cms pearl user YOURUSERID\n")

        if arguments.info:
            pearl.info()

        elif arguments.verbose:
            pearl.set_verbose(arguments.ON)

        elif arguments.key:
            pearl.set_key(arguments.KEY)

        elif arguments.venv:

            if not arguments.VENV.startswith("~"):
                arguments.VENV = f"~/{arguments.VENV}"
            arguments.VENV = path_expand(arguments.VENV)


            question = f"Do you like to delete and create the venv {arguments.VENV}"

            if arguments.yes:
                create = True
            elif arguments.no:
                create = False
            elif yn_choice(question):
                create = True
            else:
                create = False

            if create:
                Console.ok(f"Creating venv {arguments.VENV}")
                os.system(f"rm -rf {arguments.VENV}")
                os.system(f"python -m venv {arguments.VENV}")
            else:
                Console.error(f"Skipping the creation of the venv {arguments.VENV}")

        elif arguments.install:

            pearl.ssh(execute=f"python3 -m venv {arguments.VENV}")

            # pearl.ssh(execute="pip install cloudmesh-pearl")
            # pearl.ssh(execute="pip install cloudmesh-pearl")
            # pearl.ssh(execute="pearl")

        elif arguments.module:

            pearl.module()

        elif arguments.info:

            pearl.info()

        elif arguments.queue:

            pearl.queue()

        elif arguments.notebook:
            # pearl notebook NAME [--cpu=CPU] [--gpu=GPU] [--output=OUTPUT]
            pearl.notebook(name=arguments.NAME,
                           cpu=arguments.CPU,
                           gpu=arguments.GPU,
                           duration=arguments.DURATION,
                           force=arguments.FORCE)

        elif arguments.ssh:

            if len (arguments.COMMAND) > 0:
                arguments.COMMAND = ' '.join(arguments.COMMAND)
            else:
                arguments.COMMAND = None
            pearl.ssh(execute=arguments.COMMAND)

        elif arguments.run:

            pearl.run(cpu=arguments.cpu, gpu=arguments.gpu)

        elif arguments.sync and arguments.put:

            pearl.sync_put(arguments.DIR)

        elif arguments.sync and arguments.get:

            pearl.sync_get(arguments.DIR)

        elif arguments.batch:

            pearl.batch(arguments.SCRIPT)

        else:
            Console.error("check your usage")

        """
        USER
            pearl batch SCRIPT
            pearl run [OPTIONS]
            pearl fuse DIR
            pearl
        """

        return ""
