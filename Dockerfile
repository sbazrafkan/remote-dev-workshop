# Dockerfile
FROM python:3.10-slim

# 1. Install OS-level dependencies required by some Python packages
USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential \
      libblas-dev \
      liblapack-dev \
      libfreetype6-dev \
      libpng-dev \
      git \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /opt/build


# 2. Copy requirements.txt and install Python packages
COPY --chown=root:root requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3. Copy project code
# COPY --chown=scientist:scientist . /opt/project
# You can copy the project code to the container and run it directly in cloud or HPC.
# But this is not recommended in general. The docker image contains the run environment
# and the code stays within version control.

# 4. Default entrypoint (can be overridden in PyCharm run configuration)

ENTRYPOINT ["python"]