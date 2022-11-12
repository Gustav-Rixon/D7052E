import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";

function UserNavBar({ handleSingOut, objectVals }) {
  return (
    <div id="navbar">
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#">
            <img id="Profile" src={objectVals[0]} alt="Home" />{" "}
          </Navbar.Brand>
          <Nav className="me-auto">
            <Navbar.Brand>
              {objectVals[1]} {objectVals[2]}
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
