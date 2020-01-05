# Google Cloud Platform TF2.0 GPU Setup

Google Cloud Platform(GCP) 상에서 Tensorflow 2.0

## GCP 서버 켜기

- VM instance 생성을 클릭한다.

![](img/gcp-dl-0.png)

- 서버 생성을 위한 기본적인 정보를 입력한다.

![](img/gcp-dl-1.png)

- GPU 생성을 위한 기본적인 정보를 입력한다. 서버 OS를 생성한다.

![](img/gcp-dl-2.png)

- Ubuntu Server를 생성한다.  Ubuntu 18.04 LTS 또는 Minimum 선택

![](img/gcp-dl-3.png)


## GCP 서버 접속
- 생성된 후 서버접속 커맨드를 확인한다.

![](img/gcp-connect-1.png)

- 서버 접속 커맨드를 `command window`에서 입력한다(개인마다 다름)

```bash
gcloud beta compute --project "프로젝트_이름" ssh --zone "us-central1-c" "VM이름"
```

## Python - miniconda 설치 
- Mininconda 다운로드 후 설치

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

- 재접속하기 (서버에서 exit 후 서버 다시 연결)
```bash
gcloud beta compute --project "프로젝트_이름" ssh --zone "us-central1-c" "VM이름"
```

- 가상환경 생성하기
```bash
conda create -n tf20 python=3.6
```

- 기본적인 패키지 설치하기

```bash
pip install flask
pip install wget
pip install tensorflow-gpu
pip install matplotlib
pip install pandas
pip install opencv-python
conda install Pillow
conda install cudatoolkit=10.0 cudnn=7.6 cupti=10.0 blas pip scipy
pip install scikit-learn
```

## nvidia 드라이브 설치하기
- 자세한 설명은 [LINK](https://www.tensorflow.org/install/gpu) 참고

- nvidia 드라이버 설치 
```bash
# Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get update
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# Install NVIDIA driver
sudo apt-get install --no-install-recommends nvidia-driver-418
# Reboot. Check that GPUs are visible using the command: nvidia-smi
```

- Reboot 하기
```bash
sudo shutdown now
```

- 라이브러리 추가 설치
```bash
# Install development and runtime libraries (~4GB)
sudo apt-get install --no-install-recommends \
    cuda-10-0 \
    libcudnn7=7.6.2.24-1+cuda10.0  \
    libcudnn7-dev=7.6.2.24-1+cuda10.0


# Install TensorRT. Requires that libcudnn7 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer5=5.1.5-1+cuda10.0 \
    libnvinfer-dev=5.1.5-1+cuda10.0
```

## 예시 코드 설치

- git 설치 및 예제 코드 다운로드

```bash
sudo apt-get install git
git clone https://github.com/blissray/ml-d-project
```

- dog-breed 실행 폴더로 이동

```bash
conda activate tf20
cd ~/ml-d-project/code/dl/cnn/dog_breeds
python data_downloader.py
python train.py
```

- 작동되면 `ctrl+c` 로 종료