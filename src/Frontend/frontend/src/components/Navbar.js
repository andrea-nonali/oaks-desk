import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="Navbar">
        <nav className="bg-white shadow-lg">
          <ul class="flex">
          <li class="mr-3">
            <a class="inline-block border border-green-300 py-1 px-3 bg-green-300 text-white" href="/">Home</a>
          </li>
          <li class="mr-3">
            <Link to="/pokemon-list">Pokemon List</Link>
          </li>
        </ul>
        </nav>
    </div>
  );
}
