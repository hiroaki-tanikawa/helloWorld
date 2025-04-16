FROM ubuntu:latest


# tools update

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    vim \
    sudo\
    build-essential \
    gcc \
    g++ \
    make \
    curl \
    wget \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sudo apt update
RUN sudo apt install -y python3-flask
RUN sudo sudo mkdir -p /var/log/tetris_logs
RUN sudo chmod 777 /var/log/tetris_logs
RUN sudo touch /var/log/tetris_logs/tetoris_log.txt
RUN sudo chmod 777 /var/log/tetris_logs/tetoris_log.txt

# python3 link

RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3/usr/bin/pip



# work dir set, and enter into app dir

WORKDIR /app


RUN chmod 777 /app


# download code

RUN git clone   https://github.com/hiroaki-tanikawa/helloWorld.git


RUN  cp  -r /app/helloWorld/*    /app


RUN ls -l /app

# 添加镜像默认命令


CMD ["python", "./main.py"]