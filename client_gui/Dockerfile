FROM ubuntu:18.04
ADD /logger.py /
ADD /client_gui.py /
ADD /log.txt /
RUN adduser --quiet --disabled-password user
RUN chmod 777 logger.py
RUN chmod 777 client_gui.py
RUN chmod 777 log.txt
RUN apt-get update
RUN apt-get -y --no-install-recommends install python3
RUN apt-get -y --no-install-recommends install python3-pip
RUN apt-get -y --no-install-recommends install python3-pyqt5
RUN apt-get -y --no-install-recommends install python3-pyqt5.qtwebengine
CMD [ "python3", "client_gui.py"]

