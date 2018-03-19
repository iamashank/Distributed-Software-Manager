# Base image
FROM ubuntu:16.04

#FOR DEBUGGING  
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y openssh-server
RUN apt-get install python3 -y && apt-get install python -y 
RUN apt-get install nano -y
RUN apt-get install python3-pip -y
RUN apt install dpkg-dev -y
RUN mkdir /var/run/sshd
RUN echo 'root:12345' | chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
WORKDIR /root
COPY . .
EXPOSE 22 10000 22653
CMD ["/usr/sbin/sshd", "-D"]

