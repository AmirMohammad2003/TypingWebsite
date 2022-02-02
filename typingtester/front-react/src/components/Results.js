import React, { useEffect, useState } from "react";
import { calculateWpmCpm, calculateAccuracy } from "../util";
import { IconButtonWithPopup, ResultBox } from "./smallComponents";
import { Grid } from "@mui/material";
import { SendTestRecordData } from "../lookups/requests";
import { isAuthenticatedStrict } from "../lookups/lookups";

const Results = ({
  quote_id,
  start_time,
  end_time,
  errors,
  letters_typed,
  refreshCallback,
}) => {
  const [results, setResults] = useState([0, 0, 0]);
  useEffect(() => {
    let [cpm, wpm] = calculateWpmCpm(
      start_time,
      end_time,
      letters_typed - errors
    );
    let acc = calculateAccuracy(letters_typed, errors);

    setResults([acc, cpm, wpm]);

    if (isAuthenticatedStrict) {
      SendTestRecordData(quote_id, end_time - start_time, cpm, acc);
    }
  }, [end_time, start_time, letters_typed, errors, quote_id]);

  let [acc, cpm, wpm] = results;
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
          to="#"
          iconClass="fa-rotate-right"
          popupText="Refresh Test"
          onClickCallback={refreshCallback}
        />
      </div>
    </>
  );
};

export default Results;
