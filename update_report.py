import json
import re
from datetime import datetime, timedelta

def fetch_latest_data():
    """
    模擬抓取最新市場數據。
    實際部署時可替換為真實 API 呼叫。
    """
    print("Fetching latest data...")

    # 取得今日日期
    today = datetime.now()
    # 若為週末則回退到週五
    if today.weekday() == 5:  # 週六
        today = today - timedelta(days=1)
    elif today.weekday() == 6:  # 週日
        today = today - timedelta(days=2)

    date_str = today.strftime('%Y/%m/%d')

    latest_data = {
        "date": date_str,
        "index": 39100,
        "index_chg_points": 173,
        "index_chg_percent": 0.44,
        "month_chg_points": 7376,
        "month_chg_percent": 23.2,
        "trade_value": "1.05兆",
        "foreign_sell": 250,
        "foreign_sell_days": 1,
        "trust_buy": 15,
        "trust_buy_days": 9,
        "tsmc_price": 2150,
        "tsmc_chg_points": 15,
        "tsmc_chg_percent": 0.70,
        "q1_profit": "1.55兆",
        "q1_profit_target": "6兆",
        "sentiment": {
            "basic": 85,
            "chip": 35,
            "tech": 50,
            "fund": 65,
            "theme": 80
        },
        "bull_factors": [
            "企業獲利持續成長，Q1表現優於預期",
            "AI需求旺盛，相關供應鏈訂單滿載",
            "ETF資金持續流入，提供市場流動性",
            "520行情與Computex題材持續發酵",
            "國際資金對台灣科技股仍具信心"
        ],
        "bear_factors": [
            "外資持續調節大型權值股，賣壓未止",
            "技術面指標高檔鈍化，短線修正壓力大",
            "全球通膨壓力未解，升息預期影響資金",
            "地緣政治風險仍存，影響投資人信心",
            "新台幣貶值壓力，外資匯出意願高"
        ],
        "support": 38000,
        "resistance": 40000,
        "target_near": 41500,
        "target_optimistic": 43500,
        "hot_stocks": [
            {"name": "台積電 2330", "status": "neutral", "event": "Q1財報亮眼，但外資持續調節"},
            {"name": "聯電 2303", "status": "buy", "event": "股東會利多，外資持續買超"},
            {"name": "聯發科 2454", "status": "buy", "event": "AI ASIC目標翻倍，獲利成長"},
            {"name": "日月光 3711", "status": "buy", "event": "AI封測龍頭，目標價上調"},
            {"name": "南亞科 2408", "status": "sell", "event": "HBM需求強勁，但外資大幅調節"}
        ],
        "history_data": [
            {"date": "04/22", "index": 38663, "chg": 0.58, "foreign": 155, "trust": 12.4, "event": "站穩38000點關卡"},
            {"date": "04/23", "index": 39108, "chg": 1.15, "foreign": 340, "trust": 30.2, "event": "科技股大漲，美股財報激勵"},
            {"date": "04/24", "index": 39025, "chg": -0.21, "foreign": -85, "trust": 25, "event": "震盪洗盤，融資餘額續增"},
            {"date": "04/25", "index": 39150, "chg": 0.32, "foreign": 50, "trust": 18, "event": "區間震盪，等待方向"},
            {"date": "04/26", "index": 39280, "chg": 0.33, "foreign": 80, "trust": 20, "event": "小幅上漲，量能溫和"},
            {"date": "04/27", "index": 39345, "chg": 0.82, "foreign": 210, "trust": 18.5, "event": "AI權值股領軍，市場情緒樂觀"},
            {"date": "04/28", "index": 39522, "chg": 0.45, "foreign": 120, "trust": 22, "event": "指數再創收盤歷史新高"},
            {"date": "04/29", "index": 39303, "chg": -0.55, "foreign": -161, "trust": 15.2, "event": "高檔震盪，外資轉賣"},
            {"date": "04/30", "index": 38926, "chg": -0.96, "foreign": -535, "trust": 11.8, "event": "獲利了結，外資連4賣"},
            {"date": "05/02", "index": 39100, "chg": 0.44, "foreign": 250, "trust": 15, "event": "AI概念股反彈，指數小漲"}
        ]
    }
    return latest_data


def update_html_content(html_path, data):
    """讀取 index.html 並更新日期標題"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 更新標題日期
    html_content = re.sub(
        r'台股每日利多利空統整報告 \| \d{4}/\d{2}/\d{2}',
        '台股每日利多利空統整報告 | ' + data['date'],
        html_content
    )

    # 更新資料截至日期
    today_date = datetime.strptime(data['date'], '%Y/%m/%d').strftime('%Y年%m月%d日')
    html_content = re.sub(
        r'資料截至 \d{4}年\d{2}月\d{2}日收盤',
        '資料截至 ' + today_date + '收盤',
        html_content
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("HTML title and date updated successfully.")


if __name__ == "__main__":
    html_file_path = "index.html"
    latest_data = fetch_latest_data()
    update_html_content(html_file_path, latest_data)
    print("Report updated successfully for " + latest_data['date'])
