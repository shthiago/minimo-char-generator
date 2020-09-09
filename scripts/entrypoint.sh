#!/usr/bin/env bash
# Administrate commands entered to image
case $1 in
    run)
        echo "Running server"
        poetry run make run
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