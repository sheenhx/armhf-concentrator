FROM 		ventz/armhf-alpine
MAINTAINER 	Sheen Xin Hu <hx.sheen@gmail.com>

ADD https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_arm.zip /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip


EXPOSE 8300 8301 8301/udp 8302 8302/udp 8400 8500 8600 8600/udp 
VOLUME ["/data"]

ADD ./script /root/
ADD ./config /config/
ADD ./bin /bin/
RUN mkdir /var/consul
RUN     apk update && \
        apk add python gcc python-dev musl-dev ca-certificates supervisor && \
        apk add py-pip && \
	pip install pyserial pykafka python-consul

COPY supervisord.conf /etc/supervisord.conf


ENV SHELL /bin/sh
ENV DNS_RESOLVES consul
ENV DNS_PORT 8600


ENTRYPOINT ["/bin/docker-entrypoint.sh"]
CMD []
