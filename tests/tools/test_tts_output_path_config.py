"""text_to_speech must honor the configured ``tts.output_path``.

The default output dir (``DEFAULT_OUTPUT_DIR``) is used only when
``tts.output_path`` is unset or empty. This source-level check mirrors the
microsecond-timestamp regression test (``test_tts_output_timestamp.py``) and
avoids a network synthesis call.
"""

import inspect

from tools import tts_tool


def test_both_tts_entry_points_honor_configured_output_path():
    """``output_path`` config is respected at both synthesis entry points."""
    src = inspect.getsource(tts_tool)
    marker = 'tts_config.get("output_path") or DEFAULT_OUTPUT_DIR'
    # The config-honoring expression must appear in both ``_text_to_speech_single``
    # and ``text_to_speech_tool``.
    assert src.count(marker) == 2, (
        "TTS output directory must respect tts.output_path at both entry points"
    )


def test_empty_configured_output_path_falls_back_to_default():
    """An empty ``tts.output_path`` falls back to the default dir, not '.'."""
    src = inspect.getsource(tts_tool)
    # `or DEFAULT_OUTPUT_DIR` guards against an explicitly-empty string so the
    # tool never writes to the current working directory.
    assert 'tts_config.get("output_path") or DEFAULT_OUTPUT_DIR' in src
