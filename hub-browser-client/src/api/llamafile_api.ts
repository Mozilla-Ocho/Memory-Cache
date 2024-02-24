import {
  ILlamafile,
  IDownloadLlamafileRequest,
  IDownloadLlamafileResponse,
  IRunLlamafileRequest,
  IRunLlamafileResponse,
  IStopLlamafileRequest,
  IStopLlamafileResponse,
} from "../types";

const base = window.location;
const origin = `${base.protocol}//${base.hostname}`;
const port = 8001;
const llamafileApi = `${origin}:${port}/api/llamafile`;

// List llamafiles
export async function listLlamafiles(): Promise<ILlamafile[]> {
  const response = await fetch(`${llamafileApi}/list_llamafiles`);
  const data = await response.json();
  return data.llamafiles;
}

// Download llamafile
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

// Run llamafile
export async function runLlamafile(
  name: string,
): Promise<IRunLlamafileResponse> {
  const request: IRunLlamafileRequest = { name };
  const response = await fetch(`${llamafileApi}/run_llamafile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  const data = await response.json();
  return data;
}

// Stop llamafile
export async function stopLlamafile(
  name: string,
): Promise<IStopLlamafileResponse> {
  const request: IStopLlamafileRequest = { name };
  const response = await fetch(`${llamafileApi}/stop_llamafile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  const data = await response.json();
  return data;
}
