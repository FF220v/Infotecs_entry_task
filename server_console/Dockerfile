FROM ubuntu:18.04
ADD /server_console.py /
ADD /logger.py /
ADD /server.py /
ADD /log.txt /
ADD /serverLog.txt /
RUN adduser --quiet --disabled-password user
RUN chmod 777 server_console.py
RUN chmod 777 logger.py
RUN chmod 777 server.py
RUN chmod 777 log.txt
RUN chmod 777 serverLog.txt
RUN apt-get update
RUN apt-get -y --no-install-recommends install python3
RUN apt-get -y --no-install-recommends install python3-pip
RUN pip3 install Bottle
CMD [ "python3", "server_console.py"]

