FROM python:3
COPY . ./app
WORKDIR ./app
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
