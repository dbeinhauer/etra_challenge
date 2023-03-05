# -*- coding: utf-8 -*-
import sys
import urllib.request
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import numpy as np
import pandas as pd

class ETRA:
    """
    ETRA Dataset
    """

    data_dir: Path = None

    # URL to ETRA Dataset
    _URL = "http://smc.neuralcorrelate.com/ETRA2019/ETRA2019Challenge.zip"

    def __init__(self,
                 data_dir: str = "data",
                 dataset: str = "etra",
                 download=True) -> None:
        self.data_dir = Path.cwd() / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if download:
            data_path = self.data_dir / "{}.zip".format(dataset)
            if not data_path.exists():
                print(
                    f"Downloading dataset {dataset} (this can take a while) ... ",
                    file=sys.stderr,
                    end="",
                )
                urllib.request.urlretrieve(self._URL, filename=data_path)
                print("DONE", file=sys.stderr)
            else:
                print(f"Dataset {dataset} already downloaded.", file=sys.stderr)

            with ZipFile(data_path, "r") as archive:
                print(f"Unpacking {dataset}...", file=sys.stderr)
                for filename in archive.namelist():
                    file_path = self.data_dir / filename
                    if not file_path.exists():
                        print(f"Extracting\t{filename}", file=sys.stderr)
                        archive.extract(filename, path=self.data_dir)


def read_data(data_path: Union[str, Path]) -> pd.DataFrame:
    data_path = Path(data_path)

    filename = data_path.stem
    (
        participant_id,
        trial_id,
        fv_fixation,
        task_type,
        stimulus_id,
    ) = filename.split("_")[:5]

    df = pd.read_csv(data_path)
    orig_cols = df.columns.to_list()
    new_cols = {
        "participant_id": participant_id,
        "trial_id": trial_id,
        "fv_fixation": fv_fixation,
        "task_type": task_type,
        "stimulus_id": stimulus_id if stimulus_id else pd.NA, 
            # Check whether `stimulus_id` is defined (not always).
    }
    df = df.assign(**new_cols)
    df = df[[
        "participant_id",
        "trial_id",
        "fv_fixation",
        "task_type",
        "stimulus_id",
    ] + orig_cols]

    return df