import { useState, useEffect } from "react";
import "./App.css";
import { listLlamafiles } from "./api/llamafile_api";
import { ILlamafile } from "./types";
import { LlamafileDetails } from "./components/llamafile_details";

function App() {
  const [llamafiles, setLlamafiles] = useState<ILlamafile[]>([]);

  useEffect(() => {
    listLlamafiles().then(setLlamafiles);

    // Set up an interval to fetch llama files every second
    const intervalId = setInterval(() => {
      console.log("Fetching llamafiles");
      listLlamafiles().then(setLlamafiles);
    }, 1000);

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      {llamafiles.map((llamafile, index) => (
        <div key={index}>
          <LlamafileDetails key={llamafile.name} llamafile={llamafile} />
        </div>
      ))}
      <button onClick={() => listLlamafiles().then(setLlamafiles)}>
        Refresh
      </button>
    </div>
  );
}

export default App;
