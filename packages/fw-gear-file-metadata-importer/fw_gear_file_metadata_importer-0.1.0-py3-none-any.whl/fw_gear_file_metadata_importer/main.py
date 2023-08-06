import logging
import sys
import typing as t
from pathlib import Path

import flywheel
from fw_meta import MetaData

from fw_gear_file_metadata_importer import dicom

AnyPath = t.Union[str, Path]

log = logging.getLogger(__name__)


def run(
    file_type: str,
    file_path: AnyPath,
    project: flywheel.Project = None,
    siemens_csa: bool = False,
) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).
        siemens_csa (bool): If True parse Siemens CSA DICOM header (Default: False).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    if file_type == "dicom":
        if project:
            log.info(
                "Updating allow/deny tag list from project.info.context.header.dicom."
            )
            # Updating allow/deny tag list from project.info.context.header.dicom
            dicom.update_array_tag(
                project.info.get("context", {}).get("header", {}).get("dicom", {})
            )

        log.info("Processing %s...", file_path)
        fe, meta, qc = dicom.process(file_path, siemens_csa=siemens_csa)
    else:
        log.error(f"File type {file_type} is not supported currently.")
        sys.exit(1)

    return fe, meta, qc
