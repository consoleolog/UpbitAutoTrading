#!/bin/bash

sudo git -v || {
  echo -e "=== START GIT SETUP ===\n"

  echo ">>> Update All package"
  sudo yum update -y || {
    echo ">>> Fail to yum update"
    exit 1
  }

  echo ">>> Install Git"
  sudo yum install git -y || {
    echo ">>> Fail to install Git"
    exit 1
  }

  sudo git -v || {
    echo ">>> Can't Find Git"
    exit 1
  }
  sudo usermod -a -G docker ec2-user
  echo ">>> Success to Install Git"

  echo -e "\n=== SUCCESS Git SETUP ==="
}

echo ">>> Git Is Already Installed"