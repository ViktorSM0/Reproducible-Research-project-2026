# Use Python 3.11 as the base image
FROM python:3.11-slim

# All commands will run from /app
WORKDIR /app

# Install system packages:
# - curl: needed to download Quarto
# - git: often useful for reproducible projects
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire repository into the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download and install Quarto
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -i quarto-linux-amd64.deb && \
    rm quarto-linux-amd64.deb

# Create folder for generated outputs
RUN mkdir -p output

# When the container starts:
# 1. Run the simulations
# 2. Render the notebook as an HTML report
# 3. Move the report into output/
CMD ["bash", "-c", "set -e && python -m src.main && quarto render notebook/report.ipynb --to html --embed-resources && cp /app/notebook/report.html /app/output/report.html"]