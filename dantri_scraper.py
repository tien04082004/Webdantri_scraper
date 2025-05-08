import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import schedule
import os
import logging
import argparse

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    """Thiết lập Selenium WebDriver với Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy ở chế độ không giao diện
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_dantri():
    """Vào dữ liệu bài viết từ dantri.com.vn."""
    logger.info("Bắt đầu quá trình vào dữ liệu...")
    driver = setup_driver()
    data = []

    try:
# 1. Truy cập trang web
        driver.get("https://dantri.com.vn/")
        time.sleep(3)  

# 2. Chọn danh mục tin tức (ví dụ: Công nghệ)
        category_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Công nghệ')]")
        category_link.click()
        time.sleep(3)

# 3. Tìm kiếm (nếu có ô tìm kiếm)
        try:
            search_box = driver.find_element(By.XPATH, "//input[@placeholder='Tìm kiếm']")
            search_box.send_keys("công nghệ")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            logger.warning("Không tìm thấy ô tìm kiếm, bỏ qua bước tìm kiếm.")

# 4. Lấy dữ liệu từ tất cả các trang
        while True:
            # Lấy danh sách bài viết
            articles = driver.find_elements(By.XPATH, "//article[contains(@class, 'article-item')]")
            article_links = [article.find_element(By.TAG_NAME, 'a').get_attribute('href') for article in articles]

# 5. Vào dữ liệu từ từng bài viết
            for link in article_links:
                try:
                    driver.get(link)
                    time.sleep(2)

                    # Lấy tiêu đề
                    title = driver.find_element(By.TAG_NAME, 'h1').text.strip()

                    # Lấy mô tả
                    try:
                        description = driver.find_element(By.XPATH, "//h2[@class='singular-sapo']").text.strip()
                    except:
                        description = ""

                    # Lấy hình ảnh
                    try:
                        image = driver.find_element(By.XPATH, "//figure[@class='image align-center']//img").get_attribute('src')
                    except:
                        image = ""

                    # Lấy nội dung bài viết
                    try:
                        content_elements = driver.find_elements(By.XPATH, "//div[@class='singular-content']//p")
                        content = " ".join([elem.text.strip() for elem in content_elements])
                    except:
                        content = ""

                    data.append({
                        'Tiêu đề': title,
                        'Mô tả': description,
                        'Hình ảnh': image,
                        'Nội dung': content,
                        'Link': link,
                        'Thời gian vào': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    logger.info(f"Đã vào bài viết: {title}")
                except Exception as e:
                    logger.error(f"Lỗi khi vào bài viết {link}: {e}")

            # Kiểm tra nút "Trang tiếp"
            try:
                next_button = driver.find_element(By.XPATH, "//a[@class='page-item next']")
                next_button.click()
                time.sleep(3)
            except:
                logger.info("Không còn trang tiếp theo, kết thúc vào dữ liệu.")
                break

# 6. Lưu dữ liệu vào file CSV
        if data:
            df = pd.DataFrame(data, columns=["title", "description", "image", "content", "link"])
            df.to_excel("dantri.xlsx")
            print(df)


    except Exception as e:
        logger.error(f"Lỗi trong quá trình vào dữ liệu: {e}")
    finally:
        driver.quit()
# 7. Set lịch chạy vào lúc 6h sáng hằng ngày
def schedule_task():
    """Lập lịch chạy hàng ngày lúc 6 giờ sáng."""
    schedule.every().day.at("06:00").do(scrape_dantri)
    logger.info("Đã thiết lập lịch chạy lúc 6h sáng hàng ngày.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vào dữ liệu từ DanTri")
    parser.add_argument('--schedule', action='store_true', help="Chạy theo lịch 6h sáng")
    args = parser.parse_args()

    if args.schedule:
        schedule_task()
    else:
        scrape_dantri()