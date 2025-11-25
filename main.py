# main.py
import streamlit as st
import json
import os
from datetime import datetime, time, date

DATA_FILE = "data.json"

st.set_page_config(page_title="연타로 상담일지", layout="wide")

# --- pastel 스타일 ---
st.markdown(
    """
    <style>
    .main > div {
        background: linear-gradient(180deg, #fffaf0, #f7fbff);
        border-radius: 12px;
        padding: 18px;
    }
    .card {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
    }
    .title {
        font-size:30px;
        font-weight:700;
        color:#5a5a5a;
    }
    .small-muted { color:#6b6b6b; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div style="display:flex;justify-content:space-between;align-items:center">', unsafe_allow_html=True)
st.markdown('<div><span class="title">연타로 상담일지</span><div class="small-muted">🎴🍡🗾 - 타로 / 사주 기록을 한눈에</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:14px">💠 디자인: 파스텔 톤 · 귀여운 일본 이모지</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 데이터 로드/저장 ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# --- 내담자 입력 ---
st.header("내담자 정보 입력 / 불러오기 🧾")
col1, col2, col3, col4 = st.columns([2,2,1,1])
with col1:
    name = st.text_input("이름")
with col2:
    birth = st.date_input("생년월일")
with col3:
    gender = st.selectbox("성별", ["여", "남", "기타"])
with col4:
    birth_time = st.time_input("태어난 시간", value=time(12,0))

if name.strip() == "":
    st.info("내담자 이름을 입력하세요.")
else:
    client_key = f"{name}|{birth.isoformat()}|{gender}|{birth_time.strftime('%H:%M')}"
    if st.button("내담자 불러오기 / 등록"):
        if client_key not in data:
            data[client_key] = {
                "meta": {
                    "name": name,
                    "birth": birth.isoformat(),
                    "gender": gender,
                    "birth_time": birth_time.strftime("%H:%M"),
                    "created_at": datetime.now().isoformat()
                },
                "records": []
            }
            save_data(data)
            st.success("신규 내담자 등록됨 ✅")
        else:
            st.success("내담자 정보 로드됨 ✅")

# --- 상담 기록 추가 섹션 ---
st.header("상담 기록 추가 ✍️")
if name.strip() != "":
    st.markdown("**상담 유형 선택** (규칙: 1=타로, 2=사주, 3=사주+타로)")
    type_map = {"1":"타로", "2":"사주", "3":"사주 + 타로"}
    type_choice = st.radio("상담 유형", options=["1","2","3"], format_func=lambda x: f"{x} — {type_map[x]}")
    session_date = st.date_input("상담 날짜", value=date.today())
    session_time = st.time_input("상담 시간", value=datetime.now().time())
    session_text = st.text_area("상담 내용 입력 (메모 / 해석 / 주의사항 등)", height=180, placeholder="클라이언트에게 전할 말, 카드/사주 해석 메모 등")
    save_col1, save_col2 = st.columns([1,1])
    with save_col1:
        if st.button("상담 기록 저장 💾"):
            record = {
                "type": type_choice,
                "type_label": type_map[type_choice],
                "date": session_date.isoformat(),
                "time": session_time.strftime("%H:%M"),
                "content": session_text,
                "saved_at": datetime.now().isoformat()
            }
            # ensure client exists
            if client_key not in data:
                data[client_key] = {
                    "meta": {
                        "name": name,
                        "birth": birth.isoformat(),
                        "gender": gender,
                        "birth_time": birth_time.strftime("%H:%M"),
                        "created_at": datetime.now().isoformat()
                    },
                    "records": []
                }
            data[client_key]["records"].append(record)
            save_data(data)
            st.success("상담 기록이 저장되었습니다.")
    with save_col2:
        if st.button("기록 초기화(입력란 비우기)"):
            # trivial: just rerun with empty inputs
            st.experimental_rerun()
else:
    st.info("내담자 이름을 먼저 입력하고 '내담자 불러오기 / 등록' 버튼을 눌러주세요.")

# --- 내담자 목록 및 누가기록(고객관리) ---
st.header("고객 관리 · 누가기록 📚")
if len(data) == 0:
    st.info("등록된 내담자가 없습니다.")
else:
    # summary list
    keys = list(data.keys())
    # show selectbox of clients
    client_display = [f"{data[k]['meta']['name']} | {data[k]['meta']['birth']} | {data[k]['meta']['gender']} | {data[k]['meta']['birth_time']}" for k in keys]
    sel = st.selectbox("내담자 선택", options=range(len(keys)), format_func=lambda i: client_display[i])
    sel_key = keys[sel]
    client = data[sel_key]
    meta = client["meta"]
    st.markdown(f"**{meta['name']}** · {meta['birth']} · {meta['gender']} · 태생시 {meta['birth_time']}")
    st.write("등록일:", meta.get("created_at","-"))

    # show records sorted by date desc
    records = client.get("records", [])
    if not records:
        st.info("이 내담자의 상담 기록이 없습니다.")
    else:
        # sort by date + time
        def rec_key(r):
            try:
                return datetime.fromisoformat(r.get("date")+"T"+r.get("time"))
            except:
                return datetime.fromisoformat(r.get("saved_at"))
        records_sorted = sorted(records, key=rec_key, reverse=True)
        for idx, r in enumerate(records_sorted):
            with st.expander(f"{r['date']} {r['time']} · {r['type_label']}"):
                st.markdown(f"- **유형:** {r['type_label']}")
                st.markdown(f"- **저장일:** {r.get('saved_at','-')}")
                st.markdown("**상담 내용**")
                st.write(r.get("content","(내용 없음)"))
                col_a, col_b = st.columns([1,1])
                with col_a:
                    if st.button(f"삭제 — {idx}", key=f"del_{sel_key}_{idx}"):
                        # remove by matching saved_at & date/time/content
                        try:
                            # find in original list and remove the first matching
                            orig = data[sel_key]["records"]
                            for i_item, item in enumerate(orig):
                                if item.get("saved_at") == r.get("saved_at") and item.get("date")==r.get("date") and item.get("time")==r.get("time"):
                                    orig.pop(i_item)
                                    save_data(data)
                                    st.success("기록 삭제됨")
                                    st.experimental_rerun()
                            st.warning("삭제할 항목을 찾지 못했습니다.")
                        except Exception as e:
                            st.error("삭제 중 오류가 발생했습니다.")
                with col_b:
                    if st.button(f"복사해서 새 기록 만들기 — {idx}", key=f"dup_{sel_key}_{idx}"):
                        # duplicate the record and save with current timestamp
                        new = r.copy()
                        new["saved_at"] = datetime.now().isoformat()
                        data[sel_key]["records"].append(new)
                        save_data(data)
                        st.success("기록 복사 저장됨")
                        st.experimental_rerun()

# --- 하단 도움말 ---
st.markdown("---")
st.markdown("**주의**: 이 앱은 로컬 `data.json` 파일에 간단히 저장합니다. 배포 환경에 따라 파일 저장 방식이 다를 수 있습니다. 서버에 여러 사용자가 동시에 쓰는 경우 별도 DB를 권장합니다.")
st.markdown("이모지: 🎴(타로) 🍡(일본간식) 🗾(일본) 🎎(인형) 🫖(차)")

