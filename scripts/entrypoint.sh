#!/usr/bin/env bash
# Administrate commands entered to image
case $1 in
    run)
        echo "Running server"
        make run
        ;;

    test)
        echo "Running tests"
        make test
        ;;

    *)
        echo "Running command"
        exec "$@"
        ;;
esac