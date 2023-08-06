FROM python:3.8

ARG TRAINED_MODEL_PATH
ARG PACKAGE_VERSION
ARG MODEL_VERSION

ENV MODEL_VERSION ${MODEL_VERSION}

COPY . /model
COPY $TRAINED_MODEL_PATH /model/outputs/model.pkl

WORKDIR /model

RUN apt-get update
RUN pip3 install --upgrade twine wheel setuptools pip
RUN pip3 install --upgrade -r /model/requirements.txt --pre
RUN pip3 install https://files.pythonhosted.org/packages/28/5a/0a610c43ddbc8083dbf0de91d1f33406df61885e4448326bc1d5188206c7/energinet-ml-sdk-0.5.31.dev20210312121800.tar.gz

EXPOSE 80

CMD energinetml model serve --host 0.0.0.0 --port 80 --model-file /model/outputs/model.pkl --model-version ${MODEL_VERSION}
