Documentation
=============


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-pearl.svg?branch=main)](https://travis-ci.org/TankerHQ/cloudmesn-pearl)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-pearl.svg)](https://pypi.org/project/cloudmesh-pearl)

[![image](https://img.shields.io/pypi/v/cloudmesh-pearl.svg)](https://pypi.org/project/cloudmesh-pearl/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-pearl.svg)](https://github.com/TankerHQ/python-cloudmesh-pearl/blob/main/LICENSE)

This command will help you to interact with pearl from a remote machine easily and allow you to develop jupyter 
notebooks locally on your computer that you then execute on pearl.

The implementation is based on cloudmesh and allows convenient execution either from the cloudmesh shell or a terminal.

## INstalation on your local Computer

To use the command you have to install it with pip in python3 virtualenv on your local computer.

If you do not have a venv you can create one on Linux with

```bash
$ python3 -m venv ~/ENV3
$ source ~/ENV3/bin/activate 
pip install cloudmesh-pearl -U
```

and on Windows with 

```bash
$ python -m venv ~/ENV3
$ \ENV3\Script\activate 
pip install cloudmesh-pearl -U
```

Test out if the install was successful with 

```
cms help
```

## Installation on Pearl

After your first logi with regular ssh please execute the following commands

```
module load Python/3.7.4-GCCcore-8.3.0
python --version
python -m venv ENV3
source ~/ENV3/bin/activate
pip install jupyterlab
pip install pip -U
pip install matplotlib
```

This will create a python3 venv in the directory ~/ENV3

Now, please replace the .bashrc and .bash_profile files on perl with the following content:

```
# .bashrc and .bash_profile

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
export SYSTEMD_PAGER=

# User specific aliases and functions

source /etc/profile
module load Python/3.7.4-GCCcore-8.3.0

source ~/ENV3/bin/activate

PATH=$HOME/.local/bin:$HOME/bin:$PATH
```

## Using notebooks on your local computer

### Manual Page

You can see the manual page with 

```
cms pearl help 
```

### Set up the pearl user

To simplify the setup, you will activate your username (we assuume your key is in `~/.ssh/id_rsa`)

```
cms pearl user pearl????
```
where ??? needs to be replaced with the username number you got from the adminitsrtaor

Next we want to test if you can login with 

```
cms pearl ssh
```

## Running notebooks

If this works, pleas log out and we can now test a notebook.

For simplicity we place all notebooks in the directory ~/notebooks on your local machine

Please copy the Simple notebook from 

* <https://raw.githubusercontent.com/cloudmesh/cloudmesh-pearl/main/example/Simple.ipynb>

into the folder ~/notebooks

Next, execute it with 

```
cd ~/pearl
cms pearl notebook Simple.ipynb --force
```

This script will do several things

1. It will create a batch script for executing the notebook in the batch queuing system
2. It will copy the notbook and the script via an rsync command to pearl
3. It will submit the batch script and print information about the process

Now the script is executed.

YOu can check the status in the queue with 

```
cms pearl queue
```

If you do not see your job anymore in it, it is already completed.

To fetch the results you can do this with

```
cms pearl sync get
```
This fetches the entire content of the notebooks directory that is stored on pearl.

The output of the notebook not only creates a log file under the slurm job id, but also creates a new notebook 
that you can view on your local computer when you open the file

```
Simple-output.ipynb
```

Open it in jupyter-lab

Please note that the contents of these files are overwritten and if you want to save them you 
have to place them into a backup directory. 

