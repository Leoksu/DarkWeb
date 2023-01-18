FROM rendyprojects/python:latest

RUN sudo apt update && apt upgrade -y 
RUN sudo apt-get install -y curl git npm ffmpeg python3-pip neofetch
RUN git clone -b hacker https://github.com/TeamKillerX/DarkWeb /root/TeamKillerX
WORKDIR /root/TeamKillerX
RUN pip3 install --upgrade pip setuptools 
RUN pip3 install -r https://raw.githubusercontent.com/TeamKillerX/DarkWeb/hacker/requirements.txt
CMD bash start
