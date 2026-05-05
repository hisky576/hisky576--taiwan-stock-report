"""
台股每日報告自動更新腳本
每日從 TWSE 官方 API 抓取真實數據並更新 index.html
"""
import re
import json
import requests
from datetime import datetime, timedelta

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.twse.com.tw/'
}


def get_latest_trading_date():
    """取得最近交易日（跳過週末）"""
    today = datetime.now()
    # 若今天是週六，回退到週五
    if today.weekday() == 5:
        today -= timedelta(days=1)
    # 若今天是週日，回退到週五
    elif today.weekday() == 6:
        today -= timedelta(days=2)
    return today


def fetch_taiex_data():
    """抓取加權指數當日數據"""
    try:
        url = 'https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?response=json'
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        if data.get('data'):
            rows = data['data']
            latest = rows[-1]  # 最新一筆
            # 格式: ['115/05/04', '39,228.39', '40,755.52', '39,228.39', '40,705.14']
            date_str = latest[0]  # 民國年
            closing = float(latest[4].replace(',', ''))
            opening = float(latest[1].replace(',', ''))

            # 轉換民國年為西元年
            parts = date_str.split('/')
            year = int(parts[0]) + 1911
            month = int(parts[1])
            day = int(parts[2])
            date_formatted = f"{year}/{month:02d}/{day:02d}"

            # 取得前一日收盤
            prev_close = None
            if len(rows) >= 2:
                prev_close = float(rows[-2][4].replace(',', ''))
            else:
                # 本月只有一筆，抓上個月最後一日
                try:
                    prev_month = month - 1 if month > 1 else 12
                    prev_year = year if month > 1 else year - 1
                    prev_date = f"{prev_year}{prev_month:02d}01"
                    url2 = f'https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?response=json&date={prev_date}'
                    r2 = requests.get(url2, headers=HEADERS, timeout=15)
                    data2 = r2.json()
                    if data2.get('data'):
                        prev_close = float(data2['data'][-1][4].replace(',', ''))
                        rows = data2['data'] + rows  # 合併歷史
                except Exception as e2:
                    print(f"上月數據 API 錯誤: {e2}")

            chg_points = round(closing - prev_close, 2) if prev_close else 0
            chg_percent = round(chg_points / prev_close * 100, 2) if prev_close else 0

            print(f"加權指數: {closing} ({chg_points:+.2f}, {chg_percent:+.2f}%)")
            return {
                'date': date_formatted,
                'closing': closing,
                'opening': opening,
                'chg_points': chg_points,
                'chg_percent': chg_percent,
                'history': rows
            }
    except Exception as e:
        print(f"加權指數 API 錯誤: {e}")
    return None


def fetch_institutional_data():
    """抓取三大法人買賣超彙總"""
    try:
        url = 'https://www.twse.com.tw/rwd/zh/fund/BFI82U?response=json'
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        if data.get('stat') == 'OK' or data.get('data'):
            result = {
                'foreign_net': 0,
                'trust_net': 0,
                'dealer_net': 0,
                'total_net': 0
            }
            for row in data.get('data', []):
                name = row[0]
                # 買賣差額（元）
                net_str = row[3].replace(',', '').replace('+', '')
                try:
                    net_val = int(net_str)
                except:
                    net_val = 0

                if '外資及陸資(不含外資自營商)' in name:
                    result['foreign_net'] = net_val
                elif '投信' in name and '自營商' not in name:
                    result['trust_net'] = net_val
                elif '自營商(自行買賣)' in name:
                    result['dealer_net'] = net_val
                elif '合計' in name:
                    result['total_net'] = net_val

            # 轉換為億元
            result['foreign_net_yi'] = round(result['foreign_net'] / 1e8, 2)
            result['trust_net_yi'] = round(result['trust_net'] / 1e8, 2)
            result['dealer_net_yi'] = round(result['dealer_net'] / 1e8, 2)
            result['total_net_yi'] = round(result['total_net'] / 1e8, 2)

            print(f"外資: {result['foreign_net_yi']:+.2f}億, 投信: {result['trust_net_yi']:+.2f}億")
            return result
    except Exception as e:
        print(f"三大法人 API 錯誤: {e}")
    return None


def fetch_tsmc_data():
    """抓取台積電（2330）當日數據"""
    try:
        url = 'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?stockNo=2330&response=json'
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        if data.get('data'):
            latest = data['data'][-1]
            # ['115/05/04', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數', '註記']
            closing = float(latest[6].replace(',', ''))
            chg_str = latest[7].replace(',', '')
            chg = float(chg_str) if chg_str not in ['--', ''] else 0
            chg_percent = round(chg / (closing - chg) * 100, 2) if (closing - chg) != 0 else 0
            print(f"台積電: {closing} ({chg:+.2f}, {chg_percent:+.2f}%)")
            return {
                'price': closing,
                'chg': chg,
                'chg_percent': chg_percent
            }
    except Exception as e:
        print(f"台積電 API 錯誤: {e}")
    return None


