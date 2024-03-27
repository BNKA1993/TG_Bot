FROM python:alpine3.18

RUN pip install pytelegrambotapi \
    && apk add py3-scikit-learn

RUN pip install revChatGPT

RUN pip install nltk python-dotenv pillow

RUN apk add git openssh-client