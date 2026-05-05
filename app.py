import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอ Dashboard
st.set_page_config(page_title="Goals Radar App", layout="wide")

st.title("⚽ Goals Radar: League Goal Ranking")
st.markdown("### สถิติลีกจอมถล่มประตู (ข้อมูลล่าสุด 2026)")

# ข้อมูลลีกที่คุณเลือก
data = {
    "League": ["Switzerland Super League", "Norway Eliteserien", "Bundesliga", "Mexico Liga MX", "Premier League"],
    "Flag": ["🇨🇭", "🇳🇴", "🇩🇪", "🇲🇽", "🏴󠁧󠁢󠁥󠁮󠁧󠁿"],
    "GPG": [3.34, 3.22, 3.14, 3.10, 2.85],
    "Progress": [100, 11, 91, 100, 90],
    "Status": ["จบฤดูกาล", "เพิ่งเริ่ม", "โค้งสุดท้าย", "จบช่วงแรก", "ทรงตัว"]
}

df = pd.DataFrame(data)
df = df.sort_values(by="GPG", ascending=False)

# แสดงผล Ranking แบบ Metric สวยๆ
cols = st.columns(len(df))
for index, row in df.iterrows():
    with cols[list(df.index).index(index)]:
        st.metric(label=f"{row['Flag']} {row['League']}", value=f"{row['GPG']} GPG")
        st.progress(row['Progress'] / 100)
        st.caption(f"ความคืบหน้า: {row['Progress']}% | {row['Status']}")

st.divider()

# ส่วนเลือกดูรายละเอียดที่คุยกันเรื่อง "ปัจจัยเปิดหน้าแลก"
st.subheader("🔍 วิเคราะห์ปัจจัยการทำประตู")
selected_league = st.selectbox("เลือกลีกที่สนใจดูเงื่อนไขเปิดเกมบุก:", df['League'])

if selected_league == "Bundesliga":
    st.info("💡 **ปัจจัยบุกแหลก:** เน้น High Line Defense และการแย่งพื้นที่ยุโรปในช่วงท้ายฤดูกาล")
    st.write("**ทีมแนะนำ:** Bayern Munich, RB Leipzig")
elif selected_league == "Norway Eliteserien":
    st.warning("☀️ **ปัจจัยบุกแหลก:** เป็นช่วงต้นฤดูกาล ทีมยังฟิตและเน้นเกมบุกเพื่อสร้าง Momentum")
    st.write("**ทีมแนะนำ:** Bodo/Glimt, Molde")
else:
    st.write("ตรวจสอบสถิติเชิงลึกได้เร็วๆ นี้...")
