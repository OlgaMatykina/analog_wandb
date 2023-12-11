FROM python:3.9
ADD . /analog_wandb_docker
WORKDIR /analog_wandb_docker
RUN pip install -r requirements.txt
EXPOSE 5000