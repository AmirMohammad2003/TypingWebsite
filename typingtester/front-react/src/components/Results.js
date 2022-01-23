import { calculateWpmCpm, calculateAccuracy } from "../util";
import { IconButtonWithPopup } from "./smallComponents";
import { Grid } from "@mui/material";

const ResultBox = ({ _key, value }) => {
  return (
    <>
      <div className="detail">
        <div className="result-key">{_key}</div>
        <div className="result-value">{value}</div>
      </div>
    </>
  );
};

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
            <ResultBox _key="WPM" value={wpm} />
          </Grid>
          <Grid item xs={3} align="center">
            <ResultBox _key="CPM" value={cpm} />
          </Grid>
          <Grid item xs={3} align="center">
            <ResultBox _key="ACC" value={acc + "%"} />
          </Grid>
          <Grid item xs={3} align="center">
            <ResultBox
              _key="Time"
              value={(end_time - start_time).toFixed(2).toString() + "s"}
            />
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
