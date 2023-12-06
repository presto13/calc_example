# calc_example

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m calc_example
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml`
to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and
enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml`
with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "CALC_EXAMPLE_" prefix.

For example if you see in your "calc_example/settings.py" a variable named like
`random_parameter`, you should provide the "CALC_EXAMPLE_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by
overriding `env_prefix` property
in `calc_example.settings.Settings.Config`.

An example of .env file:

```bash
CALC_EXAMPLE_RELOAD="True"
CALC_EXAMPLE_PORT="8000"
CALC_EXAMPLE_ENVIRONMENT="dev"
```

You can read more about BaseSettings class
here: https://pydantic-docs.helpmanual.io/usage/settings/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

2. Run the pytest.

```bash
pytest -vv .
```
