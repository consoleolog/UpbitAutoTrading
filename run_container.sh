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
  BEFORE_COLOR=""
fi

TICKERS=("KRW-BTC" "KRW-ETH" "KRW-BCH" "KRW-AAVE" "KRW-SOL" "KRW-BSV" "KRW-XRP")
BLUE_PORTS=("8000" "8100" "8200" "8300" "8400" "8500" "8600")
GREEN_PORTS=("8001" "8101" "8201" "8301" "8401" "8501" "8601")

echo "TICKERS: ${TICKERS[@]}"
echo "BLUE_PORTS: ${BLUE_PORTS[@]}"
echo "GREEN_PORTS: ${GREEN_PORTS[@]}"

if [ "${#TICKERS[@]}" -ne "${#BLUE_PORTS[@]}" ] || [ "${#TICKERS[@]}" -ne "${#GREEN_PORTS[@]}" ]; then
  echo ">>> TICKERS, BLUE_PORTS, and GREEN_PORTS do not match."
  exit 1
fi

# 새 컨테이너 배포
for i in "${!TICKERS[@]}"; do
  TICKER=${TICKERS[$i]}

  LOWER_TICKER=$(echo "$TICKER" | tr '[:upper:]' '[:lower:]')

  if [ "$AFTER_COLOR" == "blue" ]; then
    PORT=${BLUE_PORTS[$i]}
    SERVER_PORT=${BLUE_PORTS[$i]}
  elif [ "$AFTER_COLOR" == "green" ]; then
    PORT=${GREEN_PORTS[$i]}
    SERVER_PORT=${BLUE_PORTS[$i]}
  fi

  echo ">>> Deploying $TICKER on port $SERVER_PORT..."

  sudo PORT="$PORT" SERVER_PORT="$SERVER_PORT" TICKER="$TICKER" docker-compose -p "$LOWER_TICKER-$AFTER_COLOR" -f docker-compose.yaml up -d --build
done

if [ -z "$BEFORE_COLOR" ]; then
    exit 0
fi
for i in "${!TICKERS[@]}"; do
  TICKER=${TICKERS[$i]}
  LOWER_TICKER=$(echo "$TICKER" | tr '[:upper:]' '[:lower:]')
    # 색상에 따른 포트 할당
  if [ "$AFTER_COLOR" == "blue" ]; then
    PORT=${BLUE_PORTS[$i]}
    SERVER_PORT=${BLUE_PORTS[$i]}
  elif [ "$AFTER_COLOR" == "green" ]; then
    PORT=${GREEN_PORTS[$i]}
    SERVER_PORT=${BLUE_PORTS[$i]}
  fi
  echo ">>> Stopping $TICKER on port $PORT..."
  sudo docker-compose -p "$LOWER_TICKER-$BEFORE_COLOR" down
done
sudo docker rmi "$IMAGE_ID"

echo ">>> Deployment Complete. Current Active: $AFTER_COLOR"
exit 0
