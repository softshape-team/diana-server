import { connect } from "react-redux";

import { Navbar } from "../../components";
import { withRoot, withAuthenticate } from "../../components/hoc";

interface TasksProps {
  user: any;
}

const Tasks: React.FC<TasksProps> = (props) => {
  return (
    <div className="tasks">
      <Navbar />
      <h1>Tasks</h1>
    </div>
  );
};

const mapStateToProps = (state: any) => ({
  user: state.user,
});

export default withRoot(connect(mapStateToProps)(withAuthenticate(Tasks)));
