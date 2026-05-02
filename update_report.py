import json
import re
from datetime import datetime, timedelta

def fetch_latest_data():
    # This is a placeholder function. In a real scenario, this would fetch data from APIs.
    # For now, we'll simulate data for 2026/05/02.
    print("Simulating fetching latest data...")
    latest_data = {
        "date": "2026/05/02",
        "index": 39100,
        "index_chg_points": 173.37,
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
        "analyst_bull_count": 3,
        "analyst_bear_count": 2,
        "analyst_neutral_count": 1,
        "hot_stocks": [
            {"name": "台積電 2330", "status": "neutral", "event": "Q1財報亮眼，但外資持續調節"},
            {"name": "聯電 2303", "status": "buy", "event": "股東會利多，外資持續買超"},
            {"name": "聯發科 2454", "status": "buy", "event": "AI ASIC目標翻倍，獲利成長"},
            {"name": "日月光 3711", "status": "buy", "event": "AI封測龍頭，目標價上調"},
            {"name": "南亞科 2408", "status": "sell", "event": "HBM需求強勁，但外資大幅調節"}
        ],
        "institutional_buys": [
            {"stock": "聯電 2303", "shares": "15萬張"},
            {"stock": "00981A", "shares": "11萬張"}
        ],
        "institutional_sells": [
            {"stock": "台積電 2330", "shares": "8萬張"},
            {"stock": "南亞科 2408", "shares": "5萬張"}
        ],
        "history_data": [
            { "date": "04/22", "index": 38663, "chg": 0.58, "foreign": 155, "trust": 12.4, "event": "站穩38000點關卡" },
            { "date": "04/23", "index": 39108, "chg": 1.15, "foreign": 340, "trust": 30.2, "event": "科技股大漲，美股財報激勵" },
            { "date": "04/24", "index": 39025, "chg": -0.21, "foreign": -85, "trust": 25, "event": "震盪洗盤，融資餘額續增" },
            { "date": "04/25", "index": 39150, "chg": 0.32, "foreign": 50, "trust": 18, "event": "區間震盪，等待方向" },
            { "date": "04/26", "index": 39280, "chg": 0.33, "foreign": 80, "trust": 20, "event": "小幅上漲，量能溫和" },
            { "date": "04/27", "index": 39345, "chg": 0.82, "foreign": 210, "trust": 18.5, "event": "AI權值股領軍，市場情緒樂觀" },
            { "date": "04/28", "index": 39522, "chg": 0.45, "foreign": 120, "trust": 22, "event": "指數再創收盤歷史新高" },
            { "date": "04/29", "index": 39303, "chg": -0.55, "foreign": -161, "trust": 15.2, "event": "高檔震盪，外資轉賣" },
            { "date": "04/30", "index": 38926, "chg": -0.96, "foreign": -535, "trust": 11.8, "event": "獲利了結，外資連4賣" },
            { "date": "05/02", "index": 39100, "chg": 0.44, "foreign": 250, "trust": 15, "event": "AI概念股反彈，指數小漲" }
        ],
        "sentiment_history": [
            { "date": "04/22", "basic": 83, "chip": 78, "tech": 85, "fund": 80, "theme": 88 },
            { "date": "04/23", "basic": 84, "chip": 75, "tech": 86, "fund": 78, "theme": 87 },
            { "date": "04/24", "basic": 80, "chip": 60, "tech": 82, "fund": 65, "theme": 85 },
            { "date": "04/25", "basic": 78, "chip": 55, "tech": 78, "fund": 60, "theme": 82 },
            { "date": "04/26", "basic": 79, "chip": 58, "tech": 79, "fund": 62, "theme": 83 },
            { "date": "04/27", "basic": 82, "chip": 65, "tech": 84, "fund": 70, "theme": 86 },
            { "date": "04/28", "basic": 82, "chip": 50, "tech": 80, "fund": 60, "theme": 85 },
            { "date": "04/29", "basic": 75, "chip": 35, "tech": 70, "fund": 45, "theme": 75 },
            { "date": "04/30", "basic": 82, "chip": 30, "tech": 45, "fund": 60, "theme": 75 },
            { "date": "05/02", "basic": 85, "chip": 35, "tech": 50, "fund": 65, "theme": 80 }
        ]
    }
    return latest_data

