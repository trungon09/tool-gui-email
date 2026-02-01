import streamlit as st
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CẤU HÌNH SẢN PHẨM (MỖI SẢN PHẨM LÀ 1 DANH SÁCH 2 FOLDER) ---
PRODUCTS = {
    "Full bộ 50 Preset Mobile & PC": [
        {
            "name": "Preset DNG (Dành cho điện thoại)",
            "folder_id": "1ty9bxR7P6VEXSJxeeSFYpWdexNnCwkgS", 
            "link": "https://drive.google.com/drive/folders/1ty9bxR7P6VEXSJxeeSFYpWdexNnCwkgS?usp=sharing"
        },
        {
            "name": "Preset XMP (Dành cho máy tính)",
            "folder_id": "1Qv2oGjYDa2X0RkxHqapwt1z-y8nP7ChG",
            "link": "https://drive.google.com/file/d/1Qv2oGjYDa2X0RkxHqapwt1z-y8nP7ChG/view?usp=sharing"
        }
    ],
    "Bộ 36 Preset Best seller Mobile & PC": [
        {
            "name": "Preset DNG (Dành cho điện thoại)",
            "folder_id": "1xaMdIzxfZYsmyC44Tjric4GUlgqje8sC",
            "link": "https://drive.google.com/drive/folders/1xaMdIzxfZYsmyC44Tjric4GUlgqje8sC?usp=sharing"
        },
        {
            "name": "Preset XMP (Dành cho máy tính)",
            "folder_id": "1bS_qEbU5UMr-zY01SB6aX8s2QEtiTGcp",
            "link": "https://drive.google.com/file/d/1bS_qEbU5UMr-zY01SB6aX8s2QEtiTGcp/view?usp=sharing"
        }
    ]
}

DISPLAY_NAME = "Trung's Preset" # Đã đổi theo yêu cầu

# --- CẤU HÌNH LINK TRONG NỘI DUNG MAIL ---
LINK_NOTE = "https://photos.app.goo.gl/xA2x3gRcLWKsXQMAA" # Link từ ảnh sếp
LINK_VIDEO_TIKTOK = "https://www.tiktok.com/@trung_lightroom/video/7385215457105562898?is_from_webapp=1&sender_device=pc&web_id=7177406567393134081" # Sếp điền link tiktok vào đây
LINK_VIDEO_HUONG_DAN_MOBILE = "https://www.tiktok.com/@trung_lightroom/video/7275748130144931074?" # Sếp điền link video mobile
LINK_VIDEO_HUONG_DAN_PC = "https://www.tiktok.com/@trung_lightroom/video/7570758078954605845?is_from_webapp=1&sender_device=pc&web_id=7177406567393134081" # Sếp điền link video PC

# --- HÀM 1: RA LỆNH ROBOT CẤP QUYỀN ---
def add_user_to_drive(customer_email, folder_id):
    try:
        key_dict = json.loads(st.secrets["GCP_JSON"])
        creds = service_account.Credentials.from_service_account_info(
            key_dict, scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=creds)

        user_permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': customer_email
        }
        
        service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            fields='id',
            sendNotificationEmail=False
        ).execute()
        return True, ""
    except Exception as e:
        return False, str(e)

