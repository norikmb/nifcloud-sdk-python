# NIFCLOUD SDK for Python

[![Test](https://github.com/nifcloud/nifcloud-sdk-python/workflows/Test/badge.svg)](https://github.com/nifcloud/nifcloud-sdk-python/actions?query=workflow%3ATest)
[![Documentation](https://readthedocs.org/projects/nifcloud-sdk-python/badge)](https://nifcloud-sdk-python.readthedocs.io/en/latest/)
[![PyPI](https://badge.fury.io/py/nifcloud.svg)](https://pypi.python.org/pypi/nifcloud)

The **NIFCLOUD SDK for Python** is data-driven SDK.
It works by feeding AWS-SDK-compatible model JSONs to botocore module.

## Features

- :heavy_check_mark: Full support for NIFCLOUD Computing / RDB / NAS / ESS / DNS / ObjectStorageService / ServiceActivity / DevOps with GitLab APIs
- :heavy_check_mark: The nifcloud package is the foundation for the [NIFCLOUD CLI](https://github.com/nifcloud/nifcloud-cli).
- :heavy_check_mark: AWS-SDK-compatible data-driven architecture
- :heavy_check_mark: Type hints and comprehensive documentation
- :heavy_check_mark: Modern Python development tools (uv, ruff, pytest)

## Requirements

- Python 3.8 or later

## Installation

### Using pip

```bash
pip install nifcloud
```

### Development Setup with uv

For development, install dependencies using [uv](https://docs.astral.sh/uv/):

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/nifcloud/nifcloud-sdk-python.git
cd nifcloud-sdk-python

# Sync dependencies
uv sync

# Install pre-commit hooks
pre-commit install
```

## Quick Start

Write your python program:

```python
from nifcloud import session

client = session.get_session().create_client(
    "computing",
    region_name="jp-east-1",
    nifcloud_access_key_id="<Your NIFCLOUD Access Key ID>",
    nifcloud_secret_access_key="<Your NIFCLOUD Secret Access Key>"
)

print(client.describe_instances())
```

Execute the program:

```bash
python test.py
```

### Environment Variables

Credentials and region name can be passed via environment variables:

```python
from nifcloud import session

client = session.get_session().create_client("computing")
print(client.describe_instances())
```

```bash
export NIFCLOUD_ACCESS_KEY_ID=<Your NIFCLOUD Access Key ID>
export NIFCLOUD_SECRET_ACCESS_KEY=<Your NIFCLOUD Secret Access Key>
export NIFCLOUD_DEFAULT_REGION=jp-east-1
python test.py
```

## Development

### Running Tests

```bash
# Run unit tests with uv
uv run pytest tests/unit

# Run with coverage report
uv run pytest tests/unit --cov=nifcloud --cov-report=term-missing

# Run acceptance tests (requires NIFCLOUD credentials)
uv run pytest tests/acceptance/minimal
```

### Code Quality

```bash
# Run linter (ruff)
uv run ruff check nifcloud/

# Format code
uv run ruff format nifcloud/

# Type checking
uv run mypy nifcloud/

# Run pre-commit hooks
pre-commit run --all-files
```

## Documentation

See [official documentation](https://nifcloud-sdk-python.readthedocs.io/en/latest/) for detailed API reference and examples.

## License

Apache License 2.0

See [LICENSE.txt](LICENSE.txt) for details.
