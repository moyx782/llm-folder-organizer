from llm_folder_organizer.extractor import read_preview


def test_read_preview_returns_empty_for_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    assert read_preview(missing, max_bytes=64, preview_chars=20) == ""


def test_read_preview_handles_binary_without_exception(tmp_path):
    binary_file = tmp_path / "data.bin"
    binary_file.write_bytes(b"\xff\xfe\x00\x01hello\x00world")

    preview = read_preview(binary_file, max_bytes=64, preview_chars=20)

    assert isinstance(preview, str)
