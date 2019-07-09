#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A nagoya_rest.taskapp beat -l INFO
