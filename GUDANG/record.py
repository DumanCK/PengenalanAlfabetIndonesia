import sounddevice as sd
from scipy.io.wavfile import write
#import pydub
#from pydub import AudioSegment


fs = 11000  # Sample rate
seconds = 2  # Duration of recording
print('start')
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
print('finish')
write('SXXX.wav', fs, myrecording)  # Save as WAV file

#pydub.AudioSegment.converter  = "D:\TRANSPORT\MASTER\ffmpeg-4.2.1-win64-static\ffmpeg-4.2.1-win64-static\bin\ffmpeg.exe"

#sound = AudioSegment.from_wav('./output.wav')
#sound.export('myfile.mp3', format='mp3')
