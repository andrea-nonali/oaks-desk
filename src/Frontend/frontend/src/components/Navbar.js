import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="Navbar">
        <nav className="bg-white shadow">
          <ul className="flex">
            <li className="nav-item">
                <a className="inline-block" href="/">
                    Home
                </a>
            </li>
            <li className="nav-item">
                <Link to="/pokemon-list">Pokemon List</Link>
            </li>
        </ul>
        </nav>
    </div>
  );
}
