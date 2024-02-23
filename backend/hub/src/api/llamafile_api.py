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

class ListLlamafilesResponse(BaseModel):
    llamafiles: list[LlamafileInfo]

@router.get("/list_llamafiles")
async def list_llamafiles():
    """List all llamafiles, including those that have not been downloaded."""
    llamafiles = manager.list_all_llamafiles()
    llamafile_infos = []
    for name, url in llamafiles:
        llamafile_infos.append(LlamafileInfo(name=name, url=url, downloaded=manager.has_llamafile(name), running=manager.is_llamafile_running(name)))

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
    llamafile = next((l for l in all_llamafile_infos if l[0] == request.name), None)
    if llamafile is None:
        return GetLlamafileResponse(llamafile=None)

    return GetLlamafileResponse(
        llamafile=LlamafileInfo(name=llamafile[0],
                                url=llamafile[1],
                                downloaded=manager.has_llamafile(llamafile[0]),
                                running=manager.is_llamafile_running(llamafile[0])))

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
