# FastAPI 블로그 프로젝트

FastAPI와 SQLite를 사용한 간단한 블로그 애플리케이션입니다.

## 📋 프로젝트 개요

- **백엔드**: FastAPI (Python)
- **데이터베이스**: SQLite (SQLAlchemy ORM)
- **프론트엔드**: Vanilla JavaScript + HTML/CSS
- **아키텍처**: MPA (Multi-Page Application)

## ✨ 주요 기능

### 현재 구현된 기능
- ✅ 블로그 글 목록 조회 (최신순)
- ✅ 블로그 글 상세 조회
- ✅ 블로그 글 작성
- ✅ 블로그 글 수정
- ✅ 블로그 글 삭제
- ✅ SQLite 데이터베이스 저장
- ✅ RESTful API 구현
- ✅ Swagger UI 자동 문서화

### 향후 구현 예정
- ⏳ JWT 기반 사용자 인증
- ⏳ 회원가입 및 로그인
- ⏳ 작성자 권한 검증

## 📁 프로젝트 구조

```
blog/
├── .env                    # 환경변수 설정
├── .gitignore             # Git 제외 파일
├── requirements.txt       # Python 패키지 목록
├── main.py               # FastAPI 메인 애플리케이션
├── blogs.db              # SQLite 데이터베이스 (자동 생성)
├── spa.html              # SPA 버전 (테스트용)
├── venv/                 # Python 가상환경
└── static/               # 정적 파일 (프론트엔드)
    ├── blog_list.html    # 블로그 목록 페이지
    ├── blog_detail.html  # 블로그 상세 페이지
    ├── blog_create.html  # 블로그 작성 페이지
    └── blog_edit.html    # 블로그 수정 페이지
```

## 🚀 설치 및 실행

### 1. 필수 요구사항
- Python 3.11 이상
- pip (Python 패키지 관리자)

### 2. 프로젝트 클론 또는 다운로드
```bash
cd /path/to/project/blog
```

### 3. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 4. 패키지 설치
```bash
pip install -r requirements.txt
```

### 5. 서버 실행
```bash
uvicorn main:app --reload
```

서버가 시작되면 다음 메시지가 표시됩니다:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 접속 URL

### 웹 애플리케이션
- **메인 페이지**: http://localhost:8000/static/blog_list.html
- **SPA 버전**: http://localhost:8000/spa.html (테스트용)

### API 문서
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API 엔드포인트
- **루트**: http://localhost:8000/
- **Hello**: http://localhost:8000/api/hello

## 📡 API 명세

### 블로그 API

#### 1. 블로그 목록 조회
```http
GET /blogs
```
**응답 예시**:
```json
[
  {
    "id": 3,
    "title": "JavaScript",
    "content": "Fetch API is great",
    "author": "admin",
    "created_at": "2025-01-06",
    "updated_at": "2025-01-06"
  }
]
```

#### 2. 블로그 상세 조회
```http
GET /blogs/{blog_id}
```

#### 3. 블로그 작성
```http
POST /blogs
Content-Type: application/json

{
  "title": "제목",
  "content": "내용"
}
```

#### 4. 블로그 수정
```http
PUT /blogs/{blog_id}
Content-Type: application/json

{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```

#### 5. 블로그 삭제
```http
DELETE /blogs/{blog_id}
```

## 🧪 테스트 방법

### 1. Swagger UI로 테스트
1. http://localhost:8000/docs 접속
2. 각 API 엔드포인트를 직접 테스트 가능
3. "Try it out" 버튼 클릭 후 파라미터 입력

### 2. 웹 브라우저로 테스트
1. http://localhost:8000/static/blog_list.html 접속
2. UI를 통해 CRUD 기능 테스트

### 3. curl로 테스트
```bash
# 목록 조회
curl http://localhost:8000/blogs

# 상세 조회
curl http://localhost:8000/blogs/1

# 작성
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"title":"테스트","content":"테스트 내용"}'

# 수정
curl -X PUT http://localhost:8000/blogs/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"수정","content":"수정된 내용"}'

# 삭제
curl -X DELETE http://localhost:8000/blogs/1
```

