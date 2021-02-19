import { useState } from "react";
import { connect } from "react-redux";
import { Container, Row, Col, Form, Button } from "react-bootstrap";

import { registrationRequest } from "../../redux/actions/registration";
import { User } from "../../tstypes";
import { useRouter } from "next/router";
import style from "./main.module.scss";

interface RegistrationProps {
  registration: any;
  register: Function;
}

const Registration: React.FC<RegistrationProps> = (props) => {
  const router = useRouter();

  const [user, setUser] = useState({
    firstName: "",
    lastName: "",
    username: "",
    email: "",
    password: "",
  });

  const ChangeHandler = (event: any) => {
    setUser((state) => ({
      ...state,
      [event.target.name]: event.target.value,
    }));
  };

  const submitHandler = async () => {
    const res = await props.register(user);
    if (res === true) {
      router.push("/accounts/login");
    }
  };

  return (
    <Container fluid>
      <Row className="justify-content-center">
        <Form className={style.form} as={Col} xs={10}>
          <Form.Row>
            <Form.Group as={Col} xs={6}>
              <Form.Label>First Name</Form.Label>
              <Form.Control
                name="firstName"
                value={user.firstName}
                placeholder="First Name"
                onChange={ChangeHandler}
                isInvalid={
                  props.registration.errs && props.registration.errs.first_name
                }
              />
              <Form.Control.Feedback type="invalid">
                {props.registration.errs && props.registration.errs.first_name}
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group as={Col} xs={6}>
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                name="lastName"
                value={user.lastName}
                placeholder="Last Name"
                onChange={ChangeHandler}
                isInvalid={
                  props.registration.errs && props.registration.errs.last_name
                }
              />
              <Form.Control.Feedback type="invalid">
                {props.registration.errs && props.registration.errs.last_name}
              </Form.Control.Feedback>
            </Form.Group>
          </Form.Row>

          <Form.Group>
            <Form.Label>Username</Form.Label>
            <Form.Control
              name="username"
              value={user.username}
              placeholder="Username"
              onChange={ChangeHandler}
              isInvalid={
                props.registration.errs && props.registration.errs.username
              }
            />
            <Form.Control.Feedback type="invalid">
              {props.registration.errs && props.registration.errs.username}
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Email</Form.Label>

            <Form.Control
              name="email"
              value={user.email}
              placeholder="Email"
              onChange={ChangeHandler}
              isInvalid={
                props.registration.errs && props.registration.errs.email
              }
            />
            <Form.Control.Feedback type="invalid">
              {props.registration.errs && props.registration.errs.email}
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control
              name="password"
              value={user.password}
              type="password"
              placeholder="Password"
              onChange={ChangeHandler}
              isInvalid={
                props.registration.errs && props.registration.errs.password
              }
            />
            <Form.Control.Feedback type="invalid">
              {props.registration.errs && props.registration.errs.password}
            </Form.Control.Feedback>
          </Form.Group>
          <Button onClick={submitHandler} block>
            Register
          </Button>
        </Form>
      </Row>
    </Container>
  );
};

const mapStateToProps = (state: any) => ({
  registration: state.registration,
});

const mapDispatchToProps = (dispatch: Function) => ({
  register: (user: User) => dispatch(registrationRequest(user)),
});

export default connect(mapStateToProps, mapDispatchToProps)(Registration);
