#!/bin/bash
IMAGE_NAME="sk015-timetable"
VERSION="1.0.0"
CPU_PLATFORM="arm64"
#IS_CACHE="--no-cache"

# Docker 이미지 빌드
docker build \
  --tag ${IMAGE_NAME}:${VERSION} \
  --file Dockerfile \
  ${IS_CACHE} .
