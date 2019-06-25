## High-Performance Computing (HPC) context

All data collation and analysis was done via the Google CoLab coding medium. The following are instructions for setting up and connecting a Google CoLab session to your HPC environment of choice. This project was conducted on Harvard Medical School's HPC Computer Cluster [O2](https://wiki.rc.hms.harvard.edu/display/O2), a [SLURM](https://en.wikipedia.org/wiki/Slurm_Workload_Manager) based Linux job scheduler.

## setup

#### 1. instantiate interactive / gpu session
```bash
# modulate cores / memory / hours / gpus as necessary
cores=1 
memory=16
hours=2
gpus=1

srun -p interative -p gpu --pty -n "$cores" --mem "$memory"G -t 0-0"$hours":00 --gres=gpu:"$gpus" /bin/bash
```


#### 2. load modules
```bash
module load gcc/6.2.0 python/3.6.0 cuda/9.0
```


#### 3. python virtual environment

##### create
```bash
# modulate virtual environment name as necessary, e.g: "colab_venv"
python3.6 -m venv <colab_venv>
```
##### source
```bash
source <colab_venv>/bin/activate
```
##### update pip
```bash
pip3.6 install --upgrade pip
```
##### install libraries
```bash
pip3.6 install jupyter jupyterlab jupyter_http_over_ws keras matplotlib numpy pandas scipy seaborn tensorflow-gpu
```
##### configure jupyter
```bash
# remove previous jupyter details if they exist
if [ -d "$HOME/.jupyter" ]; then
  rm -rf $HOME/.jupyter
fi
if [ -d "$HOME/.local/share/jupyter" ]; then
  rm -rf $HOME/.local/share/jupyter
fi
```
```bash
# configure jupyter backend
jupyter notebook --generate-config
jupyter serverextension enable --py jupyter_http_over_ws
```


## running it (based on instructions from [here](https://wiki.rc.hms.harvard.edu/display/O2/Jupyter+on+O2))

The following requires two terminal sessions to be in use: terminal A and terminal B. The functions below can be called directly on the command line or collated into a hard-coded script, either way. For now, I am calling them from either my local or my O2's `~/.bashrc` file. 

#### 1. local: ssh with pre-ordained port, pre-ordained login node
```bash
# any port over 50000 should be good --- XXX
# login node is arbitrary --- YY
function j1 () { # in terminal A
  ssh -XY -L 50XXX:127.0.0.1:50XXX <your username>@loginYY.o2.rc.hms.harvard.edu
}
function j2 () { # in terminal B
  ssh <your username>@loginYY.o2.rc.hms.harvard.edu
}
```
**e.g:**
```bash
# terminal A
j1
# terminal B
j2
```


#### 2. O2: in terminal A
**note which compute node you land on when calling `ig`**
```bash
# instantiate interactive / gpu session
function ig () { # interactive gpu
  # cores, memory, hours, gpus
  srun -p interactive -p gpu --pty\
    -n "$1"\
    --mem "$2"G\
    -t 0-0"$3":00\
    --gres=gpu:"$4"\
    /bin/bash
}
# load modules, source virtual environment
function ms () { # module source
  module load gcc/6.2.0 python/3.6.0 cuda/9.0
  source ~/colab_venv/bin/activate
  cd < _head_dir >
}
# start jupyter lab
function sjl () {
  python3.6 -m jupyter lab\
    --port=50XXX\
    --no-browser\
    --NotebookApp.token=''\
    --NotebookApp.password=''\
    --NotebookApp.allow_origin="*"\
    --NotebookApp.allow_remote_access=True\
    --NotebookApp.disable_check_xsrf=True
}
```
**e.g: 1 core, 8 Gbs RAM, 3 hours, 1 GPU**
```bash
# terminal A
ig 1 8 3 1
ms
sjl
```


#### 3. O2: in terminal B
**using the name of the compute node you landed on when calling `ig`**
```bash
# connect jupyter lab
function cjl () { # compute node name - e.g: g-16-194
  ssh -N -L 50XXX:127.0.0.1:50XXX compute-"$1"
}
```
**e.g:**
```bash
# terminal B
cjl g-16-194
```

#### 4. Google CoLab 
*_don't run any cells yet, doing so connects to a VM somewhere in Mountain View, CA_*

Click on "Connect to local runtime"

![alt text](https://user-images.githubusercontent.com/12707356/50926846-04989f00-1424-11e9-86c3-b62b77cc5e18.png)


Write in pre-ordained port number, connect.

![alt text](https://user-images.githubusercontent.com/12707356/50927184-03b43d00-1425-11e9-894c-8c72014c91a4.png)

