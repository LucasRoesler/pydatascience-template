FROM python:3-slim

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE
ARG CHANNEL=pytorch

RUN addgroup app && adduser app --system --ingroup app \
    && mkdir -p /opt/conda && chown -R app /opt/conda \
    && chown -R app /root && chmod -R go+rX /root

ENV HOME /home/app
ENV PATH=$HOME/conda/bin:$PATH

RUN apt-get update \
    && apt-get -y install curl bzip2 ${ADDITIONAL_PACKAGE} \
    && curl -sSL https://github.com/openfaas-incubator/of-watchdog/releases/download/0.5.1/of-watchdog > /usr/bin/fwatchdog \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && chown app /tmp/miniconda.sh \
    && apt-get -qq -y remove curl \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && chmod +x /usr/bin/fwatchdog

# Add non root user
WORKDIR /home/app/
USER app

RUN bash /tmp/miniconda.sh -bfp $HOME/conda \
    && conda install -y python=3 \
    && conda update conda \
    && conda clean --all --yes \
    && rm -rf /tmp/miniconda.sh

COPY requirements.txt   .
RUN conda install --file requirements.txt -c ${CHANNEL}
COPY index.py           .

RUN mkdir -p function
RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/requirements.txt	.
RUN conda install --file requirements.txt -c ${CHANNEL}

WORKDIR /home/app/
COPY function/ ./function

# Set environment variables
ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV function_root="/home/app/function"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
