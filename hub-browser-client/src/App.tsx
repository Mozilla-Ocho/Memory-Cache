import React from "react";
import logo from "./logo.svg";
import "./App.css";

// Add a button that, when clicked, fetches http://localhost:8001/api/llamafile/list_llamafiles and logs the result to the console.
function fetchLlamaFiles() {
  fetch("http://localhost:8001/api/llamafile/list_llamafiles")
    .then((response) => response.json())
    .then((data) => console.log(data));
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={fetchLlamaFiles}>Fetch Llama Files</button>
      </header>
    </div>
  );
}

export default App;
