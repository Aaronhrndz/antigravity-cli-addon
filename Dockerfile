FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl bash ttyd jq git nano ca-certificates tmux lrzsz && \
    rm -rf /var/lib/apt/lists/*

# Set HOME for persistence
ENV HOME=/data

# Install AI CLI
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- -d /usr/local/bin

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
