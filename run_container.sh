#!/bin/bash

IMAGE_NAME="autotrading:v1"
IMAGE_ID=$(sudo docker images -q $IMAGE_NAME)

echo ">>> Blue or Green Check"

# 현재 실행 중인 컨테이너 확인
if curl -X GET http://localhost:8000/health > /dev/null 2>&1; then
  echo -e ">>> Blue is Running...\n"
  echo ">>> Starting Green Deployment..."
  BEFORE_COLOR="BLUE"
  AFTER_COLOR="GREEN"
elif curl -X GET http://localhost:8001/health > /dev/null 2>&1; then
  echo -e ">>> Green is Running...\n"
  echo ">>> Starting Blue Deployment..."
  BEFORE_COLOR="GREEN"
  AFTER_COLOR="BLUE"
else
  echo ">>> No Container is Running..."
  echo ">>> Starting Blue Deployment..."
  AFTER_COLOR="BLUE"
fi

# TICKERS와 PORTS 배열 생성
TICKERS=($(echo $TICKERS | tr ',' ' '))
PORTS=($(echo $PORTS | tr ',' ' '))

# 배열 길이 확인
if [ "${#TICKERS[@]}" -ne "${#PORTS[@]}" ]; then
  echo ">>> TICKERS and PORTS do not match."
  exit 1
fi

# 새 컨테이너 배포
for i in "${!TICKERS[@]}"; do
  export TICKER=${TICKERS[$i]}
  export PORT=${PORTS[$i]}
  echo ">>> Deploying $TICKER on port $PORT..."
  docker-compose -p $AFTER_COLOR up -d --build --no-recreate
done

# 이전 컨테이너 종료
sudo docker rmi "$IMAGE_ID"
if [ "$BEFORE_COLOR" == "BLUE" ]; then
  echo ">>> Stopping Blue Containers..."
  docker-compose -p blue down
else
  echo ">>> Stopping Green Containers..."
  docker-compose -p green down
fi

echo ">>> Deployment Complete. Current Active: $AFTER_COLOR"
