from datetime import datetime, timedelta, time
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="최적 수면 시간 계산기", page_icon="🌙", layout="centered"
)

st.title("🌙 최적 수면/취침 시간 계산기")
st.markdown("""
사람의 수면 주기는 평균 **약 90분**입니다.  
수면 주기가 끝나는 시점(렘수면 또는 얕은 수면)에 맞춰 깨어나면 **피로감이 훨씬 적고 상쾌하게** 일어날 수 있습니다.
""")

st.divider()

# 사이드바: 수면 설정 변경 가능
st.sidebar.header("⚙️ 수면 환경 설정")
cycle_minutes = st.sidebar.number_input(
    "1회 수면 주기 (분)", min_value=60, max_value=120, value=90, step=5
)
latency_minutes = st.sidebar.number_input(
    "잠드는 데 걸리는 시간 (분)",
    min_value=0,
    max_value=60,
    value=15,
    step=5,
)

# 탭 구성 (기상시간 기준 vs 지금 잘 때 기준)
tab1, tab2 = st.tabs(
    ["⏰ 목표 기상 시간으로 취침 시간 찾기", "🛌 지금 잘 때 기상 시간 찾기"]
)

# [탭 1] 목표 기상 시간 기준 취침 시간 계산
with tab1:
    st.subheader("일어나고 싶은 시간을 입력하세요")
    target_time = st.time_input("목표 기상 시간", value=time(7, 0))

    if st.button("추천 취침 시간 계산", type="primary", key="btn_target"):
        today = datetime.now().date()
        target_dt = datetime.combine(today, target_time)

        st.write("---")
        st.subheader("💡 추천 취침 시간 (침대에 눕는 시간)")
        st.caption(
            f"※ 침대에 누워 잠들기까지 약 **{latency_minutes}분**이 소요되는 점이 반영되었습니다."
        )

        # 수면 주기 (6회 ~ 3회)
        cycles_info = [
            (6, "9시간 수면", "🟢 충분한 휴식"),
            (5, "7.5시간 수면", "🌟 가장 추천"),
            (4, "6시간 수면", "🟡 적정 수면"),
            (3, "4.5시간 수면", "🔴 최소 수면"),
        ]

        cols = st.columns(2)
        for idx, (cycles, sleep_desc, badge) in enumerate(cycles_info):
            total_sleep_min = cycles * cycle_minutes
            # (목표 시간) - (총 수면 시간 + 입면 시간)
            bedtime_dt = target_dt - timedelta(
                minutes=total_sleep_min + latency_minutes
            )

            # 시간 포맷팅 (오전/오후 표시)
            time_str = (
                bedtime_dt.strftime("%p %I:%M")
                .replace("AM", "오전")
                .replace("PM", "오후")
            )

            with cols[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"### {time_str}")
                    st.markdown(f"**{badge}**")
                    st.text(f"• {sleep_desc}")
                    st.text(
                        f"• {cycles}주기 ({total_sleep_min // 60}시간 {total_sleep_min % 60}분)"
                    )

# [탭 2] 지금 잘 때 기준 기상 시간 계산
with tab2:
    st.subheader("지금 잠들면 몇 시에 일어나는 게 좋을까요?")

    if st.button("추천 기상 시간 계산", type="primary", key="btn_now"):
        now_dt = datetime.now()
        now_str = (
            now_dt.strftime("%p %I:%M")
            .replace("AM", "오전")
            .replace("PM", "오후")
        )

        st.write("---")
        st.subheader("💡 추천 기상 시간")
        st.caption(f"※ 지금({now_str}) 누워서 계산된 시간입니다.")

        cycles_info = [
            (3, "4.5시간 수면", "🔴 최소 수면"),
            (4, "6시간 수면", "🟡 적정 수면"),
            (5, "7.5시간 수면", "🌟 가장 추천"),
            (6, "9시간 수면", "🟢 충분한 휴식"),
        ]

        cols = st.columns(2)
        for idx, (cycles, sleep_desc, badge) in enumerate(cycles_info):
            total_sleep_min = cycles * cycle_minutes
            wake_dt = now_dt + timedelta(
                minutes=total_sleep_min + latency_minutes
            )

            time_str = (
                wake_dt.strftime("%p %I:%M")
                .replace("AM", "오전")
                .replace("PM", "오후")
            )

            with cols[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"### {time_str}")
                    st.markdown(f"**{badge}**")
                    st.text(f"• {sleep_desc}")
                    st.text(
                        f"• {cycles}주기 ({total_sleep_min // 60}시간 {total_sleep_min % 60}분)"
                    )
