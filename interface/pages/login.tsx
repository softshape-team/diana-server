import { useState } from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";
import { connect } from "react-redux";
import { loginRequest } from "../redux/actions/user";
import { Credentials } from "../tstypes";

interface LoginProps {
  login: Function;
}

const Login: React.FC<LoginProps> = (props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div>
      <Container>
        <Row className="justify-content-center">
          <Form as={Col} lg={6}>
            <Form.Group>
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </Form.Group>
            <Button onClick={() => props.login({ username, password })}>
              Login
            </Button>
          </Form>
        </Row>
      </Container>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  user: state.user,
});

const mapDispatchToProps = (dispatch: any) => ({
  login: (cred: Credentials) => dispatch(loginRequest(cred)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Login);
