import { useState, useEffect } from "react";
import "./App.css";
import { listLlamafiles } from "./api/llamafile_api";
import { ILlamafile } from "./types";
import { LlamafileDetails } from "./components/llamafile_details";

function App() {
  const [llamafiles, setLlamafiles] = useState<ILlamafile[]>([]);

  useEffect(() => {
    listLlamafiles().then(setLlamafiles);

    const intervalId = setInterval(() => {
      listLlamafiles().then(setLlamafiles);
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      {llamafiles.map((llamafile, index) => (
        <div key={index}>
          <LlamafileDetails key={llamafile.name} llamafile={llamafile} />
        </div>
      ))}
    </div>
  );
}

export default App;
