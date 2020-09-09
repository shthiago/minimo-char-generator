#! /usr/bin/bash

# Style tags
BOLD_RED='\033[1;31m'
NC='\033[0m'
BOLD_GREEN='\033[1;32m'

docker-compose -f docker-compose-test.yml up --build --force-recreate --exit-code-from web
ret=$?

if [ $ret == 0 ]; then
    echo -e "${BOLD_GREEN}----------Tests passed!----------";
else
    echo -e "${BOLD_RED}----------Tests failed!----------";
fi

exit $?
