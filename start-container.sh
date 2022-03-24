#!/bin/sh
docker run \
  --env-file env \
  --name instapy \
  --volume /Users/dima/Development/dolboinsta/dolboinsta.py:/code/docker_quickstart.py \
  --volume /Users/dima/Development/dolboinsta:/code/dolboinsta \
  instapy/instapy:latest
