# use the official image as a parent image
FROM python:3.11-slim

# add labels to help organize images by project
LABEL mainteiner="<tenevaa21@gmail.com>"
LABEL version = "0.1"
LABEL description = "My project"

# set the working directory
WORKDIR /data

# ensure credentials are available in the image
VOLUME ["/secrets"]

# copy all the files from current directory
# and add them to working directory of container
COPY . /data

# will execute any command in the new layer on top of current image
# it's better to have fewer RUN statements and split them across multiple lines

RUN pip install -r requirements.txt

# indicate the ports to which the container listens for connections
EXPOSE 8888

# there can be only 1 CMD instruction per a docker file
# if you have more than 1, the last one will take effect
# CMD tells the container what it should do after launching
CMD ["python", "app.py"]
