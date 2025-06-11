import fake_data
import datetime

# Tạo dữ liệu mẫu từ ngày 1/1/2022 đến ngày 31/12/2022
start_date = datetime.datetime(2024, 5, 1)
end_date = datetime.datetime(2024, 5, 5)

fake_data.generate_expenses(10, start_date, end_date)  # Tạo 10 mục chi tiêu giả trong năm 2022
fake_data.generate_balance(20, 12, start_date, end_date)  # Tạo 5 mục số dư giả trong năm 2022
