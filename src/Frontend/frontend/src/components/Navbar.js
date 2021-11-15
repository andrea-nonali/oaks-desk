import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="Navbar">
        <nav className="bg-white shadow">
          <ul className="flex">
          <li className="mr-3 p-4">
            <a className="inline-block" href="/">
                Home
            </a>
          </li>
          <li className="mr-3 p-4">
            <Link to="/pokemon-list">Pokemon List</Link>
          </li>
        </ul>
        </nav>
    </div>
  );
}
