"""Testing fixtures for creating/mocking certain files."""
import io

import pydicom
import pytest


def merge_dcmdict(custom: dict, default: dict) -> dict:
    """Merge a custom dict onto some defaults."""
    custom = custom or {}
    merged = {}
    for key, value in default.items():
        merged[key] = value
    for key, value in custom.items():
        if value is UNSET:
            merged.pop(key)
        else:
            merged[key] = value
    return merged


def apply_dcmdict(dataset: pydicom.Dataset, dcmdict: dict) -> None:
    """Add dataelements to a dataset from the given dcmdict."""
    # pylint: disable=invalid-name
    dcmdict = dcmdict or {}
    for key, value in dcmdict.items():
        if isinstance(value, (list, tuple)):
            VR, value = value
        else:
            VR = pydicom.datadict.dictionary_VR(key)
        dataset.add_new(key, VR, value)


# sentinel value for merge() to skip default_dcmdict keys
UNSET = object()


@pytest.fixture
def default_dcmdict():
    """default dataset dict used in create_dcm."""
    return dict(
        SOPClassUID="1.2.840.10008.5.1.4.1.1.4",  # MR Image Storage
        SOPInstanceUID="1.2.3",
        PatientID="test",
        StudyInstanceUID="1",
        SeriesInstanceUID="1.2",
    )


@pytest.fixture
def create_ds():
    """Create and return a dataset from a dcmdict."""

    def ds(**dcmdict) -> pydicom.Dataset:
        dataset = pydicom.Dataset()
        apply_dcmdict(dataset, dcmdict)
        return dataset

    return ds


@pytest.fixture
def create_dcm(default_dcmdict, create_ds):  # pylint: disable=redefined-outer-name
    """Create a dataset and return it loaded as an fw_file.dicom.DICOM."""

    def dcm(file=None, preamble=None, file_meta=None, **dcmdict):
        dcmdict = merge_dcmdict(dcmdict, default_dcmdict)
        dataset = pydicom.FileDataset(file, create_ds(**dcmdict))
        dataset.preamble = preamble or b"\x00" * 128
        dataset.file_meta = pydicom.dataset.FileMetaDataset()
        apply_dcmdict(dataset.file_meta, file_meta)
        file = file or io.BytesIO()
        pydicom.dcmwrite(file, dataset, write_like_original=bool(file_meta))
        if isinstance(file, io.BytesIO):
            file.seek(0)
        return dicom.DICOM(file)

    return dcm
