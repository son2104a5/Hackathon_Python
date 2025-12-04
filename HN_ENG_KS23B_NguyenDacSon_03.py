import csv
import os
import matplotlib.pyplot as plt

hotels = []


def in_menu():
    print("============ MENU ============")
    print("1. Hiển thị danh sách phòng")
    print("2. Thêm mới phòng")
    print("3. Cập nhật thông tin phòng")
    print("4. Xoá phòng")
    print("5. Tìm kiếm phòng")
    print("6. Sắp xếp danh sách phòng")
    print("7. Thống kê doanh thu")
    print("8. Vẽ biểu đồ thống kê điểm TB")
    print("9. Lưu vào file CSV")
    print("0. Thoát")


def lay_du_lieu():
    """
    Lấy dữ liệu từ file
    Nếu không tìm thấy sẽ báo lỗi
    """
    global hotels
    if os.path.exists("data.csv"):
        with open("data.csv", "r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            hotels = list(reader)
            for hotel in hotels:
                if "gia_ngay" in hotel:
                    hotel["gia_ngay"] = float(hotel["gia_ngay"])
                if "so_ngay_o" in hotel:
                    hotel["so_ngay_o"] = float(hotel["so_ngay_o"])
                if "dich_vu_them" in hotel:
                    hotel["dich_vu_them"] = float(hotel["dich_vu_them"])
                if "tong_tien" in hotel:
                    hotel["tong_tien"] = float(hotel["tong_tien"])
    else:
        print("Không tìm thấy file data.csv")


def in_danh_sach_don():
    """
        in danh sách ra console theo dạng bảng
    """
    if not hotels:
        print("Danh sách đơn trống!")
        return

    print("\n===== DANH SÁCH ĐƠN ĐẶT PHÒNG =====")
    header = (f"{'Mã phòng':<15} {'Loại phòng':<15} {'Giá ngày':<15} "
              f"{'Số ngày ở':<15} {'Dịch vụ thêm':<15} {'Tổng tiền':<15} "
              f"{'Phân hạng':<10}")
    print(header)
    print("-" * 110)

    for r in hotels:
        print(f"{r['ma_phong']:<15} {r['loai_phong']:<15} {r['gia_ngay']:<15} "
              f"{r['so_ngay_o']:<15} {r['dich_vu_them']:<15} "
              f"{r['tong_tien']:<15} {r['phan_hang']:<10}")

    print("-" * 110)


def them_don_dat_phong():
    """
    thêm mới đơn đặt phòng, nếu mã đơn đã tồn tại thì báo lỗi ra để nhập lại
    """
    global hotels

    print("\n===== THÊM MỚI ĐƠN ĐẶT PHÒNG =====")

    while True:
        ma = input("Nhập mã phòng: ").strip()
        if any(r["ma_phong"] == ma for r in hotels):
            print("Mã phòng đã tồn tại!")
        else:
            break

    loai_phong = input("Nhập loại phòng: ").strip()

    def nhap_du_lieu(data):
        """
        hàm nhập dữ liệu
        """
        while True:
            try:
                d = float(input(f"Nhập {data}: "))
                if 0 < d:
                    return d
                else:
                    print("Giá trị nhập vào phải lớn hơn 0!")
            except ValueError:
                print("Nhập số!")

    gia_phong = nhap_du_lieu("giá phòng")
    so_ngay_o = nhap_du_lieu("số ngày ở")
    dich_vu_them = nhap_du_lieu("phí dịch vụ thêm")

    tong_tien = round((gia_phong * so_ngay_o) + dich_vu_them)
    if tong_tien > 10000000:
        phan_hang = "Diamond"
    elif tong_tien > 5000000:
        phan_hang = "Gold"
    else: 
        phan_hang = "Silver"

    don_moi = {
        "ma_phong": ma,
        "loai_phong": loai_phong,
        "gia_ngay": gia_phong,
        "so_ngay_o": so_ngay_o,
        "dich_vu_them": dich_vu_them,
        "tong_tien": tong_tien,
        "phan_hang": phan_hang
    }

    hotels.append(don_moi)

    print("Thêm dơn đặt phòng thành công!")


def cap_nhat_don():
    """
        cập nhật thông tin phòng theo mã, nếu mã không tồn tại thì báo
          lỗi và chuyển ra menu
    """
    global hotels
    print("\n===== CẬP NHẬT THÔNG TIN ĐƠN ĐẶT PHÒNG =====")

    ma = input("Nhập mã đơn đặt phòng cần sửa: ").strip()
    hotel = next((r for r in hotels if r["ma_phong"] == ma), None)

    if hotel is None:
        print("Không tìm thấy đơn!")
        return

    print(f"Đang sửa đơn đặt phòng mã: {hotel['ma_phong']}")

    def nhap_du_lieu(data):
        """
        hàm nhập dữ liệu
        """
        while True:
            try:
                d = float(input(f"Nhập {data}: "))
                if 0 < d:
                    return d
                else:
                    print("Giá trị nhập vào phải lớn hơn 0!")
            except ValueError:
                print("Nhập số!")

    hotel["so_ngay_o"] = nhap_du_lieu("số ngày ở")
    hotel["dich_vu_them"] = nhap_du_lieu("phí dịch vụ thêm")

    tong_tien = round(
        (hotel["gia_ngay"] * hotel["so_ngay_o"]) +
        hotel["dich_vu_them"]
    )
    hotel["tong_tien"] = tong_tien
    
    if tong_tien > 10000000:
        hotel["phan_hang"] = "Diamond"
    elif tong_tien > 5000000:
        hotel["phan_hang"] = "Gold"
    else: 
        hotel["phan_hang"] = "Silver"

    print("Cập nhật đơn đặt phòng thành công!")


def xoa_don():
    """
    hàm xóa đơn đặt phòng, có xác nhận trc khi xóa
    """
    global hotels
    print("\n===== XOÁ ĐƠN =====")

    ma = input("Nhập mã đơn đặt phòng cần xoá: ").strip()
    hotel = next((s for s in hotels if s["ma_phong"] == ma), None)

    if hotel is None:
        print("Không tìm thấy mã đơn!")
        return

    print(f"Bạn đang xoá đơn đặt phòng mã: {hotel['ma_phong']}")
    confirm = input("Bạn có chắc muốn xoá? (y/n): ").lower()

    if confirm == "y":
        hotels.remove(hotel)
        print("Đã xoá đơn.")
    else:
        print("Đã huỷ xoá.")


def tim_phong():
    """
    hàm tìm kiếm phòng, theo mã hoặc loại phòng
    """
    global hotels
    print("\n===== TÌM KIẾM PHÒNG =====")

    keyword = input("Nhập mã hoặc loại phòng: ").strip().lower()

    results = [
        hotel for hotel in hotels
        if keyword in hotel["ma_phong"].lower()
        or keyword in hotel["loai_phong"].lower()
    ]

    if not results:
        print("Không tìm thấy kết quả!")
        return

    print("\nKẾT QUẢ TÌM KIẾM:")
    for hotel in results:
        print(f"{hotel['ma_phong']} - {hotel['loai_phong']} | "
              f"Tổng tiền: {hotel['tong_tien']} | {hotel['phan_hang']}")


def sap_xep_phong():
    """
    hàm sắp xếp phòng, có theo tổng tiền và số ngày ở (giảm dần)
    """
    global students
    print("\n===== SẮP XẾP DANH SÁCH =====")
    print("1. Sắp xếp theo tổng tiền giảm dần")
    print("2. Sắp xếp theo số ngày ở giảm dần")

    choice = input("Chọn kiểu sắp xếp: ")

    if choice == "1":
        hotels.sort(key=lambda s: s["tong_tien"], reverse=True)
        print("Đã sắp xếp xong.")
    elif choice == "2":
        hotels.sort(key=lambda s: s["so_ngay_o"], reverse=True)
        print("Đã sắp xếp xong.")
    else:
        print("Lựa chọn không hợp lệ!")


def thong_ke_phan_hang():
    """
    hàm thống kê, thống kê lại số lượng phòng và phân hạng của phòng
    """
    global hotels
    thong_ke = {"Diamond": 0, "Gold": 0, "Silver": 0}

    for hotel in hotels:
        xl = hotel["phan_hang"]
        if xl in thong_ke:
            thong_ke[xl] += 1

    for loai, so_luong in thong_ke.items():
        print(f"{loai}: {so_luong} đơn")

    return thong_ke


def bieu_do_thong_ke():
    """
    hàm vẽ biểu đồ
    """
    thong_ke = thong_ke_phan_hang()

    labels = list(thong_ke.keys())
    values = list(thong_ke.values())

    if sum(values) == 0:
        print("Không có dữ liệu để vẽ biểu đồ!")
        return
    
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Thống kê số lượng đơn theo phân hạng")
    plt.show()


def luu_du_lieu():
    """
    lưu dữ liệu lại vào file
    """
    global hotels
    if not hotels:
        print("Không có dữ liệu để lưu!")
        return

    fieldnames = []
    for h in hotels:
        for k in h.keys():
            if k not in fieldnames:
                fieldnames.append(k)

    with open("data.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in hotels:
            writer.writerow(row)

    print("Đã lưu dữ liệu vào data.csv")


while True:
    in_menu()
    choice = int(input("Chọn chức năng: "))
    if choice == 0:
        print("Tạm biệt!")
        break
    elif choice == 1:
        lay_du_lieu()
        in_danh_sach_don()
    elif choice == 2:
        them_don_dat_phong()
    elif choice == 3:
        cap_nhat_don()
    elif choice == 4:
        xoa_don()
    elif choice == 5:
        tim_phong()
    elif choice == 6:
        sap_xep_phong()
    elif choice == 7:
        thong_ke_phan_hang()
    elif choice == 8:
        bieu_do_thong_ke()
    elif choice == 9:
        luu_du_lieu()
