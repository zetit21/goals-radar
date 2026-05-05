import streamlit as st
import pandas as pd

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Goals Radar Pro", layout="wide")

st.title("⚽ Goals Radar PRO: Deep Analysis")
st.markdown("### การวิเคราะห์สถิติเชิงลึกและคะแนนความน่าจะเป็น (Model 2026)")

# --- ข้อมูลเชิงลึก ---
data = {
    "League": ["Switzerland Super", "Norway Eliteserien", "Bundesliga", "Mexico Liga MX", "Premier League"],
    "GPG": [3.34, 3.22, 3.14, 3.10, 2.85],
    "Over_2_5_Rate": [68, 65, 62, 58, 55],  # % ที่เกิดสกอร์สูง 2.5
    "BTTS_Rate": [64, 61, 59, 56, 52],      # % ที่ยิงกันทั้งสองฝั่ง (Both Teams to Score)
    "Last_5_Trend": ["Up", "Stable", "Up", "Down", "Stable"],
    "Progress": [100, 11, 91, 100, 90]
}

df = pd.DataFrame(data)

# --- ส่วนบน: Metrics สำคัญ ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Top GPG League", f"{df.iloc[0]['League']}", f"{df.iloc[0]['GPG']}")
with col2:
    avg_gpg = df['GPG'].mean()
    st.metric("Market Avg GPG", f"{avg_gpg:.2f}")
with col3:
    st.metric("High Yield Target", "Switzerland", "Target Found", delta_color="normal")
with col4:
    st.metric("System Status", "Live Analysis", "Ready")

st.divider()

# --- ส่วนวิเคราะห์รายลีก (Deep Dive) ---
st.subheader("🔍 ระบบคำนวณคะแนนตัดสินใจ (Y/N Logic)")
selected_league = st.selectbox("เลือกลีกเพื่อประเมินความคุ้มค่า:", df['League'])

# ดึงข้อมูลของลีกที่เลือก
row = df[df['League'] == selected_league].iloc[0]

c1, c2 = st.columns([1, 2])

with c1:
    st.write(f"### {selected_league}")
    st.write(f"**GPG ปัจจุบัน:** {row['GPG']}")
    st.write(f"**อัตราสกอร์สูง (Over 2.5):** {row['Over_2_5_Rate']}%")
    st.write(f"**ทั้งสองทีมยิง (BTTS):** {row['BTTS_Rate']}%")

with c2:
    # --- ระบบคิดคะแนนแบบ Trader ---
    st.write("### 📝 System Scoring")
    
    score = 0
    # เงื่อนไข 1: GPG > 3.0
    cond1 = "Y" if row['GPG'] > 3.0 else "N"
    if cond1 == "Y": score += 40
    
    # เงื่อนไข 2: Over 2.5 Rate > 60%
    cond2 = "Y" if row['Over_2_5_Rate'] > 60 else "N"
    if cond2 == "Y": score += 30
    
    # เงื่อนไข 3: Trend
    cond3 = "Y" if row['Last_5_Trend'] == "Up" else "N"
    if cond3 == "Y": score += 30

    # แสดงผลตารางเงื่อนไข
    score_data = {
        "เงื่อนไข (Setup)": ["GPG > 3.0", "Over 2.5 > 60%", "Trend: Up"],
        "สถานะ (Y/N)": [cond1, cond2, cond3],
        "คะแนนที่ได้": [40 if cond1=="Y" else 0, 30 if cond2=="Y" else 0, 30 if cond3=="Y" else 0]
    }
    st.table(pd.DataFrame(score_data))

    # สรุปคะแนนสุดท้าย
    st.markdown(f"## Total Score: `{score}/100`")
    
    if score >= 70:
        st.success(f"✅ **Action: เล่น (Confirm Setup)** - คะแนน {score} ถึงเกณฑ์ที่กำหนด")
    elif score >= 40:
        st.warning(f"⏳ **Action: รอ (Wait)** - คะแนน {score} ยังไม่คมพอ ให้รอดูราคาไหล")
    else:
        st.error(f"❌ **Action: ไม่เล่น (Skip)** - คะแนน {score} ต่ำเกินไป ไม่เข้าเงื่อนไข")

st.divider()

# --- ตารางเปรียบเทียบภาพรวม ---
st.subheader("📊 League Comparison Table")
st.dataframe(df.style.highlight_max(subset=['GPG', 'Over_2_5_Rate'], color='#2E7D32'), use_container_width=True)

st.caption("หมายเหตุ: ข้อมูลนี้จัดทำขึ้นเพื่อการวิเคราะห์สถิติเชิงปริมาณ (Quantitative Analysis) เท่านั้น")
