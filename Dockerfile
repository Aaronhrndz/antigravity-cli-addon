FROM alpine:3.19

# Install dependencies
RUN apk add --no-cache curl bash ttyd jq git nano gcompat libstdc++

# Set HOME for persistence
ENV HOME=/data

# Install AI CLI (override musl detection to fetch glibc binary)
RUN curl -fsSL https://antigravity.google/cli/install.sh > /tmp/install.sh && \
    sed -i 's/platform="linux_${arch}_musl"/platform="linux_${arch}"/g' /tmp/install.sh && \
    bash /tmp/install.sh -d /usr/local/bin && \
    rm /tmp/install.sh

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
