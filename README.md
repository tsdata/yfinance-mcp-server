# 주식 데이터 MCP 서버

Model Context Protocol(MCP)을 활용하여 주식 시장 데이터를 조회할 수 있는 서버입니다. 이 서버는 Claude Desktop과 같은 MCP 호환 클라이언트에 실시간 주식 정보와 날짜/시간 정보를 제공합니다.

## 주요 기능

### 1. 주식 가격 데이터 조회

- 특정 기간의 주식 가격 데이터 조회
- 시작 날짜와 종료 날짜를 유연하게 지정 가능
- 날짜를 지정하지 않을 경우 현재 날짜 기준으로 조회

### 2. 주식 정보 조회

- 회사명, 섹터, 산업 등 기본 정보 제공
- 시가총액, 주가 정보 등 재무 관련 정보 제공
- 회사 개요 및 설명 제공

### 3. 현재 날짜/시간 정보

- 다양한 시간대에 맞는 현재 날짜 및 시간 정보 제공
- 다양한 형식으로 날짜/시간 데이터 제공(ISO, 한국어, Unix 타임스탬프 등)

## 설치 방법

### 필수 요구사항

- Python 3.10 이상
- [uv](https://docs.astral.sh/uv/) 또는 pip

### 운영체제별 설치 및 사용 방법

#### Mac/Linux

1. 터미널을 열고 의존성을 설치합니다:
   ```bash
   # uv 사용 (권장)
   uv add "mcp[cli]" yfinance pytz
   
   # 또는 pip 사용
   pip install "mcp[cli]" yfinance pytz
   ```

2. 서버 실행:
   ```bash
   python3 stock_server.py
   # 또는
   mcp run stock_server.py
   ```

3. Claude Desktop에 설치:
   ```bash
   mcp install stock_server.py --name "주식 데이터 서버"
   ```

#### Windows

1. 명령 프롬프트(CMD) 또는 PowerShell을 관리자 권한으로 실행합니다.

2. 의존성 설치:
   ```powershell
   # uv 사용 (권장)
   uv add "mcp[cli]" yfinance pytz
   
   # 또는 pip 사용
   pip install "mcp[cli]" yfinance pytz
   ```

3. 서버 실행:
   ```powershell
   python stock_server.py
   # 또는
   mcp run stock_server.py
   ```

4. Claude Desktop에 설치:
   ```powershell
   mcp install stock_server.py --name "주식 데이터 서버"
   ```

## 개발 및 테스트

개발 과정에서 서버를 테스트하려면:

```bash
mcp dev stock_server.py
```

## Claude Desktop 사용 예시

Claude Desktop에서 다음과 같은 질문을 통해 서버를 사용할 수 있습니다:

1. **주식 가격 조회**:
   ```
   애플(AAPL)의 최근 주가 정보를 알려줘.
   ```
   또는
   ```
   테슬라(TSLA)의 2025년 1월 6일부터 2025년 1월 9일까지의 주가를 보여줘.
   ```

2. **주식 정보 조회**:
   ```
   마이크로소프트(MSFT)에 대한 기본 정보를 알려줘.
   ```

3. **현재 날짜/시간 정보**:
   ```
   오늘의 날짜를 알려줘.
   ```
   또는
   ```
   뉴욕의 현재 시간이 어떻게 되니?
   ```

## 도구 상세 설명

### 주식 가격 조회 도구 (`get_stock_price_history`)

| 파라미터 | 타입 | 설명 | 필수 여부 | 기본값 |
|---------|------|------|----------|--------|
| symbol | str | 주식 심볼 (예: AAPL, MSFT) | 필수 | - |
| start | str | 조회 시작 날짜 (YYYY-MM-DD 형식) | 선택 | 현재 날짜 |
| end | str | 조회 종료 날짜 (YYYY-MM-DD 형식) | 선택 | 시작일+5일 |

### 주식 정보 조회 도구 (`get_stock_info`)

| 파라미터 | 타입 | 설명 | 필수 여부 | 기본값 |
|---------|------|------|----------|--------|
| symbol | str | 주식 심볼 (예: AAPL, MSFT) | 필수 | - |

### 현재 날짜/시간 조회 도구 (`get_current_date`)

| 파라미터 | 타입 | 설명 | 필수 여부 | 기본값 |
|---------|------|------|----------|--------|
| timezone | str | 시간대 (예: Asia/Seoul, America/New_York) | 선택 | Asia/Seoul |

## 리소스 상세 설명

### 주식 개요 리소스 (`stock://{symbol}/overview`)

주식에 대한 개요 정보를 마크다운 형식으로 제공합니다.

## 주의사항

- yfinance 라이브러리는 비공식 API를 사용하므로, Yahoo Finance의 서비스 약관 변경에 따라 작동이 중단될 수 있습니다.
- 무료 API이므로 요청 빈도가 높을 경우 제한될 수 있습니다.
- 실시간 데이터보다는 약간의 지연이 있을 수 있습니다.

## 라이선스

MIT 라이선스