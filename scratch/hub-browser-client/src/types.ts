export interface ILlamafile {
  name: string;
  url: string;
  downloaded: boolean;
  running: boolean;
  download_progress: number | null;
}

export interface IDownloadLlamafileRequest {
  name: string;
}
export interface IDownloadLlamafileResponse {
  success: boolean;
}

export interface IRunLlamafileRequest {
  name: string;
}
export interface IRunLlamafileResponse {
  success: boolean;
}

export interface IStopLlamafileRequest {
  name: string;
}
export interface IStopLlamafileResponse {
  success: boolean;
}
