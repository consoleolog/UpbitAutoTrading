#!/bin/bash

EXIST_BLUE=$(sudo docker-compose -p autotrading-blue -f docker-compose.blue.yaml ps | grep Up)

if [ -z "$EXIST_BLUE" ]; then
  echo "blue up"
  docker-compose -p autotrading-blue -f docker-compose.blue.yaml up -d --build
  BEFORE_COMPOSE_COLOR="green"
  AFTER_COMPOSE_COLOR="blue"
else
  echo "green up"
  docker-compose -p autotrading-green -f docker-compose.green.yaml up -d --build
  BEFORE_COMPOSE_COLOR="blue"
  AFTER_COMPOSE_COLOR="green"
fi

sleep 10

EXIST_AFTER=$(docker-compose -p autotrading-${AFTER_COMPOSE_COLOR} -f docker-compose.${AFTER_COMPOSE_COLOR}.yaml ps | grep Up)
if [ -n "$EXIST_AFTER" ]; then
  docker-compose -p autotrading-${BEFORE_COMPOSE_COLOR} -f docker-compose.${BEFORE_COMPOSE_COLOR}.yaml down
  echo "$BEFORE_COMPOSE_COLOR down"
fi