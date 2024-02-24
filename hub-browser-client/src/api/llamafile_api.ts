import {
  ILlamafile,
  IDownloadLlamafileRequest,
  IDownloadLlamafileResponse,
} from "../types";

const base = window.location;
const origin = `${base.protocol}//${base.hostname}`;
const port = 8001;
const llamafileApi = `${origin}:${port}/api/llamafile`;

export async function listLlamafiles(): Promise<ILlamafile[]> {
  const response = await fetch(`${llamafileApi}/list_llamafiles`);
  const data = await response.json();
  return data.llamafiles;
}

export async function downloadLlamafile(
  name: string,
): Promise<IDownloadLlamafileResponse> {
  const request: IDownloadLlamafileRequest = { name };
  const response = await fetch(`${llamafileApi}/download_llamafile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  const data = await response.json();
  return data;
}
