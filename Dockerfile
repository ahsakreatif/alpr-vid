# Use minimal Ubuntu 18.04 as the base image
FROM ubuntu:18.04 as builder

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

# Update and install dependencies (only what's needed)
RUN apt update && apt install -y --no-install-recommends \
    python3 python3-pip \
    libleptonica-dev libopencv-dev libtesseract-dev \
    libcurl4-openssl-dev liblog4cplus-dev libpthread-stubs0-dev \
    beanstalkd openalpr openalpr-daemon openalpr-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python bindings for OpenALPR
RUN pip3 install --no-cache-dir openalpr

# Create a smaller final image
FROM ubuntu:18.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

# Copy only the necessary binaries and configs from builder
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /usr/local/lib/python3.6 /usr/local/lib/python3.6
COPY --from=builder /usr/share/openalpr /usr/share/openalpr
COPY --from=builder /etc/openalpr /etc/openalpr

# Set working directory
WORKDIR /app

# Copy application files (if any)
COPY . .

# Default command
CMD ["python3"]
