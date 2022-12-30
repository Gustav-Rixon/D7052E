import React, { useState } from "react";
import { Button, Navbar, Nav, Container } from "react-bootstrap";
import { Link } from "react-router-dom";

function UserNavBar({ handleSingOut, objectValList, onToggle }) {
  const [active, setActive] = useState(false);

  const handleClick = () => {
    onToggle();
    setActive((prevActive) => !prevActive);
  };

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
          <Button
            onClick={handleClick}
            variant={active ? "primary" : "outline-success"}
            className="mx-2"
          >
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
