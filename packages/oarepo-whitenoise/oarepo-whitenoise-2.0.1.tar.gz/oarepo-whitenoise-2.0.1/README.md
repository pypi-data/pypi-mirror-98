# OArepo whitenoise

This library serves static resources and index.html at runtime
using the whitenoise package. This greatly simplifies the deployment
as only one image needs to be deployed.

## Installation

```bash
pip install oarepo-micro-api oarepo-whitenoise
```

## Configuration

This library expects the static files in ``/whitenoise``
folder. If they are located elsewhere, set environment
variable ``WHITENOISE_ROOT`` to the correct location.

## Usage

In your wsgi configuration, specify:

```ini
[uwsgi]
module = oarepo_whitenoise.wsgi:application
...
```

as your wsgi entry point.
