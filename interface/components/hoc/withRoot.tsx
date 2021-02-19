const withRoot = (Component: any) => {
  interface WrapperProps {}

  const Wrapper: React.FC<WrapperProps> = (props) => {
    return (
      <div>
        <Component {...props} />
      </div>
    );
  };

  return Wrapper;
};

export default withRoot;
