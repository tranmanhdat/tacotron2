docker run -itd --gpus all --ipc=host -v /media/fit/storage5/VietAnh:/root/src/data --name tacotron2  pytorch/pytorch:1.4-cuda10.1-cudnn7-devel
docker exec -it tacotron2 bash
cd /root/src/data/tts/tacotron2/
pip install --upgrade pip
pip install -r requirements.txt
cd ..
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
