import numpy as np
import sounddevice as sd

def alert():
    # 오디오 데이터 생성
    fs = 44100  # 샘플링 레이트
    duration = 1  # 1초 동안
    frequency = 440  # A4 노트, 440 Hz
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)

    # 특정 장치로 출력
    sd.play(data, samplerate=fs, device=3)
    sd.wait()