import React, { useState } from "react";
import { ILlamafile } from "../types";
import { downloadLlamafile } from "../api/llamafile_api";

export const LlamafileDetails: React.FC<{ llamafile: ILlamafile }> = ({
  llamafile,
}) => {
  const [downloadButtonText, setDownloadButtonText] = useState("Download");
  return (
    <div
      style={{
        margin: "10px 0",
        padding: "10px",
        border: "1px solid #ccc",
        borderRadius: "5px",
      }}
    >
      <h3>{llamafile.name}</h3>
      <p>
        URL:{" "}
        <a href={llamafile.url} target="_blank" rel="noopener noreferrer">
          {llamafile.url}
        </a>
      </p>
      <p>Downloaded: {llamafile.downloaded ? "Yes" : "No"}</p>
      <p>Running: {llamafile.running ? "Yes" : "No"}</p>
      <p>Download progress: {llamafile.download_progress}</p>
      <button
        onClick={() => {
          downloadLlamafile(llamafile.name).then((result) => {
            setDownloadButtonText(
              `Download ${result.success ? "Started" : "Failed"}`,
            );
          });
        }}
        disabled={downloadButtonText.includes("Started")}
      >
        {downloadButtonText}
      </button>
    </div>
  );
};
