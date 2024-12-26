#!/bin/bash

EXIST_BLUE=$(sudo docker-compose -p "${DOCKER_APP_NAME}"-blue -f docker-compose.blue.yaml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
  echo "blue up"
  docker-compose -p "${DOCKER_APP_NAME}"-blue -f docker-compose.blue.yaml up -d
  BEFORE_COMPOSE_COLOR="green"
  AFTER_COMPOSE_COLOR="blue"
else
  echo "green up"
  docker-compose -p "${DOCKER_APP_NAME}"-green -f docker-compose.green.yaml up -d
  BEFORE_COMPOSE_COLOR="blue"
  AFTER_COMPOSE_COLOR="green"
fi

sleep 10

EXIST_AFTER=$(docker-compose -p "${DOCKER_APP_NAME}"-${AFTER_COMPOSE_COLOR} -f docker-compose.${AFTER_COMPOSE_COLOR}.yaml ps | grep Up)
if [ -n "$EXIST_AFTER" ]; then
  docker-compose -p "${DOCKER_APP_NAME}"-${BEFORE_COMPOSE_COLOR} -f docker-compose.${BEFORE_COMPOSE_COLOR}.yaml down
  echo "$BEFORE_COMPOSE_COLOR down"
fi

