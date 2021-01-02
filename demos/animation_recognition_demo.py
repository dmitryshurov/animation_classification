#  Copyright (c) 2020. Dmitry Shurov

import argparse
from animation_recognition_processor_input_data_reader import AnimationRecognitionProcessorInputDataReader
from animation_recognition_processor import AnimationRecognitionProcessor


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("anim_path", help="Recorded animation chan path")
    argparser.add_argument("lib_folder", help="Animation library folder containing chan files")

    args = argparser.parse_args()

    data = AnimationRecognitionProcessorInputDataReader.load_from_chan_files(args.anim_path, args.lib_folder)

    p = AnimationRecognitionProcessor()
    p.process(data)
    best_scores = p.get_best_scores(num_scores=10)
    timeline = p.get_timeline_with_placed_animations()

    for idx, best_scores_for_anim in enumerate(best_scores):
        print(idx + 1, best_scores_for_anim)

    print(timeline)


if __name__ == '__main__':
    main()

