# AWS Lightsail 배포 가이드

FastAPI 블로그 애플리케이션을 AWS Lightsail에 배포하는 방법입니다.

## 📋 사전 준비

- AWS 계정
- 로컬에 프로젝트 파일
- SSH 클라이언트 (Terminal, PuTTY 등)

---

## 1단계: Lightsail 인스턴스 생성

### 1.1 AWS Console 접속

1. [AWS Lightsail Console](https://lightsail.aws.amazon.com/)에 로그인
2. "인스턴스 생성" 클릭

### 1.2 인스턴스 설정

**인스턴스 위치:**
- 서울 (ap-northeast-2) 또는 가까운 리전 선택

**플랫폼 선택:**
- OS 전용 → Linux/Unix
- 블루프린트 → Ubuntu 22.04 LTS

**인스턴스 플랜:**
- $3.5/월 (512MB RAM, 1 vCPU) - 테스트용
- $5/월 (1GB RAM, 1 vCPU) - 권장

**인스턴스 이름:**
- `blog-server` (원하는 이름)

**인스턴스 생성** 클릭

### 1.3 SSH 키 다운로드

- 인스턴스 생성 시 SSH 키 페어 다운로드
- 파일명: `LightsailDefaultKey-ap-northeast-2.pem` (리전에 따라 다름)
- 안전한 위치에 저장

---

## 2단계: 네트워크 설정

### 2.1 고정 IP 할당

1. Lightsail 콘솔에서 "네트워킹" 탭 클릭
2. "고정 IP 생성" 클릭
3. 생성된 인스턴스에 연결
4. 고정 IP 주소 기록 (예: 54.123.45.67)

### 2.2 방화벽 규칙 설정

인스턴스 상세 페이지 → "네트워킹" 탭:

| 애플리케이션 | 프로토콜 | 포트 범위 |
|------------|---------|----------|
| SSH        | TCP     | 22       |
| HTTP       | TCP     | 80       |
| HTTPS      | TCP     | 443      |
| Custom     | TCP     | 8000     |

---

## 3단계: SSH 접속

### 3.1 SSH 키 권한 설정 (Mac/Linux)

```bash
chmod 400 ~/Downloads/LightsailDefaultKey-ap-northeast-2.pem
```

### 3.2 SSH 접속

```bash
ssh -i ~/Downloads/LightsailDefaultKey-ap-northeast-2.pem ubuntu@54.123.45.67
```

(54.123.45.67을 실제 고정 IP로 변경)

### 3.3 Windows 사용자

PuTTY 사용:
1. PuTTYgen으로 .pem 파일을 .ppk로 변환
2. PuTTY 설정에서 .ppk 파일 지정
3. Host Name: ubuntu@54.123.45.67

---

## 4단계: 프로젝트 파일 업로드

### 방법 1: Git Clone (권장)

**서버에서 실행:**
```bash
cd ~
git clone https://github.com/your-username/blog.git
cd blog
```

### 방법 2: SCP로 파일 전송

**로컬에서 실행:**
```bash
cd /path/to/your/blog/project
scp -i ~/Downloads/LightsailDefaultKey-ap-northeast-2.pem -r . ubuntu@54.123.45.67:~/blog
```

### 방법 3: rsync 사용

**로컬에서 실행:**
```bash
rsync -avz -e "ssh -i ~/Downloads/LightsailDefaultKey-ap-northeast-2.pem" \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '*.db' \
  . ubuntu@54.123.45.67:~/blog
```

---

## 5단계: 배포 실행

### 5.1 배포 스크립트 실행 권한 부여

```bash
cd ~/blog
chmod +x deploy/deploy.sh
chmod +x deploy/restart.sh
```

### 5.2 배포 실행

```bash
./deploy/deploy.sh
```

이 스크립트는 다음 작업을 자동으로 수행합니다:
- 시스템 패키지 업데이트
- Python 가상환경 생성
- Python 패키지 설치
- .env 파일 생성 (없을 경우)
- systemd 서비스 등록
- Nginx 설정

### 5.3 배포 완료 확인

스크립트가 완료되면 다음과 같이 표시됩니다:
```
========================================
배포 완료!
========================================

서비스 상태 확인:
● blog.service - FastAPI Blog Application
   Active: active (running)

접속 URL: http://54.123.45.67
```

---

## 6단계: 접속 확인

### 6.1 브라우저에서 접속

```
http://54.123.45.67/static/index.html
http://54.123.45.67/static/blog_list.html
http://54.123.45.67/static/login.html
```

### 6.2 API 테스트

```bash
curl http://54.123.45.67/api/hello
```

---

## 7단계: 환경 설정 (중요!)

### 7.1 .env 파일 수정

```bash
cd ~/blog
nano .env
```

**필수 수정 항목:**
```env
SECRET_KEY=실제로_생성된_안전한_키_그대로_사용
DATABASE_URL=sqlite:///./blogs.db
ALLOWED_ORIGINS=http://54.123.45.67,http://yourdomain.com
ENVIRONMENT=production
```

### 7.2 서비스 재시작

```bash
sudo systemctl restart blog
```

---

## 업데이트 방법

### 코드 변경 후 업데이트

**방법 1: Git 사용**
```bash
cd ~/blog
./deploy/restart.sh
```

**방법 2: 파일 직접 업로드**
```bash
# 로컬에서
scp -i ~/Downloads/LightsailDefaultKey-ap-northeast-2.pem \
  main.py ubuntu@54.123.45.67:~/blog/

# 서버에서
cd ~/blog
./deploy/restart.sh
```

---

## 유용한 명령어

### 로그 확인
```bash
# 실시간 로그
sudo journalctl -u blog -f

# 최근 100줄
sudo journalctl -u blog -n 100
```

### 서비스 제어
```bash
# 상태 확인
sudo systemctl status blog

# 재시작
sudo systemctl restart blog

# 중지
sudo systemctl stop blog

# 시작
sudo systemctl start blog
```

### Nginx 제어
```bash
# 설정 테스트
sudo nginx -t

# 재시작
sudo systemctl restart nginx

# 로그 확인
sudo tail -f /var/log/nginx/error.log
```

### 데이터베이스 관리
```bash
# 데이터베이스 백업
cd ~/blog
cp blogs.db blogs.db.backup.$(date +%Y%m%d_%H%M%S)

# 데이터베이스 초기화 (주의!)
rm blogs.db
sudo systemctl restart blog
```

---

## 문제 해결

### 서비스가 시작되지 않을 때
```bash
# 로그 확인
sudo journalctl -u blog -n 50

# 수동 실행 테스트
cd ~/blog
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 502 Bad Gateway 오류
```bash
# blog 서비스 상태 확인
sudo systemctl status blog

# 재시작
sudo systemctl restart blog
sudo systemctl restart nginx
```

### 권한 오류
```bash
# 파일 소유권 확인
ls -la ~/blog

# 소유권 수정
sudo chown -R ubuntu:ubuntu ~/blog
```

---

## 보안 강화 (선택)

### SSL/TLS 설정 (HTTPS)

```bash
# Certbot 설치
sudo apt-get install certbot python3-certbot-nginx

# 도메인이 있는 경우
sudo certbot --nginx -d yourdomain.com
```

### 방화벽 설정 (UFW)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 비용 예상

| 플랜 | RAM | CPU | 스토리지 | 전송량 | 월 비용 |
|------|-----|-----|----------|--------|---------|
| 최소 | 512MB | 1 | 20GB SSD | 1TB | $3.5 |
| 권장 | 1GB | 1 | 40GB SSD | 2TB | $5 |
| 프로덕션 | 2GB | 1 | 60GB SSD | 3TB | $10 |

---

## 추가 리소스

- [AWS Lightsail 문서](https://lightsail.aws.amazon.com/ls/docs/)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Nginx 설정 가이드](https://nginx.org/en/docs/)

---

## 지원

문제가 발생하면 다음을 확인하세요:
1. 로그 파일 (`sudo journalctl -u blog -f`)
2. Nginx 로그 (`/var/log/nginx/error.log`)
3. 방화벽 설정 (Lightsail 콘솔)
4. .env 파일 설정
