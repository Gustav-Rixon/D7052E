import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";

import { Link } from "react-router-dom";


function UserNavBar({ handleSingOut, objectValList }) {
  return (
    <div id="navbar">
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand>
            <Link to="/">
              <img id="Profile" src={objectValList[0]} alt="Home" />
            </Link>
          </Navbar.Brand>
          <Nav className="me-auto">
            <Navbar.Brand>
              {objectValList[1]} {objectValList[2]}
            </Navbar.Brand>
          </Nav>

          <Button onClick={handleSingOut} variant="outline-success">
            Logout
          </Button>
        </Container>
      </Navbar>
    </div>
  );
}

export default UserNavBar;
