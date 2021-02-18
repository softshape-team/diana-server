import { useRouter } from "next/router";
import ErrorPage from "next/error";
import { Container, Row, Col } from "react-bootstrap";
import style from "./main.module.scss";
import cn from "classnames";

import Login from "../../components/login";
import Registration from "../../components/registration";

interface AccountsProps {}

const Accounts: React.FC<AccountsProps> = (props) => {
  const router = useRouter();

  let FormComponent = null;

  if (router.query.name === "login") {
    FormComponent = <Login />;
  } else if (router.query.name === "registration") {
    FormComponent = <Registration />;
  } else {
    return <ErrorPage statusCode={404} />;
  }

  return (
    <Container fluid className={style.container}>
      <Row className={style.row}>
        <Col xs={6} className={cn(style.description, style.displayNone)}>
          <h1>Welcome to Diana</h1>
        </Col>
        <Col xs={12} md={6} className={style.form}>
          <div className={style.formContainer}>{FormComponent}</div>
        </Col>
      </Row>
    </Container>
  );
};

export default Accounts;
