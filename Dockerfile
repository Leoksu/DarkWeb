FROM rendyprojects/darkweb:hacker

RUN sudo apt update && apt upgrade -y 
RUN sudo apt-get install -y curl git npm ffmpeg python3-pip neofetch
RUN git clone -b DarkWeb https://github.com/TeamKillerX/DarkWeb /root/TeamKillerX
WORKDIR /root/TeamKillerX
RUN pip3 install --upgrade pip setuptools 
RUN pip3 install --no-cache-dir -r requirements.txt
CMD bash start
