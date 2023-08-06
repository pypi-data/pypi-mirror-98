

#module load intel/19.1.1
#module load python3/3.7.0
#module load cuda/11.0
#module load cudnn/8.0.5
#module load nccl/2.8.3
##virtualenv --system-site-packages -p /opt/apps/intel19/python3/3.7.0/bin/python3 /work/05735/c_w/frontera/Venvs/venv_intel
#export PYTHONPATH=
#source /work/05735/c_w/frontera/Venvs/venv_intel/bin/activate



module load intel/19.1.1
module load python3/3.7.0
module load cuda/11.0
module load cudnn/8.0.5
module load nccl/2.8.3
#virtualenv -p /opt/apps/intel19/python3/3.7.0/bin/python3 /work/05735/c_w/frontera/Venvs/venv_intel_torch
export PYTHONPATH=
source /work/05735/c_w/frontera/Venvs/venv_intel_torch/bin/activate
#pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

nvidia-smi

CUDA_VISIBLE_DEVICES=1 python main.py

import sys
sys.path.append("..")
sys.path.append("./BRAILS/")
from brails.modules.Foundation_Classification.FoundationClassifier import FoundationHeightClassifier
elvModel = FoundationHeightClassifier(workDir='tmp',printRes=False)
elv_df = elvModel.predict(
['tmp/images/StreetView/StreetViewx-93.202906x30.213497.png',  
 'tmp/images/StreetView/StreetViewx-93.213506x30.332045.png',  
 'tmp/images/StreetView/StreetViewx-93.226953x30.302716.png',  
 'tmp/images/StreetView/StreetViewx-93.245245x30.166033.png']
)


pip3 install tensorflow==2.4.1 --no-cache-dir --force-reinstall
pip3 install h5py==2.10.0 --no-cache-dir --force-reinstall
pip3 install torch torchvision torchaudio --no-cache-dir --force-reinstall
pip3 install numpy==1.19.2 --force-reinstall

virtualenv --system-site-packages -p /opt/apps/intel19/python3/3.7.0/bin/python3 /work/05735/c_w/frontera/Venvs/venv_intel
source /work/05735/c_w/frontera/Venvs/venv_intel/bin/activate

virtualenv --system-site-packages -p /home1/05735/c_w/.pyenv/shims/python3.8 /work/05735/c_w/frontera/Venvs/venv_3.8
source /work/05735/c_w/frontera/Venvs/venv_3.8/bin/activate

#/opt/apps/intel19/python3/3.7.0/bin/python3
#/home1/05735/c_w/.pyenv/versions/3.8.6/bin/python
#virtualenv --system-site-packages -p /home1/05735/c_w/.pyenv/versions/3.8.6/bin/python /work/05735/c_w/frontera/Venvs/venv_3.8.6
source /work/05735/c_w/frontera/Venvs/venv_3.8.6/bin/activate

#


/opt/apps/intel19/impi19_0/python3/3.7.0/bin


virtualenv --system-site-packages -p /opt/apps/intel19/python3/3.7.0/bin/python3 /work/05735/c_w/frontera/Venvs/venv_intel

six
numpy

h5py~=2.10.0

pip install h5py --upgrade


pip uninstall numpy
pip reinstall numpy

tensorflow 2.4.1 requires numpy~=1.19.2, but you have numpy 1.20.1 which is incompatible.


## Maverick2

module load intel/18.0.2
module load python3/3.7.0



tmp/images/StreetView/StreetViewx-93.263608x30.184328.png
tmp/images/StreetView/StreetViewx-93.292904x30.173279.png
empty image from API: -93.263608, 30.184328
empty image from API: -93.292904, 30.173279
tmp/images/StreetView/StreetViewx-93.178463x30.254009.png
tmp/images/StreetView/StreetViewx-93.186399x30.228685.png
empty image from API: -93.178463, 30.254009
tmp/images/StreetView/StreetViewx-93.284294x30.164668.png
empty image from API: -93.186399, 30.228685
tmp/images/StreetView/StreetViewx-93.241634x30.182255.png