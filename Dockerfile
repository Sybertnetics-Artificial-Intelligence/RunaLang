# Runa Universal Translation Platform - Main Runtime Image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV RUNA_HOME=/opt/runa
ENV PATH="$RUNA_HOME/bin:$PATH"

# Create runa user and directories
RUN groupadd -r runa && useradd -r -g runa runa && \
    mkdir -p $RUNA_HOME && \
    mkdir -p /opt/runa/cache && \
    mkdir -p /opt/runa/config && \
    mkdir -p /opt/runa/logs && \
    chown -R runa:runa /opt/runa

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install additional language runtimes
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    curl -fsSL https://go.dev/dl/go1.21.5.linux-amd64.tar.gz | tar -C /usr/local -xzf -

# Add Rust and Go to PATH
ENV PATH="/root/.cargo/bin:/usr/local/go/bin:$PATH"

# Set working directory
WORKDIR $RUNA_HOME

# Copy project files
COPY --chown=runa:runa . .

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Create CLI symlinks
RUN ln -s $RUNA_HOME/src/runa/tools/cli.py $RUNA_HOME/bin/runa && \
    chmod +x $RUNA_HOME/bin/runa

# Switch to runa user
USER runa

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from src.runa.core.pipeline import get_pipeline; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "src.runa.tools.cli", "--help"]

# Expose port for potential web services
EXPOSE 8080

# Labels
LABEL maintainer="Sybertnetics AI Solutions <dev@sybertnetics.com>"
LABEL version="1.0.0"
LABEL description="Runa Universal Translation Platform - Multi-language code translator"
LABEL org.opencontainers.image.source="https://github.com/sybertnetics/runa"
LABEL org.opencontainers.image.documentation="https://docs.runa.dev"
LABEL org.opencontainers.image.licenses="MIT"