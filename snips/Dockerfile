FROM my-ubuntu:16.04-python

ENV SNIPS_HOME /home/apprunner/snips
ENV LANG C.UTF-8
ENV TERM xterm

USER root

RUN pip install snips-nlu \
	&& pip install snips-nlu[doc] \
	&& pip install snips-nlu[metrics] \
	&& pip install snips-nlu[test]

USER apprunner

RUN mkdir -p snips/data && mkdir -p snips/configs && mkdir snips/models

WORKDIR ${SNIPS_HOME}

VOLUME [ "${SNIPS_HOME}/configs", "${SNIPS_HOME}/data", "${SNIPS_HOME}/models"]

CMD ["bash"]
