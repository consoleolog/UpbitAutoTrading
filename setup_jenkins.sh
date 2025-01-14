#!/bin/bash

IMAGE_NAME="my_jenkins:v1"
CONTAINER_NAME="jenkins_container"
EXIST_JENKINS_CONTAINER=$(sudo docker ps -aqf "name=$CONTAINER_NAME")

echo -e "=== BUILD JENKINS IMAGE ===\n"

sudo docker -v || {
  echo ">>> DOCKER IS NOT INSTALLED!!"
  exit 1
}

GROUP_GID=$(getent group docker | cut -d: -f3)
USER_UID=$(id -u $USER)

sudo docker build -t "$IMAGE_NAME" --build-arg USER_UID="$USER_UID" --build-arg GROUP_GID="$GROUP_GID" ./jenkins/ || {
  echo ">>> FAIL TO BUILD IMAGE : $IMAGE_NAME"
  exit 1
}
echo -e "=== COMPLETE TO BUILD IMAGE : $IMAGE_NAME ===\n"

if [ ! -z "$EXIST_JENKINS_CONTAINER" ]; then
  echo -e "=== STOP CONTAINER : $CONTAINER_NAME ===\n"

  echo docker stop "$EXIST_JENKINS_CONTAINER" || {
    echo "=== FAIL TO STOP CONTAINER : $CONTAINER_NAME ==="
    exit 1
  }

  echo "=== COMPLETE STOP CONTAINER : $CONTAINER_NAME ==="
fi

echo "=== START JENKINS CONTAINER ==="
sudo chown -R 1000:1000 /var/jenkins_home
sudo docker run -d \
  -p 8081:8080 -p 50000:50000 \
  -v /var/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name "$CONTAINER_NAME" "$IMAGE_NAME" || {
      echo ">>> FAIL TO START CONTAINER : $CONTAINER_NAME"
      exit 1
  }
echo "=== COMPLETE TO START CONTAINER : $CONTAINER_NAME ==="
