import codecs
import os
from multiprocessing.pool import Pool
import soundfile as sf
import librosa
import sys


def convert_to_16k(path_file):
    in_path = path_file
    out_path = path_file.replace("/speech_data/", "/speech_data_22050/")
    out_folder = os.path.dirname(out_path)
    os.makedirs(out_folder, exist_ok=True)
    y, s = librosa.load(in_path, sr=16000)
    y_16k = librosa.resample(y, s, 22050)
    sf.write(out_path, y_16k, 22050, format='WAV', subtype='PCM_16')
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


