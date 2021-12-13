import sounddevice as sd
from scipy.io.wavfile import write
#import scipy.io.wavfile
import librosa
from dtw import dtw
from numpy.linalg import norm

i = 1
while i < 2:
    #print(i)
    #i += 1
    A = raw_input("Tekan  Enter untuk merekam suara 1 ....")
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording
    print 'Record Suara 1'
    print 'mulai'
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print 'berhenti'
    write('output.wav', fs, myrecording)  # Save as WAV file 

    B = raw_input("Tekan  Enter untuk merekam suara 2 ....")
    print 'Record Suara 2'
    print 'mulai'
    myrecording2 = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print 'berhenti'
    write('output2.wav', fs, myrecording2)  # Save as WAV file

    y1, sr1 = librosa.load('./output.wav')
    y2, sr2 = librosa.load('./output2.wav')
    mfcc1 = librosa.feature.mfcc(y1, sr1)
    mfcc2 = librosa.feature.mfcc(y2, sr2)
    dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
    print 'Jarak suara 1 dan 2 :', dist

    C = raw_input("Tekan sembarang untuk mengulangi atau 1 untuk selesai : ")
    if C == '1' :
        i += 5
    
