import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Video Downloader", page_icon="📥", layout="centered")

st.title("📥 YouTube Video Downloader")
st.write("Download YouTube videos in best quality (video + audio merged).")

url = st.text_input("🎥 Enter YouTube Video URL")

download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

if st.button("⬇️ Download Video"):
    if not url:
        st.error("Please enter a valid YouTube URL.")
    else:
        st.info("Downloading... Please wait ⏳")

        ydl_opts = {
            "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "quiet": True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # If merged into mp4, fix extension
                if filename.endswith(".webm") or filename.endswith(".mkv"):
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

            st.success("✅ Download completed!")

            with open(filename, "rb") as file:
                st.download_button(
                    label="📂 Click here to Download File",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
