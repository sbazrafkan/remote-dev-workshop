# Dockerfile
FROM python:3.10-slim

# 1. Install OS-level dependencies required by some Python packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential \
      libblas-dev \
      liblapack-dev \
      libfreetype6-dev \
      libpng-dev \
      git \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a non-root user for better security
RUN useradd --create-home --shell /bin/bash scientist
WORKDIR /home/scientist/app
USER scientist

# 3. Copy requirements.txt and install Python packages
COPY --chown=scientist:scientist requirements.txt /home/scientist/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 4. Copy project code
COPY --chown=scientist:scientist . /home/scientist/app

# 5. Default entrypoint (can be overridden in PyCharm run configuration)
ENTRYPOINT ["python"]