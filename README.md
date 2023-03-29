# Pydantic TypeScript Sync

[![CI](https://github.com/captaincoordinates/pydantic-typescript-sync/actions/workflows/validation.yml/badge.svg?branch=main)](https://github.com/captaincoordinates/pydantic-typescript-sync/actions/workflows/validation.yml)

Creates a [container image](https://hub.docker.com/repository/docker/captaincoordinates/pydantic-typescript-sync/general) for Pydantic-to-TypeScript code generation driven by changes to Pydantic models. Builds upon [pydantic-to-typescript](https://pypi.org/project/pydantic-to-typescript/).

## Purpose

The purpose of this project is to allow a Python API using Pydantic and a TypeScript API client to share the same type definitions. For example, FastAPI uses Pydantic to describe API request and response types as described [here](https://fastapi.tiangolo.com/features/#pydantic-features). If a TypeScript API client (e.g. an Angular web application) shares the same type definitions as the API the API client build will break any time its expectations around API request or response models are invalidated, helping to reduce errors discovered during integration testing or at runtime.

## Usage

Example usage is shown [here](https://github.com/captaincoordinates/fastapi-websocket-sync/blob/687e2c153b1cadb1a04d7a4f7d4772fe869d6c3d/docker-compose.yml) (project is work-in-progress). The pydantic-typescript-sync container image is included in docker-compose.yml with source directories mounted to `/input` and `/output`. As Pydantic models are added or modified the `tsgenerator` container recognises those changes and creates or updates generated TypeScript types. Assuming `make serve` is running the Angular build system will rebuild the application in response to changes in any generated TypeScript types that are referenced by the application, identifying any errors in how the application references the TypeScript types. Example generated TypeScript file [here](https://github.com/captaincoordinates/fastapi-websocket-sync/blob/2985ed82bd170240e2c13ae695205ce3866f9560/web/wss/src/app/types/api_push_report.ts).

`/input` should bind to the top-level Python source directory containing Pydantic models. Pydantic models will be automatically discovered within this directory. `/output` should bind to a location within a TypeScript source directory.

### Dependencies

Pydantic models might reference types outside the Python Standard Library, and these dependencies must be installed within the pydantic-typescript-sync container to support TypeScript generation for those Pydantic models. Log messages such as the following indicate that a Pydantic model could not be imported
>WARNING:/tsgen/generation/generate.py:unable to import type class from module 'app.models.push_report', so skipping. Some dependencies may be missing: No module named 'starlette'

In this example the `starlette` dependency is preventing the model from being imported and must be installed.

This utility will search `/input` for any `requirements.txt` files and install those dependencies during startup. This may not be an ideal approach, and other methods of identifying Python dependencies are not yet supported. This approach will be reviewed as time permits (suggestions and PRs welcome).
