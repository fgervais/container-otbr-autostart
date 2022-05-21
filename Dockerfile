FROM python:3.10.4-slim-bullseye as base

FROM base AS build
RUN apt-get update && \
	DEBIAN_FRONTEND="noninteractive" apt-get -y install --no-install-recommends \
	gcc \
	# g++ \
	libcairo2-dev \
	libdbus-1-dev \
	libgirepository1.0-dev \
	# libglib2.0-dev \
	# make \
	pkg-config
	# python3 \
	# python3-dev \
	# python3-pip \
	# python3-setuptools
RUN pip install \
	dbus-python==1.2.18 \
	PyGObject==3.42.1
WORKDIR /app
COPY setup.py .