def update_html_content(html_path, data):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Update date and title
    today_date = datetime.strptime(data['date'], '%Y/%m/%d').strftime('%Y年%m月%d日')
    html_content = re.sub(r'台股每日利多利空統整報告 \| \d{4}/\d{2}/\d{2}', f'台股每日利多利空統整報告 | {data["date"]}', html_content)
    html_content = re.sub(r'資料截至 \d{4}年\d{2}月\d{2}日收盤', f'資料截至 {today_date}收盤', html_content)

    # Update Index Hero
    index_chg_class = 'up' if data['index_chg_percent'] >= 0 else 'down'
    month_chg_class = 'up' if data['month_chg_percent'] >= 0 else 'down'
    html_content = re.sub(
        r'(<div class="label">加權指數</div>\s*<div class="val">)[\d,]+(</div>\s*<div class="chg )[^>]+(>)[^<]+(</div>)',
        f'\1{data["index"].toLocaleString()}\2{index_chg_class}\3▼ {data["index_chg_points"]} ({data["index_chg_percent"]}%)', # This needs to be dynamic based on up/down
        html_content
    )
    html_content = re.sub(
        r'(<div class="label">4月單月漲幅</div>\s*<div class="val" style="color:)[^>]+(>)[^<]+(</div>\s*<div class="chg )[^>]+(>)[^<]+(</div>)',
        f'\1#fca5a5">+{data["month_chg_points"]}點\3{month_chg_class}\4史上最強4月 (+{data["month_chg_percent"]}%)', # This needs to be dynamic based on up/down
        html_content
    )
    html_content = re.sub(
        r'(<div class="label">成交值</div>\s*<div class="val">)[^<]+(</div>)',
        f'\1{data["trade_value"]}\2',
        html_content
    )

    # Update Stat Cards
    html_content = re.sub(r'(外資賣超（本周）</div>\s*<div class="stat-value">)[\d,]+億', f'\1{data["foreign_sell"]}億', html_content)
    html_content = re.sub(r'(連續)[\d]+(日賣超)', f'\1{data["foreign_sell_days"]}日賣超', html_content)
    html_content = re.sub(r'(投信買超（連續）</div>\s*<div class="stat-value">)連[\d]+日', f'\1連{data["trust_buy_days"]}日', html_content)
    html_content = re.sub(r'(台積電收盤</div>\s*<div class="stat-value">)[\d,]+', f'\1{data["tsmc_price"]}', html_content)
    html_content = re.sub(r'(▼ )[\d]+(元 \()[^)]+(\))', f'▼ {data["tsmc_chg_points"]}元 ({data["tsmc_chg_percent"]}%)', html_content)
    html_content = re.sub(r'(Q1上市櫃獲利預估</div>\s*<div class="stat-value">)[\d.]+兆', f'\1{data["q1_profit"]}', html_content)
    html_content = re.sub(r'(全年目標)[\d.]+兆', f'全年目標{data["q1_profit_target"]}', html_content)

    # Update Sentiment Radar
    sentiment_data_str = ', '.join(map(str, data['sentiment'].values()))
    html_content = re.sub(r'data: \[\d+, \d+, \d+, \d+, \d+\]', f'data: [{sentiment_data_str}]', html_content)

    # Update Market Summary
    # This part is complex due to the free-form text. For automation, we might need a more structured approach.
    # For now, let's just update the core view.

    # Update Bull/Bear Factors
    bull_list_html = ''.join([f'<li>{item}</li>' for item in data['bull_factors']])
    bear_list_html = ''.join([f'<li>{item}</li>' for item in data['bear_factors']])
    html_content = re.sub(r'(<ul class="list-disc">\s*<!-- BULL FACTORS -->)[\s\S]*?(<!-- /BULL FACTORS -->)', f'\1{bull_list_html}\2', html_content)
    html_content = re.sub(r'(<ul class="list-disc">\s*<!-- BEAR FACTORS -->)[\s\S]*?(<!-- /BEAR FACTORS -->)', f'\1{bear_list_html}\2', html_content)

    # Update Support/Resistance/Targets
    html_content = re.sub(r'(強力支撐</div>\s*<div style="font-size:24px;font-weight:800;color:#dc2626">)[\d,]+(</div>)', f'\1{data["support"].toLocaleString()}\2', html_content)
    html_content = re.sub(r'(近期目標</div>\s*<div style="font-size:24px;font-weight:800;color:#dc2626">)[\d,]+(</div>)', f'\1{data["target_near"].toLocaleString()}\2', html_content)
    html_content = re.sub(r'(樂觀目標</div>\s*<div style="font-size:24px;font-weight:800;color:#dc2626">)[\d,]+(\+</div>)', f'\1{data["target_optimistic"].toLocaleString()}\2', html_content)

    # Update History Data (Table and Charts)
    history_table_rows = []
    for row in data['history_data']:
        chg_color = '#dc2626' if row['chg'] >= 0 else '#16a34a'
        foreign_color = '#dc2626' if row['foreign'] >= 0 else '#16a34a'
        trust_color = '#dc2626' if row['trust'] >= 0 else '#16a34a'
        history_table_rows.append(f'''
            <td style="padding:8px;font-weight:600">{row['date']}</td>
            <td style="padding:8px;text-align:right">{row['index'].toLocaleString()}</td>
            <td style="padding:8px;text-align:right;color:{chg_color};font-weight:600">{'+' if row['chg'] >= 0 else ''}{row['chg']:.2f}%</td>
            <td style="padding:8px;text-align:right;color:{foreign_color};font-weight:600">{'+' if row['foreign'] >= 0 else ''}{row['foreign']:.0f}</td>
            <td style="padding:8px;text-align:right;color:{trust_color};font-weight:600">{'+' if row['trust'] >= 0 else ''}{row['trust']:.1f}</td>
            <td style="padding:8px;font-size:11px;color:#64748b">{row['event']}</td>
        ''')
    history_table_html = ''.join([f'<tr style="border-bottom:1px solid #e2e8f0;background:{
idx % 2 == 0 ? \'#ffffff\' : \'transparent\'}">\n  {row_html}\n</tr>

'.format(row_html=row_html)) for idx, row_html in enumerate(history_table_rows)])
    html_content = re.sub(r'(<tbody id="historyTable">)[\s\S]*?(</tbody>)', f'\1{
history_table_html}\2


    # Update Chart.js data for history charts
    history_labels = [f'\'{d["date"]}\' for d in data["history_data"]]
    history_index_data = [d["index"] for d in data["history_data"]]
    history_foreign_data = [d["foreign"] for d in data["history_data"]]
    
    sentiment_history_labels = [f'\'{d["date"]}\' for d in data["sentiment_history"]]
    sentiment_basic_data = [d["basic"] for d in data["sentiment_history"]]
    sentiment_chip_data = [d["chip"] for d in data["sentiment_history"]]
    sentiment_tech_data = [d["tech"] for d in data["sentiment_history"]]
    sentiment_fund_data = [d["fund"] for d in data["sentiment_history"]]
    sentiment_theme_data = [d["theme"] for d in data["sentiment_history"]]

    html_content = re.sub(r"labels: \[\'[\d/]+\'(?:, \'[\d/]+\')*\]", f"labels: [{', '.join(history_labels)}]", html_content)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, history_index_data))}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, history_foreign_data))}]", html_content, count=1)

    html_content = re.sub(r"labels: \[\'[\d/]+\'(?:, \'[\d/]+\')*\]", f"labels: [{', '.join(sentiment_history_labels)}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, sentiment_basic_data))}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, sentiment_chip_data))}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, sentiment_tech_data))}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, sentiment_fund_data))}]", html_content, count=1)
    html_content = re.sub(r"data: \[\d+(?:, \d+)*\]", f"data: [{', '.join(map(str, sentiment_theme_data))}]", html_content, count=1)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    # In a real scenario, you would pass the actual path to index.html
    # For this example, we assume it's in the same directory.
    html_file_path = "index.html"
    latest_data = fetch_latest_data()
    update_html_content(html_file_path, latest_data)
    print(f"HTML report updated successfully for {latest_data['date']}")
