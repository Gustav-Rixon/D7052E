import React from "react";
import { Button, Navbar, Nav, Container } from "react-bootstrap";
import { Link } from "react-router-dom";

function UserNavBar({ handleSingOut, objectValList, onToggle }) {
  return (
    <div id="navbar">
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand>
            <Link to="/home">
              <img id="Profile" src={objectValList[0]} alt="Home" />
            </Link>
          </Navbar.Brand>
          <Nav className="me-auto">
            <Navbar.Brand alt="Alejandro Despasito">
              {objectValList[1]} {objectValList[2]}
            </Navbar.Brand>
          </Nav>
          <Button onClick={onToggle} variant="success">
            Whitelist
          </Button>
          <Button onClick={handleSingOut} variant="success">
            Logout
          </Button>
        </Container>
      </Navbar>
    </div>
  );
}

export default UserNavBar;