# --- HÀM 2: TẠO NỘI DUNG HTML (CHUẨN FORM ẢNH) ---
def create_html_content(customer_email, product_items):
    # Tạo danh sách các thẻ Drive (Card)
    drive_cards_html = ""
    for item in product_items:
        drive_cards_html += f"""
        <div style="background-color: #f8f9fa; border: 1px solid #dadce0; border-radius: 8px; padding: 15px; margin-bottom: 10px; width: fit-content; min-width: 300px;">
            <div style="display: flex; align-items: center;">
                <img src="https://yt3.googleusercontent.com/eBkA-whuMHCHR3s1GCIKUdAloMVgohvvPBTufiIc0rPUd2AlyP4UeV52ubGAF76RIUqP8GFOAQ=s900-c-k-c0x00ffffff-no-rj" width="24" style="margin-right: 12px;">
                <div>
                    <div style="font-weight: 500; font-size: 14px; color: #202124;">{item['name']}</div>
                    <div style="font-size: 12px; color: #5f6368;">Google Drive • Đã cấp quyền cho {customer_email}</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #ececec;">
                <a href="{item['link']}" style="text-decoration: none; color: #1a73e8; font-weight: bold; font-size: 14px;">MỞ THƯ MỤC ➔</a>
            </div>
        </div>
        """

    # Nội dung Text y hệt trong ảnh Sếp gửi
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        
        {drive_cards_html}

        <p><strong>Cảm ơn bạn đã ủng hộ sản phẩm team mình!!!</strong></p>
        
        <p>Để chọn ảnh phù hợp với preset cũng như chỉnh lại thế nào cho hợp lý thì bạn đọc phần note trong từng preset ở đây nhe: 
        <a href="{LINK_NOTE}">Xem Note Hướng Dẫn</a></p>
        
        <p>Để sử dụng preset hiệu quả thì bạn cần có kiến thức chỉnh màu cơ bản vì vậy mình đang làm một chuỗi video hướng dẫn cách sử dụng các công cụ trong lightroom bạn có thể xem nó ở đây nhe: 
        <a href="{LINK_VIDEO_TIKTOK}">Tiktok Video</a></p>
        
        <p style="color: #673ab7;">Đối với mobile, bạn tải từng file trong mục Preset for mobile về rồi làm theo Video hướng dẫn đây nhe: 
        <a href="{LINK_VIDEO_HUONG_DAN_MOBILE}">Video hướng dẫn</a></p>
        
        <p style="color: #673ab7;">(Lưu ý: File có đuôi .zip là dành cho máy tính)<br>
        Video hướng dẫn cách cài PC: <a href="{LINK_VIDEO_HUONG_DAN_PC}">Click vào đây nhe</a></p>
        
        <p>Ngoài cung cấp preset thì:</p>
        <ul style="list-style-type: - ;">
            <li>Mình có nhận chỉnh màu theo yêu cầu với mức giá từ 25-80k tùy vào độ khó của màu.</li>
            <li>Hỗ trợ cài bản crack các app của adobe ( sử dụng vĩnh viễn ). Chi tiết liên hệ zalo: <strong>0762042093</strong>.</li>
            <li>Panel retouch ảnh.</li>
        </ul>

        <p>Nếu bạn có nhu cầu học chỉnh màu ảnh thì mình có thể giới thiệu bạn với chỗ lúc trước mình chỉnh màu (do mình giới thiệu sẽ được giảm học phí thêm nhe), khóa học sẽ dạy về công cụ trong lightroom, camera raw, cách phối màu, tư duy chỉnh màu ảnh, đây cũng đều là kiến thức nền tảng để giúp bạn chỉnh được mọi tone màu bạn muốn. Còn nếu bạn đã nắm chắc những phần đó rồi thì cũng sẽ có khóa nâng cao hơn để bạn học chỉnh màu chuyên sâu nhe, nếu cần thì liên hệ với mình qua số zalo trên nhé!!!</p>
        
        <br>
        <p>Trân trọng,<br>
        <strong>Trung's Preset</strong></p>
      </body>
    </html>
    """

def send_email(to_email, product_key, gmail_user, gmail_password):
    # Lấy danh sách các folder cần gửi (1 gói có thể có nhiều folder)
    product_items = PRODUCTS[product_key]
    
    # BƯỚC 1: CẤP QUYỀN DRIVE CHO TỪNG FOLDER
    # Chạy vòng lặp để cấp quyền cho cả Mobile và PC
    errors = []
    for item in product_items:
        success, msg = add_user_to_drive(to_email, item['folder_id'])
        if not success:
            errors.append(f"Lỗi folder {item['name']}: {msg}")
    
    # Nếu có lỗi cấp quyền thì dừng và báo ngay
    if errors:
        return False, " | ".join(errors)

    # BƯỚC 2: GỬI MAIL
    try:
        html_content = create_html_content(to_email, product_items)
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{DISPLAY_NAME} <{gmail_user}>"
        msg['To'] = to_email
        msg['Subject'] = f"Gửi bạn {product_key} - {DISPLAY_NAME}"
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()
        return True, "Thành công! Đã cấp quyền cả 2 folder & Gửi mail."
    except Exception as e:
        return False, f"Lỗi gửi mail: {str(e)}"

# --- GIAO DIỆN ---
st.set_page_config(page_title="Tool Gửi Preset", page_icon="📸")
st.title("📸 Tool Gửi Preset - Trung's Preset")

with st.form("email_form"):
    customer_email = st.text_input("Email Khách Hàng")
    option = st.selectbox("Chọn gói:", list(PRODUCTS.keys()))
    submitted = st.form_submit_button("Cấp Quyền & Gửi 🚀")

    if submitted:
        if not customer_email or "@" not in customer_email:
             st.error("⚠️ Email sai rồi Sếp!")
        else:
            with st.spinner(f"Đang xử lý gói '{option}' cho {customer_email}..."):
                MY_EMAIL = st.secrets["GMAIL_USERNAME"]
                MY_PASSWORD = st.secrets["GMAIL_PASSWORD"]
                success, message = send_email(customer_email, option, MY_EMAIL, MY_PASSWORD)
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")