## ⚙️ 환경변수 설정

`.env` 파일에서 다음 환경변수를 설정할 수 있습니다:

```bash
# JWT 시크릿 키 (인증 구현 후 사용)
SECRET_KEY=dev-secret-key-change-in-production-min-32-chars

# 데이터베이스 URL
DATABASE_URL=sqlite:///./blogs.db

# CORS 허용 출처 (쉼표로 구분)
ALLOWED_ORIGINS=*

# 환경 (development, production)
ENVIRONMENT=development
```

## 💡 사용 방법

### 블로그 글 작성하기
1. 브라우저에서 http://localhost:8000/static/blog_list.html 접속
2. "새 글 작성" 버튼 클릭
3. 제목과 내용 입력
4. "작성" 버튼 클릭

### 블로그 글 수정하기
1. 목록에서 수정할 글 클릭
2. "수정" 버튼 클릭
3. 내용 수정 후 "수정" 버튼 클릭

### 블로그 글 삭제하기
1. 목록에서 삭제할 글 클릭
2. "삭제" 버튼 클릭
3. 확인 대화상자에서 "확인" 클릭

## 🔧 문제 해결

### 포트 충돌 오류
```
ERROR: [Errno 48] Address already in use
```
**해결 방법**:
```bash
# 8000 포트 사용 중인 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

### 패키지 설치 오류
```
error: externally-managed-environment
```
**해결 방법**: 가상환경 사용
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 데이터베이스 초기화
데이터베이스를 초기화하려면 `blogs.db` 파일을 삭제하고 서버를 다시 시작하면 됩니다:
```bash
rm blogs.db
uvicorn main:app --reload
```

## 📚 기술 스택

### 백엔드
- **FastAPI** 0.115.0 - 고성능 Python 웹 프레임워크
- **Uvicorn** 0.30.0 - ASGI 서버
- **SQLAlchemy** 2.0.35 - SQL ORM
- **Pydantic** 2.9.0 - 데이터 검증
- **python-dotenv** 1.0.1 - 환경변수 관리

### 향후 추가 예정
- **python-jose** - JWT 토큰 처리
- **passlib** - 비밀번호 해싱
- **python-multipart** - 파일 업로드

### 프론트엔드
- Vanilla JavaScript (ES6+)
- HTML5 + CSS3
- Fetch API

## 📝 개발 노트

### 구현 내역
1. **1단계**: 프로젝트 초기 설정 및 CORS 설정
2. **2단계**: 메모리 기반 CRUD API 구현
3. **3단계**: SPA 프론트엔드 구현
4. **4단계**: MPA로 전환 (페이지 분리)
5. **5단계**: SQLAlchemy + SQLite 데이터베이스 연동
6. **6단계**: Static 파일 서빙 설정

### 학습 자료
- FastAPI 베이스캠프 5장: 블로그 기능 구현
- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- SQLAlchemy 문서: https://docs.sqlalchemy.org/

## 🚀 향후 계획

### Phase 1: 인증 시스템 (다음 단계)
- [ ] User 모델 추가
- [ ] JWT 토큰 발급/검증
- [ ] 회원가입/로그인 API
- [ ] 작성자별 권한 관리
- [ ] 로그인 UI 추가

### Phase 2: 배포 준비
- [ ] 환경 분리 (개발/프로덕션)
- [ ] Nginx 설정
- [ ] Systemd 서비스 파일
- [ ] 배포 자동화 스크립트

### Phase 3: AWS Lightsail 배포
- [ ] Lightsail 인스턴스 설정
- [ ] Static IP 할당
- [ ] 도메인 연결 (선택)
- [ ] HTTPS 설정 (Let's Encrypt)

## 📄 라이선스

이 프로젝트는 학습 목적으로 작성되었습니다.

## 👨‍💻 개발자

FastAPI 베이스캠프 5장 실습 프로젝트

---

**마지막 업데이트**: 2025-11-11
