# ---------------- FIX FOR PYTHON 3.13 STREAMLIT ERROR ----------------
from sys import getsizeof   # ✅ FIX (IMPORTANT)

import streamlit as st
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Rock Paper Scissors", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #38bdf8;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1e293b, #334155);
    color: white;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.score {
    font-size: 30px;
    font-weight: bold;
}
.result {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🎮 Rock Paper Scissors</div>', unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "scores" not in st.session_state:
    st.session_state.scores = {}

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Game Settings")

mode = st.sidebar.selectbox("Game Mode", ["Single Player", "Two Player", "Multi Player"])
target_score = st.sidebar.slider("Target Score", 1, 10, 5)

choices = ["Rock", "Paper", "Scissors"]
emoji = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}

# ---------------- GAME LOGIC ----------------
def winner(p1, p2):
    if p1 == p2:
        return "Draw"
    elif (p1 == "Rock" and p2 == "Scissors") or \
         (p1 == "Paper" and p2 == "Rock") or \
         (p1 == "Scissors" and p2 == "Paper"):
        return "P1"
    else:
        return "P2"

# ---------------- SINGLE PLAYER ----------------
if mode == "Single Player":
    name = st.text_input("Enter Your Name", "Player")
    user = st.selectbox("Choose", choices)

    if st.button("🎯 PLAY"):
        comp = random.choice(choices)

        st.markdown(f"<div class='result'>{emoji[user]} VS {emoji[comp]}</div>", unsafe_allow_html=True)

        res = winner(user, comp)

        if res == "Draw":
            st.info("🤝 Draw!")
            st.markdown("![draw](https://media.giphy.com/media/2HtWpp60NQ9CU/giphy.gif)")
        elif res == "P1":
            st.session_state.scores[name] = st.session_state.scores.get(name, 0) + 1
            st.markdown(f"<div class='result'>🎉 Congratulations {name}!</div>", unsafe_allow_html=True)
            st.markdown("![win](https://media.giphy.com/media/111ebonMs90YLu/giphy.gif)")
        else:
            st.session_state.scores["Computer"] = st.session_state.scores.get("Computer", 0) + 1
            st.markdown("<div class='result'>😢 Computer Wins! Try Again!</div>", unsafe_allow_html=True)
            st.markdown("![lose](https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif)")

# ---------------- TWO PLAYER ----------------
elif mode == "Two Player":
    p1_name = st.text_input("Player 1 Name", "Player 1")
    p2_name = st.text_input("Player 2 Name", "Player 2")

    p1 = st.selectbox("Player 1 Move", choices)
    p2 = st.selectbox("Player 2 Move", choices)

    if st.button("🎯 PLAY"):
        st.markdown(f"<div class='result'>{emoji[p1]} VS {emoji[p2]}</div>", unsafe_allow_html=True)

        res = winner(p1, p2)

        if res == "Draw":
            st.info("🤝 Draw!")

        elif res == "P1":
            st.session_state.scores[p1_name] = st.session_state.scores.get(p1_name, 0) + 1
            st.markdown(f"<div class='result'>🎉 {p1_name} Wins!</div>", unsafe_allow_html=True)
        else:
            st.session_state.scores[p2_name] = st.session_state.scores.get(p2_name, 0) + 1
            st.markdown(f"<div class='result'>🎉 {p2_name} Wins!</div>", unsafe_allow_html=True)

# ---------------- MULTI PLAYER ----------------
elif mode == "Multi Player":
    num = st.number_input("Players", 2, 5, 3)

    names = []
    moves = []

    for i in range(num):
        name = st.text_input(f"Player {i+1} Name", f"P{i+1}", key=f"name{i}")
        move = st.selectbox(f"{name} Move", choices, key=f"move{i}")
        names.append(name)
        moves.append(move)

    if st.button("🎯 PLAY"):
        for i in range(num):
            for j in range(i+1, num):
                res = winner(moves[i], moves[j])

                if res == "P1":
                    st.session_state.scores[names[i]] = st.session_state.scores.get(names[i], 0) + 1
                    st.write(f"🏆 {names[i]} beats {names[j]}")
                elif res == "P2":
                    st.session_state.scores[names[j]] = st.session_state.scores.get(names[j], 0) + 1
                    st.write(f"🏆 {names[j]} beats {names[i]}")
                else:
                    st.write(f"{names[i]} vs {names[j]} → Draw")

# ---------------- SCORE BOARD ----------------
st.markdown("## 🏆 Score Board")

cols = st.columns(3)

for i, (player, score) in enumerate(st.session_state.scores.items()):
    cols[i % 3].markdown(
        f"<div class='card'><h4>{player}</h4><div class='score'>{score}</div></div>",
        unsafe_allow_html=True
    )

# ---------------- MATCH WINNER ----------------
for player, score in st.session_state.scores.items():
    if score >= target_score:
        st.balloons()
        st.success(f"🎉 {player} WON THE MATCH!")
        st.session_state.scores = {}
        break
