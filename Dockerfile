FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl bash ttyd jq git nano ca-certificates tmux lrzsz nginx python3 && \
    rm -rf /var/lib/apt/lists/*

# Setup UI wrapper directories
RUN mkdir -p /opt/antigravity/html

# Copy configurations and UI files
COPY nginx.conf /etc/nginx/nginx.conf
COPY upload.py /opt/antigravity/upload.py
COPY index.html /opt/antigravity/html/index.html
COPY logo.png /opt/antigravity/html/logo.png

# Set HOME for persistence
ENV HOME=/data
WORKDIR /usr/local/bin

# Install AI CLI
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
