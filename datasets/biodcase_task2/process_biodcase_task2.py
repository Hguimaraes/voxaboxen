import os
import argparse
import pandas as pd
from tqdm import tqdm
from glob import glob
from typing import List


# def process_audio_and_annot(
#     annot,
#     audio,
#     sr,
#     labels=["abz", "d", "bm"],
# ):
#     low_hz = 100
#     high_hz = sr / 2 - low_hz

#     selection_table = pd.DataFrame(
#         {
#             "Begin Time (s)": begin_time,
#             "End Time (s)": end_time,
#             "Annotation": ys,
#             "Low Freq (Hz)": [low_hz for x in begin_time],
#             "High Freq (Hz)": [high_hz for x in begin_time],
#         }
#     ).drop_duplicates()

#     return selection_table


def main(args):
    data_root = args.data_root
    dest_folder = os.path.join(os.getcwd(), "formatted")
    get_audio_path = lambda mode: os.path.join(data_root, mode, "audio")
    get_annot_path = lambda mode: os.path.join(data_root, mode, "annotations/*.csv")

    train_audio_path = get_audio_path("train")
    train_annotation_file = glob(get_annot_path("train"))
    train_annotation_file = pd.concat(
        [pd.read_csv(f) for f in train_annotation_file], axis=0
    )

    valid_audio_path = get_audio_path("validation")
    valid_annotation_file = glob(get_annot_path("validation"))
    valid_annotation_file = pd.concat(
        [pd.read_csv(f) for f in valid_annotation_file], axis=0
    )

    train_info, train_selection_table = annot_block_process(
        "train", train_annotation_file, train_audio_path, dest_folder
    )


def annot_block_process(
    mode="train",
    annotation_file: pd.DataFrame = None,
    data_root: str = None,
    dest_folder: str = None,
):
    print(f"[DEBUG]::Processing the {mode} split")
    mode_info = [
        {
            "fn": "_".join([r.dataset, r.filename])[:-4],
            "audio_fp": os.path.join(data_root, r.filename),
            "selection_table_fp": os.path.join(
                dest_folder, "_".join([r.dataset, r.filename]).replace(".wav", ".txt")
            ),
        }
        for _, r in annotation_file.iterrows()
    ]
    mode_info = pd.DataFrame(mode_info).drop_duplicates().reset_index(drop=True)
    print(mode_info)

    selection_table = None
    for idx, row in tqdm(mode_info.iterrows(), total=len(mode_info)):
        annots_for_sample = annotation_file[
            annotation_file.filename == os.path.basename(row.audio_fp)
        ]
        print(annots_for_sample)
        break

    return mode_info, selection_table


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_root",
        default="/media/heitor/Research/raw_files/biodcase_task2",
        type=str,
        help="Audio & annotations root directory",
    )
    args = parser.parse_args()

    main(args)
