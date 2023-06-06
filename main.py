import wave
import os
import time
import threading
import tkinter
import pyaudio

class VoiceRecorder():

    def __init__(self): # при создание экземпляра класса происходит создание интерфейса
        self.root = tkinter.Tk() # создаём графический интерфейс
        self.root.resizable(True, False)
        self.button = tkinter.Button(
            text='🎙',
            font={'Arial', 220, 'bold'},
            command=self.click_handler # при клике начинаетс и заканчивается запись звука
        )
        self.button.pack()
        self.label = tkinter.Label(text='00:00:00')
        self.label.pack() # для позиционирования виджетов
        self.recording = False # идёт запись или нет
        self.root.mainloop()

    def click_handler(self): # срабатывает при нажатие на кнопку
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start() # запускаем метод record

    def record(self): # записыват звук после нажатия
        audio = pyaudio.PyAudio()
        stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
        )

        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}') # меняем время на каждой тиерации

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1

        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'recording{i}.wav', 'wb') # открываем файл на запись
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close() 


VoiceRecorder()