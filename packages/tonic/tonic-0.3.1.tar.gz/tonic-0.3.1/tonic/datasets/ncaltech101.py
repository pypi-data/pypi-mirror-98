import os
import numpy as np
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import (
    check_integrity,
    download_and_extract_archive,
    extract_archive,
)


class NCALTECH101(VisionDataset):
    """NCALTECH101 <https://www.garrickorchard.com/datasets/n-caltech101> data set.

    arguments:
        save_to: location to save files to on disk
        download: choose to download data or not
        transform: list of transforms to apply to the data
        target_transform: list of transforms to apply to targets
    """

    url = "https://www.dropbox.com/sh/iuv7o3h2gv6g4vd/AAD0T79lglp-BrdbSCuH_7MFa/Caltech101.zip?dl=1"
    file_md5 = "66201824eabb0239c7ab992480b50ba3"
    filename = "Caltech101.zip"
    folder_name = "Caltech101"

    sensor_size = (233, 173)
    ordering = "xytp"

    def __init__(self, save_to, download=True, transform=None, target_transform=None):
        super(NCALTECH101, self).__init__(
            save_to, transform=transform, target_transform=target_transform
        )

        self.location_on_system = save_to
        self.data = []
        self.targets = []

        if download:
            self.download()

        if not check_integrity(
            os.path.join(self.location_on_system, self.filename), self.file_md5
        ):
            raise RuntimeError(
                "Dataset not found or corrupted."
                + " You can use download=True to download it"
            )

        file_path = self.location_on_system + "/" + self.folder_name
        for path, dirs, files in os.walk(file_path):
            dirs.sort()
            for file in files:
                if file.endswith("bin"):
                    events = self._read_dataset_file(path + "/" + file)
                    self.data.append(events)
                    label_number = os.path.basename(path)
                    self.targets.append(label_number)

    def __getitem__(self, index):
        events, target = self.data[index], self.targets[index]
        if self.transform is not None:
            events = self.transform(events, self.sensor_size, self.ordering)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return events, target

    def __len__(self):
        return len(self.data)

    def download(self):
        download_and_extract_archive(
            self.url, self.location_on_system, filename=self.filename, md5=self.file_md5
        )

    def _read_dataset_file(self, filename):
        f = open(filename, "rb")
        raw_data = np.fromfile(f, dtype=np.uint8)
        f.close()
        raw_data = np.uint32(raw_data)

        all_y = raw_data[1::5]
        all_x = raw_data[0::5]
        all_p = (raw_data[2::5] & 128) >> 7  # bit 7
        all_ts = (
            ((raw_data[2::5] & 127) << 16) | (raw_data[3::5] << 8) | (raw_data[4::5])
        )

        # Process time stamp overflow events
        time_increment = 2 ** 13
        overflow_indices = np.where(all_y == 240)[0]
        for overflow_index in overflow_indices:
            all_ts[overflow_index:] += time_increment

        # Everything else is a proper td spike
        td_indices = np.where(all_y != 240)[0]

        td = np.empty([td_indices.size, 4], dtype=np.int32)
        td[:, 0] = all_x[td_indices]
        td[:, 1] = all_y[td_indices]
        td[:, 2] = all_ts[td_indices]
        td[:, 3] = all_p[td_indices]

        return td
