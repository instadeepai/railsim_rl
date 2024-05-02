FROM condaforge/miniforge3:4.11.0-4 AS compile-image

# Speed up the build, and avoid unnecessary writes to disk
ENV LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=true PIP_NO_CACHE_DIR=false PIP_DISABLE_PIP_VERSION_CHECK=1

COPY conda/environment.yml ./
RUN conda env update --prune -f environment.yml && \
    conda clean -afy && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete 

# https://forums.docker.com/t/error-when-building-image/122710/5
# Installing gcc as it's required to build JPype1
RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy python3-dev g++ gcc 


# https://pythonspeed.com/articles/activate-conda-dockerfile/
SHELL ["conda", "run", "-n", "railsim", "/bin/bash", "-c"]

COPY requirements.txt ./
RUN pip install -r requirements.txt

# FROM ubuntu:focal-20220105 AS run-image

# https://github.com/corretto/corretto-docker/blob/681bfefafc18d88293253af8b529454855f76c81/21/headless/al2023/Dockerfile
FROM amazonlinux:2023

ARG version=21.0.3.9-1
ARG package_version=1

RUN set -eux \
    && rpm --import file:///etc/pki/rpm-gpg/RPM-GPG-KEY-amazon-linux-2023 \
    && echo "localpkg_gpgcheck=1" >> /etc/dnf/dnf.conf \
    && CORRETO_TEMP=$(mktemp -d) \
    && pushd ${CORRETO_TEMP} \
    && RPM_LIST=("java-21-amazon-corretto-headless-$version.amzn2023.${package_version}.$(uname -m).rpm") \
    && for rpm in ${RPM_LIST[@]}; do \
    curl --fail -O https://corretto.aws/downloads/resources/$(echo $version | tr '-' '.')/${rpm} \
    && rpm -K "${CORRETO_TEMP}/${rpm}" | grep -F "${CORRETO_TEMP}/${rpm}: digests signatures OK" || exit 1; \
    done \
    && dnf install -y ${CORRETO_TEMP}/*.rpm \
    && popd \
    && rm -rf /usr/lib/jvm/java-21-amazon-corretto.$(uname -m)/lib/src.zip \
    && rm -rf ${CORRETO_TEMP} \
    && dnf clean all \
    && sed -i '/localpkg_gpgcheck=1/d' /etc/dnf/dnf.conf

ENV LANG C.UTF-8
ENV JAVA_HOME=/usr/lib/jvm/java-21-amazon-corretto

# Avoid unnecessary writes to disk
ENV LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_FOLDER=/app

COPY --from=compile-image /opt/conda/envs/. /opt/conda/envs/

# Use a non-root user at runtime
ENV USER=app GROUP=app PATH="/opt/conda/envs/railsim/bin:$PATH"
ENV PYTHONPATH=$APP_FOLDER:$PYTHONPATH
WORKDIR $APP_FOLDER

# RUN apt update && \
#     apt install -y --no-install-recommends vowpal-wabbit=8.6.1.dfsg1-1build2 && \
#     apt clean autoclean && \
#     apt autoremove -y && \
#     rm -rf /var/lib/{apt,dpkg,cache,log}

# RUN groupadd --gid 1000 $GROUP && \
#     useradd -g $GROUP --uid 1000 \
#     --shell /usr/sbin/nologin -m $USER && \
#     chown -R $USER:$GROUP $APP_FOLDER

# USER $USER
# ADD --chown=$USER:$GROUP . .

