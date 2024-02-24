import { ILlamafile } from "../types";

const host = "http://localhost:8001";
const llamafileApi = `${host}/api/llamafile`;

export async function listLlamafiles(): Promise<ILlamafile[]> {
  const response = await fetch(`${llamafileApi}/list_llamafiles`);
  const data = await response.json();
  return data.llamafiles;
}
