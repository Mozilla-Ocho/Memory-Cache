import React from "react";
import { ILlamafile } from "../api/llamafile_api";

export const LlamafileDetails: React.FC<{ llamafile: ILlamafile }> = ({
  llamafile,
}) => {
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
    </div>
  );
};
