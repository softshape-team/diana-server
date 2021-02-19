import { connect } from "react-redux";
import { useEffect } from "react";
import { authenticateByTokens } from "../../redux/actions/user";

const withAuthenticate = (Component: any) => {
  interface WrapperProps {
    authenticateByTokens: Function;
  }

  const Wrapper: React.FC<WrapperProps> = (props) => {
    useEffect(() => {
      props.authenticateByTokens();
    }, []);

    return <Component {...props} />;
  };

  const mapStateToProps = (state: any) => ({});

  const mapDispatchToProps = (dispatch: any) => ({
    authenticateByTokens: () => dispatch(authenticateByTokens()),
  });

  return connect(mapStateToProps, mapDispatchToProps)(Wrapper);
};

export default withAuthenticate;
