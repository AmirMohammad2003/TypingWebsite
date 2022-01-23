import { calculateWpmCpm, calculateAccuracy } from "../util";
import { IconButtonWithPopup } from "./smallComponents";
import { Grid } from "@mui/material";

const Results = ({ start_time, end_time, errors, letters_typed }) => {
  let [cpm, wpm] = calculateWpmCpm(
    start_time,
    end_time,
    letters_typed - errors
  );
  let acc = calculateAccuracy(letters_typed, errors);

  console.log(start_time, end_time, errors, letters_typed);
  return (
    <>
      <div id="detail-board" className="popup-animation">
        <Grid container spacing={1}>
          <Grid item xs={3} align="center">
            <div className="detail">WPM: {wpm}</div>
          </Grid>
          <Grid item xs={3} align="center">
            <div className="detail">CPM: {cpm}</div>&nbsp;&nbsp;
          </Grid>
          <Grid item xs={3} align="center">
            <div className="detail">ACC: {acc}%</div>&nbsp;&nbsp;
          </Grid>
          <Grid item xs={3} align="center">
            <div className="detail">
              Time: {(end_time - start_time).toFixed(2).toString()}s
            </div>
          </Grid>
        </Grid>
      </div>
      <div className="center-flex" style={{ marginTop: "20px" }}>
        <IconButtonWithPopup
          iconClass="fa-rotate-right"
          popupText="Refresh Test"
        />
      </div>
    </>
  );
};

export default Results;
