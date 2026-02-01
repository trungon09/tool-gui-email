import streamlit as st
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CẤU HÌNH SẢN PHẨM ---
# folder_id: Là đoạn mã cuối link drive folder
PRODUCTS = {
    "Full bộ 50 Preset Mobile": {
        "folder_id": "1ty9bxR7P6VEXSJxeeSFYpWdexNnCwkgS", 
        "link": "https://drive.google.com/drive/folders/1ty9bxR7P6VEXSJxeeSFYpWdexNnCwkgS?usp=sharing",
        "subject": "Gửi bạn bộ 50 Preset Mobile - Trung Dinh"
    },
    "Bộ Full Presets PC": {
        "folder_id": "1Qv2oGjYDa2X0RkxHqapwt1z-y8nP7ChG",
        "link": "https://drive.google.com/file/d/1Qv2oGjYDa2X0RkxHqapwt1z-y8nP7ChG/view?usp=sharing",
        "subject": "Gửi bạn bộ Full Presets PC - Trung Dinh"
    }
}

DISPLAY_NAME = "Trung Dinh"
NOTE_LINK = "https://photos.app.goo.gl/LINK_NOTE"
VIDEO_LINK = "https://tiktok.com/LINK_VIDEO"

# --- HÀM 1: RA LỆNH ROBOT CẤP QUYỀN ---
def add_user_to_drive(customer_email, folder_id):
    try:
        # Lấy thông tin Robot từ Secrets
        key_dict = json.loads(st.secrets["GCP_JSON"])
        creds = service_account.Credentials.from_service_account_info(
            key_dict, scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=creds)

        # Cấu hình quyền: role='reader' (chỉ xem/tải), type='user'
        user_permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': customer_email
        }
        
        # Thực hiện lệnh add
        service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            fields='id',
        ).execute()
        return True, "Đã cấp quyền Drive"
    except Exception as e:
        return False, str(e)

# --- HÀM 2: GỬI MAIL (NHƯ CŨ) ---
def create_html_content(customer_name, product_name, drive_link):
    # (Giữ nguyên HTML template như bài trước cho gọn code)
    # Sếp copy lại đoạn HTML template ở bài trước dán vào đây nhé
    return f"""
    <html><body>
    <h3>Chào bạn, cảm ơn đã mua {product_name}</h3>
    <p>Mình đã cấp quyền truy cập cho email <b>{customer_name}</b>.</p>
    <a href="{drive_link}">BẤM VÀO ĐÂY ĐỂ TẢI</a>
    <br><br>
    <p>{DISPLAY_NAME}</p>
    </body></html>
    """

def send_email(to_email, product_key, gmail_user, gmail_password):
    product_info = PRODUCTS[product_key]
    
    # BƯỚC 1: CẤP QUYỀN DRIVE TRƯỚC
    drive_success, drive_msg = add_user_to_drive(to_email, product_info['folder_id'])
    
    if not drive_success:
        return False, f"Lỗi cấp quyền Drive: {drive_msg}"

    # BƯỚC 2: NẾU CẤP QUYỀN OK THÌ GỬI MAIL
    try:
        html_content = create_html_content(to_email, product_key, product_info['link'])
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{DISPLAY_NAME} <{gmail_user}>"
        msg['To'] = to_email
        msg['Subject'] = product_info['subject']
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()
        return True, "Thành công! Đã cấp quyền & Gửi mail."
    except Exception as e:
        return False, f"Lỗi gửi mail: {str(e)}"

# --- GIAO DIỆN ---
st.set_page_config(page_title="Tool Gửi Hàng VIP", page_icon="🔐")
st.title("🔐 Tool Gửi Hàng Bảo Mật")

with st.form("email_form"):
    customer_email = st.text_input("Email Khách Hàng")
    option = st.selectbox("Chọn gói:", list(PRODUCTS.keys()))
    submitted = st.form_submit_button("Cấp Quyền & Gửi 🚀")

    if submitted:
        if not customer_email or "@" not in customer_email:
             st.error("⚠️ Email sai rồi Sếp!")
        else:
            with st.spinner(f"Đang cấp quyền Drive cho {customer_email}..."):
                MY_EMAIL = st.secrets["GMAIL_USERNAME"]
                MY_PASSWORD = st.secrets["GMAIL_PASSWORD"]
                success, message = send_email(customer_email, option, MY_EMAIL, MY_PASSWORD)
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")
