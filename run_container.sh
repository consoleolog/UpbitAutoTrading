#!/bin/bash

IMAGE_NAME="autotrading:v1"
IMAGE_ID=$(sudo docker images -q $IMAGE_NAME)

echo ">>> Blue or Green Check"

# 현재 실행 중인 컨테이너 확인
if curl -X GET http://localhost:8000/health > /dev/null 2>&1; then
  echo -e ">>> Blue is Running...\n"
  echo ">>> Starting Green Deployment..."
  BEFORE_COLOR="blue"
  AFTER_COLOR="green"
elif curl -X GET http://localhost:8001/health > /dev/null 2>&1; then
  echo -e ">>> Green is Running...\n"
  echo ">>> Starting Blue Deployment..."
  BEFORE_COLOR="green"
  AFTER_COLOR="blue"
else
  echo ">>> No Container is Running..."
  echo ">>> Starting Blue Deployment..."
  AFTER_COLOR="blue"
fi

TICKERS=("KRW-BTC" "KRW-ETH" "KRW-BCH" "KRW-AAVE" "KRW-SOL" "KRW-BSV" "KRW-XRP")
BLUE_PORTS=("8000" "8100" "8200" "8300" "8400" "8500" "8600")
GREEN_PORTS=("8001" "8101" "8201" "8301" "8401" "8501" "8601")

echo "TICKERS: ${TICKERS[@]}"
echo "BLUE_PORTS: ${BLUE_PORTS[@]}"
echo "GREEN_PORTS: ${GREEN_PORTS[@]}"

# 배열 길이 확인
if [ "${#TICKERS[@]}" -ne "${#BLUE_PORTS[@]}" ] || [ "${#TICKERS[@]}" -ne "${#GREEN_PORTS[@]}" ]; then
  echo ">>> TICKERS, BLUE_PORTS, and GREEN_PORTS do not match."
  exit 1
fi

echo "suc"

# 새 컨테이너 배포
for i in "${!TICKERS[@]}"; do
  export TICKER=${TICKERS[$i]}

  # 색상에 따른 포트 할당
  if [ "$AFTER_COLOR" == "blue" ]; then
    export PORT=${BLUE_PORTS[$i]}
    export SERVER_PORT=${BLUE_PORTS[$i]}
  elif [ "$AFTER_COLOR" == "green" ]; then
    export PORT=${GREEN_PORTS[$i]}
    export SERVER_PORT=${BLUE_PORTS[$i]}
  fi

  echo ">>> Deploying $TICKER on port $PORT..."
  sudo docker-compose -p $AFTER_COLOR -f docker-compose.yaml up -d --build
done

# 이전 컨테이너 종료
sudo docker rmi "$IMAGE_ID"
if [ "$BEFORE_COLOR" == "blue" ]; then
  echo ">>> Stopping Blue Containers..."
  sudo docker-compose -p blue down
elif [ "$BEFORE_COLOR" == "green" ]; then
  echo ">>> Stopping Green Containers..."
  sudo docker-compose -p green down
fi

echo ">>> Deployment Complete. Current Active: $AFTER_COLOR"
