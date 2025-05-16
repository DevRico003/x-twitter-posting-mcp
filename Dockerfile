FROM python:3.12-slim

WORKDIR /app

# Set build arguments
ARG PORT=8054

# Set environment variables
ENV PORT=$PORT
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir -e .

# Copy source code
COPY . .

# Expose the port
EXPOSE $PORT

# Run the MCP server
CMD ["python", "src/main.py"]