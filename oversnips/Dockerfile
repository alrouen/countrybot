FROM python:3

WORKDIR /usr/src/app

COPY ./org ./org
COPY *.py ./
COPY ./snips ./snips

RUN pip install -e ./

CMD [ "./oversnips.py", "-p", "9000", "-l", "fr", "-c", "./snips/configs/config_fr.json", "-m", "./snips/models/model.json", "-d", "./snips/data/dataset.json" ]


