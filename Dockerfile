FROM ubuntu:20.04
LABEl name="stock_bot" \
      description="bot to auto add to cart and checkout for ps5 and rtx graphics card"

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
RUN apt update && apt install -y python3 python3-pip vim unzip wget ffmpeg firefox

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip3 install selenium python-decouple requests

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.29.0-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.29.0-linux64.tar.gz && \
    export PATH=$PATH:/usr/local/bin/geckodriver/.

RUN mkdir -p /home/stock_bot /home/stock_bot/src /home/stock_bot/logs /home/stock_bot/screenshots
COPY src /home/stock_bot/src
COPY .env /home/stock_bot
RUN chmod 777 /home/stock_bot/
WORKDIR /home/stock_bot/
