import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CẤU HÌNH TEMPLATE (Sếp sửa nội dung ở đây) ---
TEMPLATES = {
    "Gói Cơ Bản (Link Drive A)": {
        "subject": "Cảm ơn bạn đã mua Gói Cơ Bản - Đây là sản phẩm của bạn",
        "body": """
        Chào bạn,
        
        Cảm ơn bạn đã thanh toán đơn hàng.
        Đây là link tải sản phẩm Gói Cơ Bản của bạn:
        
        LINK: https://drive.google.com/drive/folders/xxxxx
        
        Nếu có vấn đề gì hãy liên hệ lại mình nhé.
        Sếp Trung.
        """
    },
    "Gói Nâng Cao (Link Drive B)": {
        "subject": "Sản phẩm Gói Nâng Cao của bạn đã sẵn sàng",
        "body": """
        Chào bạn,
        
        Mình xác nhận đã nhận được chuyển khoản.
        Gửi bạn link tải trọn bộ Gói Nâng Cao:
        
        LINK: https://drive.google.com/drive/folders/yyyyy
        
        Chúc bạn một ngày tốt lành!
        Sếp Trung.
        """
    },
    "Gói VIP (Link Drive C)": {
        "subject": "[VIP] Link tải sản phẩm độc quyền",
        "body": """
        Hi VIP member,
        
        Cảm ơn bạn đã tin tưởng. Dưới đây là link tải riêng tư:
        
        LINK: https://drive.google.com/drive/folders/zzzzz
        
        Vui lòng không chia sẻ link này ra ngoài nhé.
        Sếp Trung.
        """
    }
}

# --- HÀM GỬI EMAIL ---
def send_email(to_email, template_key, gmail_user, gmail_password):
    try:
        # Lấy thông tin template
        selected_template = TEMPLATES[template_key]
        subject = selected_template["subject"]
        body_content = selected_template["body"]

        # Thiết lập email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body_content, 'plain'))

        # Kết nối tới Server Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()
        return True, "Đã gửi thành công!"
    except Exception as e:
        return False, str(e)

# --- GIAO DIỆN NGƯỜI DÙNG (UI) ---
st.set_page_config(page_title="Tool Gửi Hàng Sếp Trung", page_icon="📩")

st.title("📩 Tool Gửi Hàng Nhanh")
st.write("Dành riêng cho Sếp Trung - Chỉ cần nhập mail và chọn gói.")

# Form nhập liệu
with st.form("email_form"):
    customer_email = st.text_input("Email Khách Hàng", placeholder="nguoi_mua@gmail.com")
    
    # Dropdown chọn loại template
    option = st.selectbox(
        "Khách mua gói nào?",
        list(TEMPLATES.keys())
    )
    
    # Nút gửi
    submitted = st.form_submit_button("Gửi Hàng Ngay 🚀")

    if submitted:
        if not customer_email:
            st.error("⚠️ Sếp quên nhập Email khách rồi!")
        elif "@" not in customer_email:
             st.error("⚠️ Email không hợp lệ nha Sếp!")
        else:
            # Lấy thông tin mật khẩu từ Secret (bảo mật)
            # Khi chạy trên máy cá nhân để test thì có thể thay trực tiếp vào đây, 
            # nhưng khi đưa lên mạng phải dùng st.secrets
            MY_EMAIL = st.secrets["GMAIL_USERNAME"]
            MY_PASSWORD = st.secrets["GMAIL_PASSWORD"]
            
            with st.spinner(f"Đang gửi gói '{option}' cho khách..."):
                success, message = send_email(customer_email, option, MY_EMAIL, MY_PASSWORD)
            
            if success:
                st.success(f"✅ {message} - Đã gửi cho {customer_email}")
                st.balloons() # Hiệu ứng bóng bay chúc mừng
            else:
                st.error(f"❌ Lỗi rồi Sếp ơi: {message}")