def fetch_trade_value():
    """抓取大盤成交值"""
    try:
        url = 'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?response=json'
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        for t in data.get('tables', []):
            if t and t.get('fields') and '成交金額' in str(t.get('fields', [])):
                total = 0
                for row in t.get('data', []):
                    if '一般股票' in row[0] or 'ETF' in row[0]:
                        try:
                            total += int(row[1].replace(',', ''))
                        except:
                            pass
                if total > 0:
                    yi = round(total / 1e12, 2)
                    print(f"成交值: {yi}兆")
                    return f"{yi}兆"
    except Exception as e:
        print(f"成交值 API 錯誤: {e}")
    return None


def build_taiex_history(taiex_data):
    """建立近10日指數歷史"""
    if not taiex_data or not taiex_data.get('history'):
        return []

    rows = taiex_data['history']
    result = []
    prev_close = None

    for row in rows[-10:]:
        date_str = row[0]  # 民國年 115/05/04
        closing = float(row[4].replace(',', ''))
        parts = date_str.split('/')
        month = int(parts[1])
        day = int(parts[2])
        label = f"{month:02d}/{day:02d}"

        chg = round(closing - prev_close, 2) if prev_close else 0
        chg_pct = round(chg / prev_close * 100, 2) if prev_close else 0

        result.append({
            'date': label,
            'index': int(closing),
            'chg': chg_pct,
            'event': ''
        })
        prev_close = closing

    return result


