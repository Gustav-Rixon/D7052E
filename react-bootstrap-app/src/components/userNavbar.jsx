import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";

function UserNavBar({ handleSingOut, picture, given_name, family_name }) {
  return (
    <div id="navbar">
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#home">
            <img id="Profile" src={picture} alt="Home" />{" "}
          </Navbar.Brand>
          <Nav className="me-auto">
            <Navbar.Brand>
              {given_name} {family_name}
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
