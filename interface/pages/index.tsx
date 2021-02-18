import Head from "next/head";
import { connect } from "react-redux";
import {
  Card,
  Container,
  Row,
  Col,
  Navbar,
  Nav,
  NavDropdown,
} from "react-bootstrap";
import cn from "classnames";
import withAuthenticate from "../components/withAuthenticate";
import { logoutRequest } from "../redux/actions/user";

import style from "./main.module.scss";

interface HomeProps {
  user: any;
  logout: Function;
}

const Home: React.FC<HomeProps> = (props) => {
  const logoutHandler = async () => {
    await props.logout(props.user.accessToken);
  };

  return (
    <div>
      <Head>
        <title>Diana - A Task Assistant</title>
      </Head>

      <div className="root">
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
                  <Nav.Link href="/accounts/registration">
                    Registration
                  </Nav.Link>
                )}
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Container fluid>
          <Row className="justify-content-center">
            <Card as={Col} md={6} className={cn(style.card)}>
              <Card.Header>
                <h1>Welcome to Diana</h1>
              </Card.Header>
              <Card.Body>
                Diana is a free and open-source application that helps you to
                live a better day. <br />
                To contribute on diana project checkout our source code
                <ul className={style.sourceCodeLinks}>
                  <li>
                    <a href="https://github.com/softshapeorg/diana">
                      Diana web
                    </a>
                  </li>
                  <li>
                    <a href="https://github.com/softshapeorg/diana-mobile">
                      Diana mobile
                    </a>
                  </li>
                </ul>
              </Card.Body>
              <Card.Footer>
                Created by <a href="https://softshape.org">Softshape</a>{" "}
              </Card.Footer>
            </Card>
          </Row>
        </Container>
      </div>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  user: state.user,
});

const mapDispatchToProps = (dispatch: Function) => ({
  logout: (accessToken: string) => dispatch(logoutRequest(accessToken)),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withAuthenticate(Home));
