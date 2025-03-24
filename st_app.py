import streamlit as st
import time
import base64
import random
from PIL import Image, ImageDraw, ImageFont
import io

# Function to set background
def set_bg(local_img_path):
    with open(local_img_path, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded_img}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background using relative path
set_bg("locals/backgroundaileenhori.jpg")

# Function to play audio
def play_audio(audio_file):
    with open(audio_file, "rb") as file:
        audio_bytes = file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Function to slot machine

if "slot_attempts" not in st.session_state:
    st.session_state.slot_attempts = 0
if "slot_won" not in st.session_state:
    st.session_state.slot_won = False

def slot_machine():
    st.session_state.slot_attempts += 1
    emojis = ["🎊", "🎂", "🎈", "🎁", "🎉"]
    
    # On the 5th try, if not won yet, force jackpot
    if st.session_state.slot_attempts == 5 and not st.session_state.slot_won:
        result = ["🎊", "🎊", "🎊"]
        st.session_state.slot_won = True
    else:
        result = [random.choice(emojis) for _ in range(3)]
        if all(e == "🎊" for e in result):
            st.session_state.slot_won = True
    
    st.markdown(f"<div style='text-align: center; font-size: 80px;'>{''.join(result)}</div>", unsafe_allow_html=True)
    
    if all(e == "🎊" for e in result):
        st.balloons()
        st.success("🎊 JACKPOT! You got all three! 🎊")
        st.markdown("""
            <div style="text-align: center;">
                <img src="https://images.thortful.com/cdn-cgi/image/width=600,format=auto,quality=90/card/64f9af007d1bd41bf6aaf0ce/64f9af007d1bd41bf6aaf0ce_medium.jpg?version=1" width="300">
            </div>
        """, unsafe_allow_html=True)
        st.session_state.slot_attempts = 0  # reset attempts after success
    else:
        st.info(f"Skill issue! Aura points lost: {st.session_state.slot_attempts*100}")

st.markdown("<div style='text-align: center;'><h2>🎰 Birthday Slot Machine 🎰</h2></div>", unsafe_allow_html=True)
if st.button("Go on, Gamble!"):
    slot_machine()


# Function to scramble message
def scramble_message(message):
    return ''.join(random.sample(message, len(message)))

# Function to create an image with text on a local background image
def create_gift_image(text):
    bg_path = "locals/bgforgift.jpg"
    bg_image = Image.open(bg_path).convert("RGBA")

    img = bg_image.resize((300, 600))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("locals/arial.ttf", 28)  # Local font file
    except:
        font = ImageFont.load_default()  # fallback
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255), font=font)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

# Streamlit UI
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: yellow;">🎂 Happy Birthday! 🎉</h1>
        <p style="color: white;">Wishing you a year as cool as you!</p>
    </div>
    """, unsafe_allow_html=True)

# Confetti Button
if st.button("🎊 Release balloons!"):
    st.balloons()
    st.success("Woohoo! You're an adult now!!!")

# Display cake image
cake_img = Image.open("locals/cakeaileen.png")

img_buffer = io.BytesIO()
cake_img.save(img_buffer, format='PNG')
img_bytes = img_buffer.getvalue()
img_base64 = base64.b64encode(img_bytes).decode()

st.markdown(f"""
<div style="text-align: center;">
    <img src="data:image/png;base64,{img_base64}" width="300">
</div>
""", unsafe_allow_html=True)

if st.button("🎂 Blow the Candles!"):
    st.write("🎶 Playing Happy Birthday... 🎶")
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTBzZXl1ajd1b3g1MmphNHJkcTRkN2dmbG56a2JqanRzc3pwbnphYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8PsbWdOLFXXKCaMl2W/giphy.gif" width="300">
    </div>
    """, unsafe_allow_html=True)

    play_audio("locals/hbd_intrumental.mp3")
    time.sleep(2)

# Virtual cat
if st.button("reveal bday cat"):
    st.image("https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif", width=300)
    st.success("You are purrfect")

# Surprise Gift Box logic
if "selected_gift" not in st.session_state:
    st.session_state.selected_gift = None
if "slider_value" not in st.session_state:
    st.session_state.slider_value = 0

# Button to select gift phrase
if st.button("🎁 Guess the phrase"):
    gifts = [
        "bRoThEr", 
        "chhado", 
        "haule galla karo", 
        "ki pharak painda hai?", 
        "cOwBOy BeboP", 
        "JDJYDJYDYJDYJ LOVE YOUUUU",
        "GAMBLINGGGG",
        "babygurl",
        "Jazz. Heals."
    ]
    st.session_state.selected_gift = random.choice(gifts)
    st.session_state.slider_value = 0

# Phrase decoding interface
if st.session_state.selected_gift:
    st.markdown("""
        <div style="text-align: center;">
            <h2>🔍 Decode the AILEEN PHRASE!</h2>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.slider_value = st.slider(
        "Slide to decode!", 
        0, 5, st.session_state.slider_value
    )

    if st.session_state.slider_value < 5:
        random.seed(st.session_state.slider_value)
        scrambled_msg = scramble_message(st.session_state.selected_gift)
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{scrambled_msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: pink;'>{st.session_state.selected_gift}</div>", unsafe_allow_html=True)
        img_io = create_gift_image(st.session_state.selected_gift)

        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.image(img_io, caption="Aileen Says....", use_container_width=True, output_format="PNG")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
        """, unsafe_allow_html=True)
        st.download_button(label="📥 Download Your 'Aileen says...' Card now!", data=img_io, file_name="lil_gift.png", mime="image/png")
        st.markdown("</div>", unsafe_allow_html=True)


