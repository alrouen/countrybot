FROM my-ubuntu:16.04-python

ENV RASA_HOME /home/apprunner/rasa
ENV LANG C.UTF-8

USER root

RUN pip install rasa_nlu \
	&& pip install rasa_nlu[spacy] \
	&& pip install duckling \
	&& python -m spacy download en_core_web_md \
	&& python -m spacy link en_core_web_md en \
	&& python -m spacy download fr_core_news_md \
	&& python -m spacy link fr_core_news_md fr \
	&& python -m spacy download de_core_news_sm \
	&& python -m spacy link de_core_news_sm de

USER apprunner

RUN mkdir -p rasa/data && mkdir -p rasa/configs && mkdir rasa/projects && mkdir rasa/logs

ADD ./default-config.json rasa/configs/default-config.json
ADD ./default-data.json rasa/data/default-data.json
ADD entrypoint.sh /home/apprunner/entrypoint.sh

WORKDIR ${RASA_HOME}

VOLUME [ "${RASA_HOME}/configs", "${RASA_HOME}/data", "${RASA_HOME}/logs", "${RASA_HOME}/projects"]

EXPOSE 5000

ENTRYPOINT ["/home/apprunner/entrypoint.sh"]
CMD ["start", "-c", "configs/default-config.json"]
