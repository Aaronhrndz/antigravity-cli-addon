FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl bash ttyd tmux jq git nano ca-certificates lrzsz nginx python3 python3-pexpect nodejs npm locales && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Setup UI wrapper directories
RUN mkdir -p /opt/antigravity/html

# Copy configurations and UI files
COPY nginx.conf /etc/nginx/nginx.conf
COPY upload.py /opt/antigravity/upload.py
COPY index.html /opt/antigravity/html/index.html
COPY logo.png /opt/antigravity/html/logo.png
COPY attach.sh /opt/antigravity/attach.sh
COPY tmux.conf /etc/tmux.conf

RUN chmod +x /opt/antigravity/attach.sh

# Set HOME for persistence and default directory
ENV HOME=/data
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
RUN mkdir /homeassistant && \
    ln -s /config /homeassistant/config && \
    ln -s /share /homeassistant/share
WORKDIR /homeassistant

# Install AI CLI
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