def update_html(html_path, taiex, institutional, tsmc, trade_value):
    """更新 index.html 的關鍵數據"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    date_str = taiex['date'] if taiex else datetime.now().strftime('%Y/%m/%d')
    today_date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y年%m月%d日')

    # 1. 更新標題日期
    content = re.sub(
        r'台股每日利多利空統整報告 \| \d{4}/\d{2}/\d{2}',
        '台股每日利多利空統整報告 | ' + date_str,
        content
    )
    # 更新 subtitle 日期（格式: 2026年5月1日 ｜ 資料截至 4月30日收盤）
    content = re.sub(
        r'\d{4}年\d{1,2}月\d{1,2}日 ｜ 資料截至 \d{1,2}月30日收盤',
        today_date + ' ｜ 資料截至 ' + today_date + '收盤',
        content
    )
    # 更新其他格式的資料截至
    content = re.sub(
        r'資料截至 \d{4}年\d{2}月\d{2}日收盤',
        '資料截至 ' + today_date + '收盤',
        content
    )

    # 2. 更新加權指數
    if taiex:
        idx = int(taiex['closing'])
        idx_fmt = f"{idx:,}"
        chg_pts = taiex['chg_points']
        chg_pct = taiex['chg_percent']
        arrow = '▲' if chg_pts >= 0 else '▼'
        chg_class = 'up' if chg_pts >= 0 else 'down'
        chg_color = '#dc2626' if chg_pts >= 0 else '#16a34a'

        # 更新指數數值
        content = re.sub(
            r'(<div class="label">加權指數</div>\s*<div class="val">)[\d,]+(</div>)',
            r'\g<1>' + idx_fmt + r'\2',
            content
        )
        # 更新漲跌（匹配加權指數後面的 chg div）
        new_chg_div = f'<div class="chg {chg_class}">{arrow} {abs(chg_pts):.2f} ({abs(chg_pct):.2f}%)</div>'
        content = re.sub(
            r'(<div class="label">加權指數</div>\s*<div class="val">[\d,]+</div>\s*)<div class="chg (?:up|down)">[^<]*</div>',
            r'\g<1>' + new_chg_div,
            content
        )

    # 3. 更新台積電
    if tsmc:
        price = int(tsmc['price'])
        chg = tsmc['chg']
        chg_pct = tsmc['chg_percent']
        arrow = '▲' if chg >= 0 else '▼'
        chg_class = 'bull' if chg >= 0 else 'neutral'

        # 更新台積電收盤價
        content = re.sub(
            r'(台積電收盤</div>\s*<div class="stat-value">)[\d,]+(</div>)',
            r'\g<1>' + f'{price:,}' + r'\2',
            content
        )
        # 更新台積電漲跌
        content = re.sub(
            r'(台積電收盤</div>\s*<div class="stat-value">[\d,]+</div>\s*<div class="stat-sub">)[^<]+(</div>)',
            r'\g<1>' + f'{arrow} {abs(chg):.0f}元 ({abs(chg_pct):.2f}%)' + r'\2',
            content
        )

    # 4. 更新外資買賣超
    if institutional:
        foreign = institutional['foreign_net_yi']
        trust = institutional['trust_net_yi']
        label = '外資買超（本周）' if foreign >= 0 else '外資賣超（本周）'
        arrow_f = '▲買超' if foreign >= 0 else '▼賣超'

        # 更新外資買賣超金額（不管標籤是買超還是賣超）
        content = re.sub(
            r'(外資(?:買超|賣超)（本周）</div>\s*<div class="stat-value">)[\d,]+億',
            r'\g<1>' + f'{abs(foreign):.0f}億',
            content
        )
        # 更新外資買賣超子標題
        content = re.sub(
            r'(外資(?:買超|賣超)（本周）</div>\s*<div class="stat-value">[\d,]+億</div>\s*<div class="stat-sub">)連續\d+日(?:買超|賣超)',
            r'\g<1>' + f'連續1日{arrow_f}',
            content
        )

    # 5. 更新成交値
    if trade_value:
        content = re.sub(
            r'(<div class="label">成交値</div>\s*<div class="val">)[^<]+(</div>)',
            r'\g<1>' + trade_value + r'\2',
            content
        )

    # 6. 更新跑馬燈
    if taiex:
        idx_fmt = f"{int(taiex['closing']):,}"
        chg_pts = taiex['chg_points']
        chg_pct = taiex['chg_percent']
        arrow = '▲' if chg_pts >= 0 else '▼'
        chg_class = 'up' if chg_pts >= 0 else 'down'
        ticker_taiex = (
            f'<span class="ticker-item">'
            f'<span class="name">加權指數</span>'
            f'<span class="price">{idx_fmt}</span>'
            f'<span class="chg {chg_class}">{arrow} {abs(chg_pts):.2f} ({abs(chg_pct):.2f}%)</span>'
            f'</span>'
        )
        content = re.sub(
            r'<span class="ticker-item"><span class="name">加權指數</span><span class="price">[\d,]+</span><span class="chg (?:up|down)">[^<]*</span></span>',
            ticker_taiex,
            content,
            flags=re.DOTALL
        )

    if tsmc:
        price = int(tsmc['price'])
        chg = tsmc['chg']
        chg_pct_t = tsmc['chg_percent']
        arrow_t = '▲' if chg >= 0 else '▼'
        chg_class_t = 'up' if chg >= 0 else 'down'
        ticker_tsmc = (
            f'<span class="ticker-item">'
            f'<span class="name">台積電 2330</span>'
            f'<span class="price">{price:,}</span>'
            f'<span class="chg {chg_class_t}">{arrow_t} {abs(chg):.0f} ({abs(chg_pct_t):.2f}%)</span>'
            f'</span>'
        )
        content = re.sub(
            r'<span class="ticker-item"><span class="name">台積電 2330</span><span class="price">[\d,]+</span><span class="chg (?:up|down)">[^<]*</span></span>',
            ticker_tsmc,
            content,
            flags=re.DOTALL
        )

    if institutional:
        foreign = institutional['foreign_net_yi']
        trust = institutional['trust_net_yi']
        total = institutional.get('total_net_yi', foreign + trust)

        # 跑馬燈三大法人合計
        arrow_total = '▲' if total >= 0 else '▼'
        chg_class_total = 'up' if total >= 0 else 'down'
        action_total = '買超' if total >= 0 else '賣超'
        ticker_total = (
            f'<span class="ticker-item">'
            f'<span class="name">三大法人</span>'
            f'<span class="price">合計</span>'
            f'<span class="chg {chg_class_total}">{arrow_total} {action_total}{abs(total):.2f}億</span>'
            f'</span>'
        )
        content = re.sub(
            r'<span class="ticker-item"><span class="name">三大法人</span><span class="price">合計</span><span class="chg (?:up|down)">[^<]*</span></span>',
            ticker_total,
            content,
            flags=re.DOTALL
        )

        # 跑馬燈外資本周
        arrow_f = '▲' if foreign >= 0 else '▼'
        chg_class_f = 'up' if foreign >= 0 else 'down'
        action_f = '買超' if foreign >= 0 else '賣超'
        ticker_foreign = (
            f'<span class="ticker-item">'
            f'<span class="name">外資本周</span>'
            f'<span class="price">動向</span>'
            f'<span class="chg {chg_class_f}">{arrow_f} {action_f}{abs(foreign):.2f}億元</span>'
            f'</span>'
        )
        content = re.sub(
            r'<span class="ticker-item"><span class="name">外資本周</span><span class="price">(?:提款|動向)</span><span class="chg (?:up|down)">[^<]*</span></span>',
            ticker_foreign,
            content,
            flags=re.DOTALL
        )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"HTML 更新完成：{date_str}")


if __name__ == "__main__":
    print("=" * 50)
    print("台股每日報告更新腳本")
    print("=" * 50)

    # 抓取數據
    taiex = fetch_taiex_data()
    institutional = fetch_institutional_data()
    tsmc = fetch_tsmc_data()
    trade_value = fetch_trade_value()

    # 更新 HTML
    update_html("index.html", taiex, institutional, tsmc, trade_value)

    print("=" * 50)
    print("更新完成！")
