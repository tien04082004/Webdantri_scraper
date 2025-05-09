# Dự án Vào Dữ liệu DanTri

Dự án này sử dụng Python và Selenium để vào dữ liệu bài viết từ trang [DanTri](https://dantri.com.vn/), lưu vào file Excel và lập lịch chạy tự động lúc 6 giờ sáng hàng ngày.

## Yêu cầu
- Python 3.6+
- Google Chrome (để Selenium sử dụng ChromeDriver)
- Git

## Cài đặt
1. **Clone repository**:
   ```bash
   git clone https://github.com/<tien04082004>/Webdantri_scraper.git
   cd Webdantri_scraper
2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt

   selenimun:
   pip install selenium

   pandas:
   pip install pandas

   webdriver_manager:
   pip install webdriver_manager

   schedule:
   pip install schedule

## Sử dụng
1. Chạy chương trình
   python dantri_scraper.py

2. Kết quả
   File dantri.xlsx sẽ được lưu trong thư mục output/.

3. Lập lịch chạy tự động chạy với lịch 6h sáng hằng ngày
   python dantri_scraper.py --schedule
