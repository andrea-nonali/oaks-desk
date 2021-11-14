import './App.css';
import { Link } from "react-router-dom";
import Navbar from './components/Navbar';

export default function App() {
  return (
    <div className="App">
      <header className="App-header">
       <Navbar />
      </header>
      <div className="h-screen bg-red-300" />
    </div>
  );
}
