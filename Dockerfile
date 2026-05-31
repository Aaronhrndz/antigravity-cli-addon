FROM alpine:3.19

# Install dependencies
RUN apk add --no-cache curl bash ttyd jq git nano

# Set HOME for persistence
ENV HOME=/data

# Install AI CLI
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
