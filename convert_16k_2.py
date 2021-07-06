import codecs
import os
from multiprocessing.pool import Pool
import soundfile as sf
import librosa
import sys
from pydub import AudioSegment
def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def convert_to_16k(path_file):
    in_path = path_file
    out_path = path_file.replace("/speech_data/", "/speech_data_22050/")
    out_folder = os.path.dirname(out_path)
    os.makedirs(out_folder, exist_ok=True)
    sound = AudioSegment.from_file(in_path, format="wav")
    sound = sound.set_frame_rate(22050).set_channels(1)
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]
    trimmed_sound.export(out_path, format="wav")

    out_path_2 = path_file.replace("/speech_data/", "/speech_data_22050_1/")
    out_folder_2 = os.path.dirname(out_path_2)
    os.makedirs(out_folder_2, exist_ok=True)
    y, s = librosa.load(out_path, sr=22050)
    y_16k = librosa.resample(y, s, 22050)
    sf.write(out_path_2, y_16k, 22050, format='WAV', subtype='PCM_16')

if __name__ == '__main__':
    input_folder = sys.argv[1]
    files = os.listdir(input_folder)
    for file in files:
        lst_file = os.path.join(input_folder, file)
        f_in = codecs.open(lst_file, "r", encoding="utf-8")
        data = f_in.readlines()
        # convert 16k sample rates
        audio_names = []
        for line in data:
            info = line.split("|")[0]
            audio_name = info.replace("/root/src/data", "/media/fit/storage5/VietAnh")
            audio_names.append(audio_name)
        pool = Pool(20)
        pool.map(convert_to_16k,audio_names)


