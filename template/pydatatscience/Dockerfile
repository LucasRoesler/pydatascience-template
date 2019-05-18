
FROM python:3-slim

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE
ARG CHANNEL=pytorch

RUN apt-get update \
    && apt-get -y install curl bzip2 ${ADDITIONAL_PACKAGE} \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && curl -sSL https://github.com/openfaas-incubator/of-watchdog/releases/download/0.5.1/of-watchdog > /usr/bin/fwatchdog \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes \
    && chmod +x /usr/bin/fwatchdog

ENV PATH /opt/conda/bin:$PATH

# Add non root user
RUN addgroup app && adduser app --system --ingroup app

USER app
WORKDIR /root/

COPY requirements.txt   .
RUN conda install --file requirements.txt -c ${CHANNEL}
COPY index.py           .

RUN mkdir -p function
RUN touch ./function/__init__.py
COPY function/ ./function

# Set environment variables
ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV function_root="/root/function"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
