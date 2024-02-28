from fastapi import APIRouter
from pydantic import BaseModel
from llamafile_manager import get_llamafile_manager
from typing import Optional

router = APIRouter()
manager = get_llamafile_manager()

class LlamafileInfo(BaseModel):
    name: str
    url: str
    downloaded: bool
    running: bool
    download_progress: Optional[int]

class ListLlamafilesResponse(BaseModel):
    llamafiles: list[LlamafileInfo]

@router.get("/list_llamafiles")
async def list_llamafiles():
    """List all llamafiles, including those that have not been downloaded."""
    llamafiles = manager.list_all_llamafiles()
    llamafile_infos = []
    for info in llamafiles:
        llamafile_infos.append(LlamafileInfo(name=info.name,
                                             url=info.url,
                                             downloaded=manager.has_llamafile(info.name),
                                             running=manager.is_llamafile_running(info.name),
                                             download_progress=manager.llamafile_download_progress(info.name)))

    return ListLlamafilesResponse(llamafiles=llamafile_infos)

class GetLlamafileRequest(BaseModel):
    name: str

class GetLlamafileResponse(BaseModel):
    # Respond with the llamafile info or None if the llamafile is not found
    llamafile: Optional[LlamafileInfo]

@router.post("/get_llamafile")
async def get_llamafile(request: GetLlamafileRequest):
    """Get the llamafile info for the llamafile of the given name."""
    all_llamafile_infos = manager.list_all_llamafiles()
    llamafile = next((l for l in all_llamafile_infos if l.name == request.name), None)
    if llamafile is None:
        return GetLlamafileResponse(llamafile=None)

    return GetLlamafileResponse(
        llamafile=LlamafileInfo(name=llamafile.name,
                                url=llamafile.url,
                                downloaded=manager.has_llamafile(llamafile.name),
                                running=manager.is_llamafile_running(llamafile.name),
                                download_progress=manager.llamafile_download_progress(llamafile.name)))

class DownloadLlamafileRequest(BaseModel):
    name: str

class DownloadLlamafileResponse(BaseModel):
    success: bool

@router.post("/download_llamafile")
async def download_llamafile(request: DownloadLlamafileRequest):
    """Download the llamafile of the given name."""
    result = manager.download_llamafile_by_name(request.name)
    return DownloadLlamafileResponse(success=result is not None)

class LlamafileDownloadProgressRequest(BaseModel):
    name: str
class LlamafileDownloadProgressResponse(BaseModel):
    progress: Optional[int]
@router.post("/llamafile_download_progress")
async def llamafile_download_progress(request: LlamafileDownloadProgressRequest):
    """Get the download progress of the llamafile of the given name."""
    progress = manager.llamafile_download_progress(request.name)
    return LlamafileDownloadProgressResponse(progress=progress)

class RunLlamafileRequest(BaseModel):
    name: str

class RunLlamafileResponse(BaseModel):
    success: bool

@router.post("/run_llamafile")
async def run_llamafile(request: RunLlamafileRequest):
    """Download the llamafile of the given name."""
    # The given name might not be valid, in which case the manager will throw.
    # If the manager throws, return success: false
    try:
        result = manager.run_llamafile(request.name, ["--host", "0.0.0.0",
                                                      "--port", "8800",
                                                      "--nobrowser"])
                                                      #"-ngl", "999"])
        return RunLlamafileResponse(success=True)
    except ValueError:
        return RunLlamafileResponse(success=False)


class StopLlamafileRequest(BaseModel):
    name: str

class StopLlamafileResponse(BaseModel):
    success: bool

@router.post("/stop_llamafile")
async def stop_llamafile(request: StopLlamafileRequest):
    """Stop the llamafile of the given name."""
    # The given name might not be valid, in which case the manager will throw.
    # If the manager throws, return success: false
    try:
        result = manager.stop_llamafile_by_name(request.name)
        return StopLlamafileResponse(success=result)
    except ValueError:
        return StopLlamafileResponse(success=False)
