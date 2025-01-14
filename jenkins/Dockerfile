FROM jenkins/jenkins:lts-jdk17

USER root

# Docker 공식 GPG 키 추가 및 Docker 저장소 설정
RUN apt-get update && \
    apt-get install -y ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null


RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

ARG GROUP_GID=998
ARG USER_UID=1000

RUN groupmod -g ${GROUP_GID} docker && \
RUN usermod -u ${USER_UID} jenkins && \
    usermod -a -G docker jenkins

USER jenkins