import Head from "next/head";
import { connect } from "react-redux";
import { Card, Container, Row, Col, Button } from "react-bootstrap";
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
      <Container fluid>
        <Row className="justify-content-center">
          <Card as={Col} md={6} className={cn(style.card)}>
            <Card.Header>
              <h1>Welcome to Diana</h1>
            </Card.Header>
            <Card.Body>
              Diana is a free and open-source application that helps you to live
              a better day. <br />
              To contribute on diana project checkout our source code
              <ul className={style.sourceCodeLinks}>
                <li>
                  <a href="https://github.com/softshapeorg/diana">Diana web</a>
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
              <span>
                {!!props.user.isAuthed && "Authed"}
                {!props.user.isAuthed && "Not authed"}
              </span>
              <Button onClick={logoutHandler}>Logout</Button>
            </Card.Footer>
          </Card>
        </Row>
      </Container>
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
