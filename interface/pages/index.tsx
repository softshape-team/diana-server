import Head from "next/head";
import { useRouter } from "next/router";
import { connect } from "react-redux";
import { Button } from "react-bootstrap";

import { withRoot, withAuthenticate } from "../components/hoc";

interface HomeProps {
  user: any;
}

const Home: React.FC<HomeProps> = (props) => {
  const router = useRouter();

  if (props.user.isAuthed) {
    router.push("/tasks");
  }

  const getStartedClickHandler = () => {
    router.push("/accounts/login");
  };

  return (
    <div className="root">
      <Head>
        <title>Diana - A Task Assistant</title>
      </Head>
      <Button onClick={getStartedClickHandler}>Get Started</Button>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  user: state.user,
});

export default withRoot(connect(mapStateToProps)(withAuthenticate(Home)));
