#import argsparse
import os
from pathlib import Path
import shutil
import codecs
import subprocess
#def wrtie_lj_meta

def get_vctk_spaker_list(vctk_path):
    wav_speaker_list = list(map(lambda x: x.name,Path(vctk_path).glob('wav48/*/')))
    txt_speaker_list = list(map(lambda x: x.name,Path(vctk_path).glob('txt/*/')))
    
    union_folders = list(set(wav_speaker_list) & set(txt_speaker_list)) # get overlap member
    print(vctk_path + '/wav/* contain ' + str(len(wav_speaker_list)) + ' speakers')
    print(vctk_path + '/txt/* contain ' + str(len(txt_speaker_list)) + ' speakers')
    print('union set have tatal ' + str(len(union_folders)))
    return sorted(union_folders)

def get_txt_info(txt_file):
    fc = subprocess.getoutput('file -b --mime-encoding %s' % txt_file)
    with codecs.open(txt_file,encoding=fc) as f:
        content = f.readline()
    ontent = [x.strip() for x in content] # 去除換行符號
    return content.strip()

def generate_ljform(vctk_path, vctk_folder, out_path):
    for vctk_speaker in vctk_folder:
        '''
        function target: generate ljspeech format for each vctk speaker
        input: vctk_path                        output: output_path
        ./VCTK_r9y9                                 ./VCTK_r9y9_ljformat
           |-- data                                           |-- p225                     
           |-- txt                                               |        |--- wavs
           |-- wav48                                       |        |-- metadata.csv
           `-- speaker-info.txt                   |-- p226
                                                                     |-- p227
        '''
        # mkdir : /VCTK_r9y9_ljformat/p225/wavs
        Path.mkdir(Path(out_path,vctk_speaker, 'wavs'), parents=True, exist_ok=True)
        # copy vctk wav to maked folder
        speaker_wavs = sorted(list(Path(vctk_path,'wav48',vctk_speaker).glob(('./*wav'))))
        list(map(lambda x:shutil.copy(x, Path(out_path,vctk_speaker,'wavs')),speaker_wavs))
        # metadata.csv
        speaker_txts = sorted(list(Path(vctk_path,'txt',vctk_speaker).glob(('./*txt'))))
        meta = list(map(lambda x:x.stem+'|' + get_txt_info(x) + '|' + get_txt_info(x),speaker_txts))
        meta_output = '\n'.join(meta)
        fc = subprocess.getoutput('file -b --mime-encoding %s' % speaker_txts[0])
        meta_path = Path(out_path,vctk_speaker,'metadata.csv')
        with codecs.open(meta_path, 'w', encoding=fc) as f:
            f.write(meta_output)

if __name__ == "__main__":
    vctk_path = '/home/docker/VCTK_r9y9'
    out_path = '/home/docker/VCTK_r9y9_ljform'
    vctk_folder = get_vctk_spaker_list(vctk_path)
    generate_ljform(vctk_path,vctk_folder, out_path)
    print('done')