import os
import toml
import requests
import streamlit as st
from base64 import b64encode
from transcript_formatter import transcript_to_srt, transcript_to_vtt

# Load secrets based on environment
if os.getenv("ENV") == "production":
    secrets = st.secrets
else:
    secrets = toml.load(".streamlit/secrets.toml")


def transcribe_audio(audio_data, return_timestamps=False):
    try:
        headers = {"Authorization": f"Bearer {secrets["HUGGINGFACE_TOKEN"]}"}
        payload = {
            "inputs": b64encode(audio_data).decode("utf-8"),
            "parameters": {"return_timestamps": return_timestamps},
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo",
            headers=headers,
            json=payload,
        )

        data = response.json()

        return data["chunks"] if return_timestamps else data["text"]
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


def main():
    # Set page metadata
    st.set_page_config(
        page_title="Transcript Generator",
        page_icon="🎙️",
        layout="centered",
    )

    # App title and description
    st.title("🎙️ Transcript Generator")
    st.write("Upload a video/audio file or provide a URL to generate a transcript.")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a video or audio file",
        type=["mp3", "wav", "mp4", "m4a"],
        accept_multiple_files=False,
    )

    OUTPUT_FORMATS = [
        "Plain Text (.txt)",
        "SubRip Subtitle (.srt)",
        "WebVTT (.vtt)",
    ]

    # Create columns for layout alignment
    col1, col2 = st.columns([3, 1])  # Adjust ratios as needed

    with col1:
        output_format = st.selectbox("Select output format", OUTPUT_FORMATS, index=0)

    with col2:
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

        # Use session state to control button disable state
        button_key = "gen_btn"
        if button_key in st.session_state and st.session_state[button_key] == True:
            st.session_state.generating = True
        else:
            st.session_state.generating = False

        generate_button = st.button(
            "Generate",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.generating,
            key=button_key,
        )

    if "transcript" not in st.session_state:
        st.session_state.file_name = None
        st.session_state.transcript = None
        st.session_state.format = None

    if generate_button:
        # Process the uploaded file
        if uploaded_file is not None:
            file_name = uploaded_file.name
            audio_data = uploaded_file.getvalue()

            with st.spinner("📝 Generating transcript..."):
                # Perform transcription if we have audio data
                transcript = transcribe_audio(
                    audio_data,
                    output_format != OUTPUT_FORMATS[0],
                )

            if transcript is not None:
                # Format the transcript based on the selected output format
                if output_format == OUTPUT_FORMATS[1]:
                    transcript = transcript_to_srt(transcript)
                    file_extension = "srt"
                elif output_format == OUTPUT_FORMATS[2]:
                    transcript = transcript_to_vtt(transcript)
                    file_extension = "vtt"
                else:
                    file_extension = "txt"

                # Store the transcript and format in session state
                st.session_state.file_name = file_name
                st.session_state.transcript = transcript
                st.session_state.format = file_extension

        st.rerun()

    if st.session_state.transcript is not None:
        st.success("✅ Transcription complete!")

        if st.session_state.format == "txt":
            container = st.container(border=True)
            container.write(st.session_state.transcript)
        else:
            # Download button
            st.download_button(
                label=f"⬇️ Download Transcript ({st.session_state.format.upper()})",
                file_name=f"{st.session_state.file_name}_transcript.{st.session_state.format}",
                mime="text/plain",
                data=st.session_state.transcript,
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
