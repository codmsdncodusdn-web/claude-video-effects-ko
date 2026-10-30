#!/usr/bin/env python3
"""Find when each word is said, so effects can land on the right word.

usage: python words.py input.mp4            -> prints "12.34  word" lines and saves input.words.json
Uses faster-whisper (installed into the skill's .venv on first run). On a Mac with mlx-whisper installed, that is used instead.

기본 언어는 한국어(WHISPER_LANG=ko), 기본 모델은 small(WHISPER_MODEL).
영어 영상이면 WHISPER_LANG=en, 언어 자동 감지는 WHISPER_LANG=auto.
"""
import json, os, subprocess, sys

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

src = sys.argv[1]
out = os.path.splitext(src)[0] + '.words.json'
lang = os.environ.get('WHISPER_LANG', 'ko').strip().lower()
lang = None if lang in ('', 'auto') else lang
words = []
try:
    import mlx_whisper
    r = mlx_whisper.transcribe(src, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', word_timestamps=True, language=lang)
    words = [{'w': w['word'].strip(), 's': round(w['start'], 2), 'e': round(w['end'], 2)} for seg in r['segments'] for w in seg.get('words', [])]
except ImportError:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print('받아쓰기 도구를 설치하는 중입니다 (처음 한 번, 약 1분)...', flush=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'faster-whisper'], check=True)
        from faster_whisper import WhisperModel
    import numpy as np
    # 소리는 ffmpeg로 직접 뽑아 넘긴다: PyAV 버전 차이와 윈도우 한글 경로 문제를 피한다
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    model = WhisperModel(os.environ.get('WHISPER_MODEL', 'small'), device='cpu', compute_type='int8')
    segs, _ = model.transcribe(audio, word_timestamps=True, vad_filter=True, language=lang)
    words = [{'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)} for s in segs for w in (s.words or [])]

json.dump(words, open(out, 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
for w in words: print(f"{w['s']:7.2f}  {w['w']}")
print(f'\n{len(words)}개 단어를 {out} 에 저장했습니다')
