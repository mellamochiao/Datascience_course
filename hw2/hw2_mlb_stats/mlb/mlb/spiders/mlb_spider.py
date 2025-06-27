import scrapy
from bs4 import BeautifulSoup

class MlbSpiderSpider(scrapy.Spider):
    name = "mlb_spider"
    allowed_domains = ["mlb.com"]
    start_urls = ["https://www.mlb.com/stats/regular-season"]

    def parse(self, response):
        # 使用 BeautifulSoup 解析網頁
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 假設我們要抓取某個表格中的數據
        table = soup.find('tbody', class_='notranslate')  # 確保選擇正確的表格標籤
        if table is not None:
            rows = table.find_all('tr')
            for row in rows:
                # 提取球員名字與姓氏
                first_name = row.find('span', class_='full-G_bAyq40').text.strip() if row.find('span', class_='full-G_bAyq40') else None
                last_name = row.find_all('span', class_='full-G_bAyq40')[-1].text.strip() if row.find_all('span', class_='full-G_bAyq40') else None
                
                # 組合名字
                player_name = f"{first_name} {last_name}" if first_name and last_name else None
                
                # 創建 item 對象
                item = {
                    'player': player_name,
                    'AB': row.find('td', attrs={'data-col': '3'}).text if row.find('td', attrs={'data-col': '3'}) else None,
                    'R': row.find('td', attrs={'data-col': '4'}).text if row.find('td', attrs={'data-col': '4'}) else None,
                    'H': row.find('td', attrs={'data-col': '5'}).text if row.find('td', attrs={'data-col': '5'}) else None,
                    'HR': row.find('td', attrs={'data-col': '8'}).text if row.find('td', attrs={'data-col': '8'}) else None,
                    'RBI': row.find('td', attrs={'data-col': '9'}).text if row.find('td', attrs={'data-col': '9'}) else None,
                    'BB': row.find('td', attrs={'data-col': '10'}).text if row.find('td', attrs={'data-col': '10'}) else None,
                    'K': row.find('td', attrs={'data-col': '11'}).text if row.find('td', attrs={'data-col': '11'}) else None,
                    'SB': row.find('td', attrs={'data-col': '12'}).text if row.find('td', attrs={'data-col': '12'}) else None,
                    'AVG': row.find('td', attrs={'data-col': '14'}).text if row.find('td', attrs={'data-col': '14'}) else None,
                    'OBP': row.find('td', attrs={'data-col': '15'}).text if row.find('td', attrs={'data-col': '15'}) else None,
                    'SLG': row.find('td', attrs={'data-col': '16'}).text if row.find('td', attrs={'data-col': '16'}) else None
                }
                yield item
        
        current_page = int(response.url.split('=')[-1]) if '=' in response.url else 1  # 當前頁數
        if current_page < 6:  # 確保最多爬取 6 頁
            next_page = f"https://www.mlb.com/stats/regular-season?page={current_page + 1}"
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            self.log("Table with class 'notranslate' not found", level=scrapy.log.ERROR)
