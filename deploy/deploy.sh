#!/bin/bash

set -e

echo "=========================================="
echo "FastAPI Blog 배포 스크립트"
echo "=========================================="
echo ""

if [ "$EUID" -eq 0 ]; then
   echo "이 스크립트를 root로 실행하지 마세요"
   exit 1
fi

PROJECT_DIR="/home/ubuntu/blog"

echo "1. 시스템 패키지 업데이트..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

echo ""
echo "2. Python 가상환경 생성..."
cd $PROJECT_DIR
python3 -m venv venv

echo ""
echo "3. Python 패키지 설치..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "4. .env 파일 확인..."
if [ ! -f .env ]; then
    echo ".env 파일이 없습니다. 샘플 파일 생성..."
    cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./blogs.db
ALLOWED_ORIGINS=*
ENVIRONMENT=production
EOF
    echo ".env 파일 생성 완료. 필요시 수정하세요."
else
    echo ".env 파일이 이미 존재합니다."
fi

echo ""
echo "5. systemd 서비스 등록..."
sudo cp deploy/blog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable blog
sudo systemctl start blog

echo ""
echo "6. Nginx 설정..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/blog
sudo ln -sf /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo ""
echo "=========================================="
echo "배포 완료!"
echo "=========================================="
echo ""
echo "서비스 상태 확인:"
sudo systemctl status blog --no-pager
echo ""
echo "접속 URL: http://$(curl -s ifconfig.me)"
echo ""
echo "유용한 명령어:"
echo "  - 로그 확인: sudo journalctl -u blog -f"
echo "  - 서비스 재시작: sudo systemctl restart blog"
echo "  - Nginx 재시작: sudo systemctl restart nginx"
