import { useRouter } from "next/router";
import { useState } from "react";
import { Container, Form, Button, Alert } from "react-bootstrap";
import { connect } from "react-redux";
import { loginRequest } from "../../redux/actions/user";
import { Credentials } from "../../tstypes";

interface LoginProps {
  user: any;
  login: Function;
}

const Login: React.FC<LoginProps> = (props) => {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submitHandler = async () => {
    const res = await props.login({ username, password });
    if (res === true) {
      router.push("/");
    }
  };

  return (
    <div>
      <Container>
        <Form>
          <Alert variant="danger" hidden={!props.user.errs}>
            Unable to login with the given credentials
          </Alert>
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
          <Button onClick={submitHandler}>Login</Button>
        </Form>
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
