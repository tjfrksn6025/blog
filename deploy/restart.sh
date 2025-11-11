#!/bin/bash

set -e

echo "=========================================="
echo "FastAPI Blog 재시작 스크립트"
echo "=========================================="
echo ""

PROJECT_DIR="/home/ubuntu/blog"

cd $PROJECT_DIR

echo "1. 최신 코드 가져오기 (git pull)..."
git pull origin main || echo "Git pull 실패 (수동 업로드인 경우 무시)"

echo ""
echo "2. Python 패키지 업데이트..."
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "3. 서비스 재시작..."
sudo systemctl restart blog

echo ""
echo "4. 서비스 상태 확인..."
sleep 2
sudo systemctl status blog --no-pager

echo ""
echo "=========================================="
echo "재시작 완료!"
echo "=========================================="
echo ""
echo "로그 확인: sudo journalctl -u blog -f"
