import { connect } from "react-redux";
import { Container, Navbar, Nav, NavDropdown } from "react-bootstrap";

import { logoutRequest } from "../../redux/actions/user";

interface NavBarProps {
  user: any;
  logout: Function;
}

const NavBar: React.FC<NavBarProps> = (props) => {
  const logoutHandler = async () => {
    await props.logout(props.user.accessToken);
  };

  return (
    <Navbar collapseOnSelect bg="dark" variant="dark" expand="md">
      <Container>
        <Navbar.Brand>Diana</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />

        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="#tasks">Tasks</Nav.Link>
            <Nav.Link href="#habits">Habits</Nav.Link>
          </Nav>
          <Nav>
            {props.user.isAuthed && (
              <NavDropdown title="User" id="collasible-nav-dropdown">
                <NavDropdown.Item href="#/accounts/profile">
                  Profile
                </NavDropdown.Item>
                <NavDropdown.Item onClick={logoutHandler}>
                  Logout
                </NavDropdown.Item>
              </NavDropdown>
            )}
            {!props.user.isAuthed && (
              <Nav.Link href="/accounts/login">Login</Nav.Link>
            )}
            {!props.user.isAuthed && (
              <Nav.Link href="/accounts/registration">Registration</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

const mapStateToProps = (state: any) => ({
  user: state.user,
});

const mapDispatchToProps = (dispatch: Function) => ({
  logout: (accessToken: string) => dispatch(logoutRequest(accessToken)),
});

export default connect(mapStateToProps, mapDispatchToProps)(NavBar);
