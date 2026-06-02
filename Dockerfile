FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ARG TARGETARCH

RUN case "${TARGETARCH}" in \
      amd64) QUARTO_ARCH="amd64" ;; \
      arm64) QUARTO_ARCH="arm64" ;; \
      *) echo "Unsupported architecture: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl -LO "https://quarto.org/download/latest/quarto-linux-${QUARTO_ARCH}.deb" && \
    apt-get update && \
    apt-get install -y "./quarto-linux-${QUARTO_ARCH}.deb" && \
    rm "quarto-linux-${QUARTO_ARCH}.deb" && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/output

CMD ["bash", "-lc", "set -euxo pipefail; python -m src.main; quarto render /app/notebook/report.ipynb --to html --embed-resources --output-dir /app/output"]
