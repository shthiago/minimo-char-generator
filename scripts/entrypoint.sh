#!/usr/bin/env bash
# Administrate commands entered to image
case $1 in
    run)
        echo "Running server"
        poetry run uvicorn --host 0.0.0.0 --port 5000 src.api:app
        ;;

    test)
        echo "Installing full dependencies"
        poetry install
        echo "Running tests"
        poetry run make test
        ;;

    *)
        echo "Running command"
        exec "$@"
        ;;
esac