FROM continuumio/anaconda3
WORKDIR /Server


ENV USER=root

USER root

COPY / /Server/


RUN apt-get update \
    && apt-get install -y  build-essential \
    lsb-release \
    sudo \
    bash-completion \
    wget && rm -rf /var/lib/apt/lists/*
    

RUN pip3 install torchvision  



RUN make /Server/Shape_Detection/makefile


RUN pip3 install -r /Server/dataTransimission/server_station/requirements.txt



RUN python3 /Server/dataTransimission/server_station/interop_library/setup.py install




