# 🎙️ Transcript Generator App

This is a [Streamlit](https://streamlit.io/) application that generates transcripts from audio files. The application utilizes the OpenAI `whisper-large-v3-turbo` model for speech recognition to convert speech to text with common formats (.txt, .srt, .vtt) and high accuracy.

## Local Setup

1. Clone the repository using Git or Github CLI.

2. Create a virtual environment (Optional).

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Rename [secrets.example.toml](./.streamlit/secrets.example.toml) file to `secrets.toml` and add your streamlit [secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management).

5. Run the application by pressing the Run button if you're using the VSCode [Code Runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) extension, or manually using:
   ```sh
   python -m streamlit run streamlit_app.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
