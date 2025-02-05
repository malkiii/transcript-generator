from typing import List, Dict


def format_timestamp(seconds: float, srt: bool = False) -> str:
    """Converts seconds to timestamp format (HH:MM:SS,sss for VTT, HH:MM:SS.sss for SRT)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{secs:06.3f}"
    return formatted_time.replace(".", ",") if srt else formatted_time


def transcript_to_vtt(transcripts: List[Dict[str, object]]) -> str:
    """Converts a list of transcript entries to WebVTT format."""
    vtt_lines = ["WEBVTT", ""]  # Start with WEBVTT header

    for i, entry in enumerate(transcripts, start=1):
        start_time = format_timestamp(entry["timestamp"][0])
        end_time = format_timestamp(entry["timestamp"][1])
        text = entry["text"].strip()

        vtt_lines.append(f"{start_time} --> {end_time}")
        vtt_lines.append(text)
        vtt_lines.append("")  # Blank line between entries

    return "\n".join(vtt_lines)


def transcript_to_srt(transcripts: List[Dict[str, object]]) -> str:
    """Converts a list of transcript entries to SubRip Subtitle (SRT) format."""
    srt_lines = []

    for i, entry in enumerate(transcripts, start=1):
        start_time = format_timestamp(entry["timestamp"][0], srt=True)
        end_time = format_timestamp(entry["timestamp"][1], srt=True)
        text = entry["text"].strip()

        srt_lines.append(str(i))  # Index
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")  # Blank line between entries

    return "\n".join(srt_lines)


if __name__ == "__main__":
    transcripts = [
        {"timestamp": [0.0, 2.5], "text": "Hello, world!"},
        {"timestamp": [3.0, 5.0], "text": "This is a test."},
    ]

    vtt_output = transcript_to_vtt(transcripts)
    srt_output = transcript_to_srt(transcripts)

    print("WebVTT format:")
    print(vtt_output)

    print("\nSRT format:")
    print(srt_output)
