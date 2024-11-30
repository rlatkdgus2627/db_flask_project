# Database design-Project-Vaccine Management System 

Flask를 이용한 백신 접종 관리 시스템


## 🖥️ 프로젝트 소개

동국대학교 2024학년 2학기 데이터베이스설계 기말고사 대체 프로젝트로, 사용자가 백신 접종 이력 및 정보를 조회하고 어떤 백신을 맞아야 하는지 간편하게 확인할 수 있는 시스템
<br>

## 🕰️ 개발 기간

* 24.11.18 - 24.11.30일

### 🧑‍🤝‍🧑 맴버구성

 - 팀장  : 김상현([**rlatkdgus2627**](https://github.com/rlatkdgus2627)) - 요구사항 명세서 및 데이터베이스 설계, 사이트 전체 구조 및 Model, Control 설계
 - 팀원1 : 노성환([**nanamamagaga**](https://github.com/nanamamagaga)) - E-R 다이어그램 작성, View 설계

### ⚙️ 개발 환경

- `python 3.11.9`
- **IDE** : Pycharm
- **Framework** : Flask(3.1.0)
- **Database** : SQLite

## 💾 필수 설치 패키지 및 설정

```
pip install python-dotenv
```

설치 후 .env 생성 후

```
FLASK_SECRET_KEY='원하는 키 값 작성'
```

## 💿DB 릴레이션

**환자[patient]** = (ID(PK), 환자 회원 아이디, 환자 회원 비밀번호, 전화번호, 환자 이름, 주민등록번호, 성별, 나이)

**의사[doctor]** = (ID(PK), 의사 면허 번호, 의사 회원 비밀번호, 의사 회원 전화번호)

**제약회사[pharmaceutical_company]** = (ID(PK), 사업자 등록 번호, 제약회사 명, 제약회사 회원 비밀번호)

**관리자[administrator]** = (ID(PK), 관리자 계정 아이디, 관리자 계정 비밀번호)

**백신[vaccine]** = (ID(PK), 제약회사 ID(FK), 백신 이름, 백신 종류 ID(FK), 특이 사항) (백신 제조사의 ID와 백신 종류 릴레이션의 ID 참조)

**백신 종류[vaccine_type]** = (ID(PK), 병명, 필수 접종 여부, 성별, 최소 나이, 접종 주기)

**접종[vaccination]** = (ID(PK), 백신 ID(FK), 환자 ID(FK), 접종 날짜) (백신 릴레이션의 ID와 환자 릴레이션의 ID 참조)

## 📌 주요 기능

#### 로그인 

- DB값 검증
- 로그인 시 세션(Session) 생성 후 dashboard로 리다이랙트

#### 회원가입

- ID 중복 체크 및 사용자별 중복되면 안되는 데이터 중복 확인(주민등록번호, 면허 번호 등)
- DB에 계정 정보 등록

#### Dashboard

- 각 사용자(환자, 의사, 제약회사, 관리자)별 기능 선택 화면

#### 환자

###### 접종 대상 백신 조회

* 백신 종류와 백신 접종 이력, 백신 테이블을 조인하여 접종해야 할 백신의 가장 최근 접종일을 계산함
* 접종 이력이 없거나 주기를 지나면 접종 대상 표시

###### 백신 정보 조회

* 백신 종류를 선택하여 백신 정보를 검색

#### 의사

###### 백신 접종 등록

* 백신 종류를 선택하고 백신 종류에 대한 백신을 선택
* 환자의 정보와 접종 날짜를 입력하여 DB에 정보 등록

##### 백신 접종 상태 조회

* ###### 환자의 이름과 주민등록번호를 입력

* 환자의 백신 접종 이력을 조회

#### 제약회사 

- 백신 종류를 선택하고 백신 종류에 대한 백신 정보를 입력하여 DB에 등록

#### 관리자

* 백신 종류 정보를 입력 후(증상 이름, 접종 대상 성별, 최소 나이, 주기) DB에 등록