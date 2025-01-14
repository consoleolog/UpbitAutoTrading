#!/bin/bash

sudo docker -v || {
  echo -e "=== START DOCKER SETUP ===\n"

  echo ">>> Update All package"
  sudo yum update -y || {
    echo ">>> Fail to yum update"
    exit 1
  }

  echo ">>> Install Docker"
  sudo yum install docker -y || {
    echo ">>> Fail to install Docker"
    exit 1
  }

  sudo docker -v || {
    echo ">>> Can't Find Docker"
    exit 1
  }
  sudo usermod -a -G docker ec2-user
  echo ">>> Success to Install Docker"

  sudo service docker start || {
    echo ">>> Fail to Start Docker Service"
    exit 1
  }
  echo ">>> Success to Started Docker"


  echo ">>> Install Docker Compose"
  sudo sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose || {
    echo ">>> Fail to Install Docker Compose"
    exit 1
  }
  sudo chmod +x /usr/local/bin/docker-compose
  echo ">>> Success to Install Docker Compose"

  sudo docker-compose version || {
    echo ">>> Can't Find Docker Compose"
    exit 1
  }

  echo -e "\n=== SUCCESS DOCKER SETUP ==="
}

echo ">>> Docker Is Already Installed"