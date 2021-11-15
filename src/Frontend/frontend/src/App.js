import './App.css';
import { Link } from "react-router-dom";
import Navbar from './components/Navbar';

export default function App() {
  return (
    <div className="App">
      <header className="App-header">
      </header>
      <div className="h-screen">
        <h1 className="text-center text-7xl font-extrabold p-5">Oak's Desk</h1>
        <h3 className="text-center text-5xl font-medium p-5">We hacked into professor Oak's PC</h3>
        <h5 className="text-center text-3xl font-light p-5">Do you want to find out what we discovered ?</h5>
        <div className="flex mt-5">
        <div className="w-1/2 text-right mr-9">
          <Link to='/pokemon-list'>
            <button className="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
              Full Pokedex
            </button>
          </Link>
          </div>
          <div className="w-1/2 text-left ml-9">
          <Link to='/pokemon-list'>
            <button className="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
              Other features
            </button>
          </Link>
        </div>
      </div>
      </div>
    </div>
  );
}
