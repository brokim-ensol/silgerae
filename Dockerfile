# 베이스 이미지
FROM python:3.10-slim

#작업 폴더 설정
WORKDIR /opt/myproject

RUN apt update

RUN apt upgrade

#chrome driver에 필요한 라이브러리 설치
RUN apt install -y libglib2.0-0 libnss3 libx11-xcb1 libxcb1 libnspr4 libnss3

#chrome 설치
RUN apt install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# ./google-chrome-stable_current_amd64.deb 삭제
RUN rm google-chrome-stable_current_amd64.deb

# 소스코드 복사
COPY . /opt/myproject

# 파이썬 패키지 설정
RUN pip3 install -r requirements.txt

# 실행 파일 설정
CMD ["python3","app.py"]