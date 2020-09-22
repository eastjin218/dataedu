import os, re, os.path, json, sys
import argparse
from tqdm import tqdm
from glob import glob
from pydub import silence, AudioSegment

in_dir = sys.argv[1]
out_dir = sys.argv[2]

big_dir = glob(in_dir+'/*.mp4')
big_dir.sort()
for nu, big in enumerate(big_dir):
    num = str(nu + 42)
    b_name = os.path.basename(big)
    trans_big = '%s/%s.wav'%(in_dir, b_name)
    os.system('ffmpeg -i '+big+' -acodec pcm_s16le -ac 1 -ar 24000 '+trans_big)
    audio_file = AudioSegment.from_file(trans_big)
    skip_idx = 0
    min_silence_len = 100
    silence_thresh=-40
    silence_chunk_len=100
    keep_silence=100
    out_ext = 'wav'
    not_silence_ranges = silence.detect_nonsilent(audio_file,min_silence_len=silence_chunk_len, silence_thresh=silence_thresh)
    edges = [not_silence_ranges[0]]
    for idx in range(1, len(not_silence_ranges)-1):
        cur_start = not_silence_ranges[idx][0]
        prev_end = edges[-1][1]

        if cur_start - prev_end < min_silence_len:
            edges[-1][1] = not_silence_ranges[idx][1]
        else:
            edges.append(not_silence_ranges[idx])

    audio_paths = []
    os.makedirs('%s/%s'%(out_dir,num), exist_ok=True) 
    for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
        export_dir = "{}/{}/{}_{:04d}.wav".format(out_dir, num, num, idx)
        start_idx = max(0, start_idx - keep_silence)
        end_idx += keep_silence

        target_audio_path = export_dir
        #target_audio_path = "{}/{}.{:04d}.{}".format(
        #        out_dir, filename, idx, out_ext)

        segment=audio_file[start_idx:end_idx]

        segment.export(target_audio_path, out_ext)  # for soundsegment

        audio_paths.append(target_audio_path)
