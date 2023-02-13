import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='source path')
parser.add_argument('--ex', help='file prefix')
args = parser.parse_args()
idx = 1
work_path = pathlib.Path(args.path)
prefix = args.ex

for i in work_path.glob("*.jpg"):
    i.replace(i.parent/f'{prefix}_{idx:06}.jpg')
    idx += 1

for i in work_path.glob("*.jpeg"):
    i.replace(i.parent/f'{prefix}_{idx:06}.jpg')
    idx += 1
