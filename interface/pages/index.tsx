import Head from "next/head";
import { Card, Container, Row, Col } from "react-bootstrap";
import cn from "classnames";
import withAuthenticate from "../components/withAuthenticate";

import style from "./main.module.scss";
import { connect } from "react-redux";

interface HomeProps {
  user: any;
}

const Home: React.FC<HomeProps> = (props) => {
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

const mapDispatchToProps = (dispatch: Function) => ({});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withAuthenticate(Home));
