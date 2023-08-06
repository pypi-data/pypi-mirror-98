from cloudmesh.common.variables import Variables
import os
from cloudmesh.common.util import path_expand
from cloudmesh.common.console import Console
import textwrap
from cloudmesh.common.util import writefile

class Pearl(object):

    def __init__(self):

        self.variables = Variables()
        self.host = "ui.pearl.scd.stfc.ac.uk"
        try:
            self.username = self.variables["pearl.username"]
        except:
            Console.error("Username not set")
        try:
            self.key = self.variables["pearl.key"]
        except:
            Console.error("Key not set")
        try:
            self.verbose = self.variables["pearl.verbose"]
        except:
            self.variables["pearl.verbose"] = self.verbose = False


    def check_user(self):
        if self.username is None:
            raise ValueError("Your user name for perl is not set")

    def _execute(self, command):
        command = f"ssh -i {self.key} {self.username}@{self.host} '{command}'"
        if self.verbose:
            print (command)
        os.system(command)

    def module(self):
        self.ssh(execute="source /etc/profile; module avail")

    def set_verbose(self, on=None):
        if on is None or on:
            self.variables["pearl.verbose"] = True
        else:
            self.variables["pearl.verbose"] = on.lower() in ["1", "true", "on"]
        if self.variables["pearl.verbose"]:
            os.system("cms debug on")
        else:
            os.system("cms debug off")

    def set_user(self, username):
        if "@" in username:
            username = username.split("@")[0]
        self.username = self.variables["pearl.username"] = username

    def set_key(self, key):
        self.key = path_expand(key)
        self.variables["pearl.key"] = self.key

    def queue(self):
        self._execute("squeue")

    def ssh(self, execute=None, shell=True):
        if execute is not None:
            if not shell:
                execute = f'"{execute}"'
                command = f"ssh -i {self.key} {self.username}@{self.host} {execute}"
            else:
                command = f'echo "{execute}" |'\
                    f' ssh -i /home/green/.ssh/id_rsa.pub {self.username}@{self.host} /bin/bash -l'
        else:
            command = f"ssh -i {self.key} {self.username}@{self.host}"
        if self.verbose:
            print (command)
        os.system(command)

    def batch(self, script):
        self.sync_put(".")
        self.ssh(f"sbatch notebooks/{script}")
        self.sync_get(".")

    def generate_notebook_batch(self, notebook=None, name="script", cpu=1, gpu=1, duration="00:00:01"):
        stem = notebook.replace(".ipynb", "")
        duration = duration or "00:00:01"

        batch_script = textwrap.dedent(f"""
        #!/bin/bash                                                                                                              

        #SBATCH -p pearl # partition (queue)                                                                                     
        #SBATCH --job-name={name}
        #SBATCH -n {cpu} # number of CPU cores
        #SBATCH --gres=gpu:{gpu}
        #SBATCH -t {duration} # time (D-HH:MM)
        #SBATCH --chdir=notebooks
        
        echo "#"
        echo "# PYTHON"
        echo "#"
        source ~/ENV3/bin/activate
        which python
        python --version
        echo "#"
        echo "# NVIDIA"
        echo "#"
        nvidia-smi
        echo "#"        
        # 
        # COMMANDS
        #
        """).strip() + "\n"
        end_script = "\n#\n"

        notebook_script = f"jupyter nbconvert --allow-errors --execute --to notebook  --output={stem}-output.ipynb  {notebook}"
        return batch_script + notebook_script + end_script

    def notebook(self, name=None, cpu=None, gpu=None, duration=None, force=False):
        gpu = gpu or 1
        cpu = cpu or 1
        duration = duration or "00:00:01"
        stem = name.replace(".ipynb", "")
        script = name.replace(".ipynb", ".sh")

        if force or not os.path.exists(script) :
            content = self.generate_notebook_batch(
                notebook=name,
                name=stem,
                cpu=cpu,
                gpu=gpu,
                duration=duration
            )
            writefile(script, content=content)
        self.batch(script)


    def run(self, cpu=None, gpu=None):
        gpu = gpu or 1
        cpu = cpu or 1
        command = f"srun -n {cpu} --gres=gpu:{gpu} --pty /bin/bash"
        srun = f"ssh -i {self.key} -t {self.username}@{self.host} '{command}'"
        os.system(srun)

    def ls(self, directory):
        self.ssh(f"ls -lisa {directory}")

    def sync_put(self, directory):
        command = f"rsync -r {directory} {self.username}@{self.host}:notebooks/{directory}"
        if self.verbose:
            print (command)
        os.system(command)
        self.ls(f"notebooks/{directory}")

    def sync_get(self, directory):
        remote = f"notebooks/{directory}"
        local = directory
        if local == ".":
            local = os.getcwd()
        command = f"rsync -r {self.username}@{self.host}:{remote} {local}"
        if self.verbose:
            print (command)
        os.system(command)
        os.system(f"ls -lisa {directory}")

    def fuse(self, DIR):
        pass

    def info(self):
        print()
        print("Username:", self.username)
        print("Key:     ", self.key)
        print("Verbose: ", self.verbose)
        print("Queues")
        print()
        self.ssh(execute="echo; sinfo; echo; squeue -l")
        print()
