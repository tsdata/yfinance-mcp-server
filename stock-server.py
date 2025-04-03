"""
YFinance MCP 서버

MCP를 사용하여 Yahoo Finance에서 주식 가격 정보를 가져오는 도구를 제공합니다.
"""

from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional

import yfinance as yf
from pydantic import Field

from mcp.server.fastmcp import FastMCP

# MCP 서버 생성
mcp = FastMCP(
    "YFinance MCP Server",
    dependencies=["yfinance", "pytz"],  # 필요한 의존성 지정
)


def is_valid_date(date_str: str) -> bool:
    """날짜 문자열이 YYYY-MM-DD 형식인지 확인합니다."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@mcp.tool()
def get_stock_price_history(
    symbol: str = Field(description="주식 심볼 (예: AAPL, MSFT)"),
    start: str = Field(
        default="", description="조회 시작 날짜 (YYYY-MM-DD 형식, 생략 시 오늘 날짜 사용)"
    ),
    end: str = Field(
        default="", description="조회 종료 날짜 (YYYY-MM-DD 형식, 생략 시 시작일로부터 5일간 조회)"
    ),
) -> List[Dict]:
    """YFinance를 사용하여 특정 기간의 주식 가격 정보를 조회합니다."""
    
    # start가 빈 문자열이면 오늘 날짜를 사용
    if not start:
        # 서울 시간대 기준 현재 날짜
        try:
            tz = pytz.timezone("Asia/Seoul")
            now = datetime.now(tz)
            start = now.strftime("%Y-%m-%d")
        except:
            # pytz 오류 시 대안
            start = datetime.now().strftime("%Y-%m-%d")
    
    # 날짜 유효성 검증
    if not is_valid_date(start):
        raise ValueError(f"잘못된 시작 날짜 형식입니다: {start}. YYYY-MM-DD 형식이어야 합니다.")

    if end and not is_valid_date(end):
        raise ValueError(f"잘못된 종료 날짜 형식입니다: {end}. YYYY-MM-DD 형식이어야 합니다.")

    try:
        stock = yf.Ticker(symbol)
        
        # 문자열로 된 날짜를 datetime 객체로 변환
        start_date = datetime.strptime(start, "%Y-%m-%d")
        
        # 특정 기간의 주식 가격 정보 조회
        if end:
            end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
            price = stock.history(start=start_date, end=end_date)
        # end 날짜가 없으면 5일간의 주식 가격 정보 조회
        else:
            end_date = start_date + timedelta(days=5)
            price = stock.history(start=start_date, end=end_date)

        # 결과가 비어있는지 확인
        if price.empty:
            return [{"message": f"'{symbol}' 심볼에 대한 주식 데이터가 없거나 해당 기간에 데이터가 없습니다."}]

        # 데이터프레임을 딕셔너리로 변환하여 반환
        df = price.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # 숫자 값 반올림
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = df[col].round(2)
            
        return df.to_dict(orient='records')

    except Exception as e:
        raise ValueError(f"주식 데이터 조회 중 오류가 발생했습니다: {str(e)}")


@mcp.tool()
def get_stock_info(
    symbol: str = Field(description="주식 심볼 (예: AAPL, MSFT)")
) -> Dict:
    """주식에 대한 기본 정보를 조회합니다."""
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # 필요한 정보만 추출
        result = {
            "symbol": symbol,
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "marketCap": info.get("marketCap", "N/A"),
            "previousClose": info.get("previousClose", "N/A"),
            "open": info.get("open", "N/A"),
            "dayLow": info.get("dayLow", "N/A"),
            "dayHigh": info.get("dayHigh", "N/A"),
            "volume": info.get("volume", "N/A"),
            "averageVolume": info.get("averageVolume", "N/A"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", "N/A"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", "N/A"),
            "trailingPE": info.get("trailingPE", "N/A"),
            "forwardPE": info.get("forwardPE", "N/A"),
            "dividendYield": info.get("dividendYield", "N/A") if info.get("dividendYield") else "N/A",
            "beta": info.get("beta", "N/A"),
            "description": info.get("longBusinessSummary", "N/A")
        }
        
        return result
        
    except Exception as e:
        raise ValueError(f"주식 정보 조회 중 오류가 발생했습니다: {str(e)}")


@mcp.tool()
def get_current_date(timezone: str = Field(
    default="Asia/Seoul", description="시간대 (예: Asia/Seoul, America/New_York, Europe/London)"
)) -> Dict:
    """현재 날짜와 시간 정보를 다양한 형식으로 반환합니다."""
    try:
        # 지정된 시간대에 맞는 현재 날짜/시간 가져오기
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        # 다양한 형식으로 날짜/시간 정보 반환
        return {
            "full_datetime": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "date_iso": now.strftime("%Y-%m-%d"),
            "time_iso": now.strftime("%H:%M:%S"),
            "date_ymd": now.strftime("%Y년 %m월 %d일"),
            "day_of_week": now.strftime("%A"),  # 요일 (영문)
            "day_of_week_kr": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][now.weekday()],
            "timezone": timezone,
            "unix_timestamp": int(now.timestamp()),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second
        }
    except Exception as e:
        raise ValueError(f"날짜 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")


@mcp.resource("stock://{symbol}/overview")
def get_stock_overview_resource(symbol: str) -> str:
    """주식에 대한 개요 정보를 제공하는 리소스입니다."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        overview = f"""# {info.get('longName', symbol)} ({symbol}) 개요

## 기본 정보
- **섹터**: {info.get('sector', 'N/A')}
- **산업**: {info.get('industry', 'N/A')}
- **시가총액**: {info.get('marketCap', 'N/A')}

## 주가 정보
- **전일 종가**: {info.get('previousClose', 'N/A')}
- **시가**: {info.get('open', 'N/A')}
- **일중 최저가**: {info.get('dayLow', 'N/A')}
- **일중 최고가**: {info.get('dayHigh', 'N/A')}
- **거래량**: {info.get('volume', 'N/A')}
- **평균 거래량**: {info.get('averageVolume', 'N/A')}

## 52주 범위
- **52주 최저가**: {info.get('fiftyTwoWeekLow', 'N/A')}
- **52주 최고가**: {info.get('fiftyTwoWeekHigh', 'N/A')}

## 주요 지표
- **PER(trailing)**: {info.get('trailingPE', 'N/A')}
- **PER(forward)**: {info.get('forwardPE', 'N/A')}
- **배당 수익률**: {info.get('dividendYield', 'N/A') if info.get('dividendYield') else 'N/A'}
- **베타**: {info.get('beta', 'N/A')}

## 회사 설명
{info.get('longBusinessSummary', '정보가 제공되지 않았습니다.')}
"""
        return overview
        
    except Exception as e:
        return f"주식 정보를 가져올 수 없습니다: {str(e)}"


if __name__ == "__main__":
    mcp.run()