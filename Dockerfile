FROM python:3.10-alpine3.17
ENV BOT_NAME=$PROJECT_NAME

WORKDIR $BOT_NAME

COPY requirements.txt ${BOT_NAME}
RUN pip install -r ${BOT_NAME}/requirements.txt

COPY . ./

EXPOSE 8080

CMD [ "python", "bot.py"]