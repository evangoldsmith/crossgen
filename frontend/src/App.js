import React, { useState, useEffect } from "react";
import "./App.css";
import Board from "./components/Board";

function App() {


  return (
      <div className="App">
          <header className="App-header">
              <h1>CrossGen</h1>
              <Board />
          </header>
      </div>
  );
}

export default App;