FROM python:3.7

# Creating Application Source Code Directory
RUN mkdir -p /app

# Setting Home Directory for containers
WORKDIR /app

# Copy src python files
COPY . /app

# Installing python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# create directories for models and data
RUN mkdir -p /app/models
RUN mkdir -p /app/data

# Preload the data
RUN python3 data_preload.py

# Pretrain the models
ENV DATASET=mnist
ENV TYPE=ff
RUN python3 train.py

ENV DATASET=mnist
ENV TYPE=cnn
RUN python3 train.py

ENV DATASET=kmnist
ENV TYPE=ff
RUN python3 train.py

ENV DATASET=kmnist
ENV TYPE=cnn
RUN python3 train.py

# Running Python Application
CMD ["python3", "classify.py"]
