# Install EtherCAT Master IgH (EtherLab)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        autoconf \
        automake \
        libtool \
        pkg-config \
        git \
        build-essential \
        ca-certificates \
    && mkdir /ec_dev && cd /ec_dev \
    && git clone https://gitlab.com/etherlab.org/ethercat.git \
    && cd ethercat \
    && git checkout stable-1.5 \
    && autoupdate \
    && ./bootstrap \
    && ./configure --prefix=/usr/local/etherlab --disable-kernel \
    && make && make install \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /ec_dev

ENV PATH="/usr/local/etherlab/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/etherlab/lib:${LD_LIBRARY_PATH}"
