import './App.css';
import { Link } from "react-router-dom";

export default function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className=" border-2">
          <h1>Hello Tailwind</h1>
        </div>
      </header>

      <nav>
        <Link to="/pokemon">Pokemon</Link> |{" "}
        <Link to="/generation">Generation</Link>
      </nav>
    </div>
  );
}
