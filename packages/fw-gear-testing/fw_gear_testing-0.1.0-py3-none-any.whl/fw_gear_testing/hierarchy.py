"""Hierachy related fixtures."""
import flywheel
import pytest


class MockFinder:
    def __init__(self, arr):
        self.arr = arr

    def iter(self):
        for x in self.arr:
            yield x

    def __len__(self):
        return len(self.arr)

    def __call__(self):
        return self.arr


class MockContainerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        analyses = []
        files = []
        _update = None  # to store updates made to the container when calling `update`

    def reload(self):
        if self._update:
            for k, v in self._update.items():
                setattr(self, k, v)
            self._update = None
        return self

    def update(self, *args, **kwargs):
        self._update = flywheel.util.params_to_dict("update", args, kwargs)
        return None


class MockAcquisition(MockContainerMixin, flywheel.Acquisition):
    pass


class MockSession(MockContainerMixin, flywheel.Session):
    acquisitions = MockFinder([])


class MockSubject(MockContainerMixin, flywheel.Subject):
    sessions = MockFinder([])


class MockProject(MockContainerMixin, flywheel.Project):
    subjects = MockFinder([])


@pytest.fixture(scope="function")
def fw_project():
    """Mock a flywheel project"""

    def get_fw_project(n_subjects=5, n_sessions=1, n_acquisitions=1, n_files=1):
        project = MockProject(label="Mock", info={"study_id": "test"})
        subjects = []
        for i in range(n_subjects):
            subject = MockSubject(label=f"sub-{i}")
            sessions = []
            for j in range(n_sessions):
                session = MockSession(label=f"ses-{j}")
                acquisitions = []
                for k in range(n_acquisitions):
                    acquisition = MockAcquisition(label=f"acq-{k}")
                    files = []
                    for l in range(n_files):
                        files.append(flywheel.FileEntry(name=f"file-{l}"))
                    acquisition.files = files
                    acquisitions.append(acquisition)
                session.acquisitions = MockFinder(acquisitions)
                sessions.append(session)
            subject.sessions = MockFinder(sessions)
            subjects.append(subject)
        project.subjects = MockFinder(subjects)
        return project

    return get_fw_project
