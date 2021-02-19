import { Navbar } from "../../components";
import { withAuthenticate, withRoot } from "../../components/hoc";

interface HabitsProps {}

const Habits: React.FC<HabitsProps> = (props) => {
  return (
    <div className="habits">
      <Navbar />
      <h1>Habits</h1>
    </div>
  );
};

export default withRoot(withAuthenticate(Habits));
