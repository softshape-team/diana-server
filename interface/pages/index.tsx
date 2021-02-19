import Head from "next/head";

import { Navbar } from "../components";
import { withRoot, withAuthenticate } from "../components/hoc";

interface HomeProps {
  user: any;
  logout: Function;
}

const Home: React.FC<HomeProps> = (props) => {
  return (
    <div>
      <Head>
        <title>Diana - A Task Assistant</title>
      </Head>
      <Navbar />

      <h1>Welcome to Diana</h1>
    </div>
  );
};

export default withRoot(withAuthenticate(Home));
