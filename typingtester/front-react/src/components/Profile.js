import React, { useEffect, useState } from "react";
import {
  Grid,
  CircularProgress,
  Table,
  TableContainer,
  TableBody,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { ResultBox } from "./smallComponents";
import {
  loadStatistics,
  loadTestRecords,
  fetchUserInfo,
} from "../lookups/lookups";
import { useNavigate } from "react-router-dom";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import { styled } from "@mui/material/styles";
import { convertDateToFormattedTime, convertSecondsToTime } from "../util";

const StyledTableCell = styled(TableCell)(() => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: "#313131",
    color: "#f5e6c8",
    border: 0,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 12,
  },
}));

const StyledTableRow = styled(TableRow)(() => ({
  "&:nth-of-type(odd)": {
    backgroundColor: "#2b2b2b",
  },
  "&:nth-of-type(even)": {
    backgroundColor: "#313131",
  },
  "*": {
    color: "#f5e6c8 !important",
    border: "none !important",
    fontSize: "0.9em !important",
  },
}));

export default () => {
  const [statistics, setStatistics] = useState(null);
  const [testRecords, setTestRecords] = useState(null);
  const [userInfo, setUserInfo] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      setStatistics(await loadStatistics());
      setTestRecords(await loadTestRecords());
      setUserInfo(await fetchUserInfo());
    })();
  }, []);
  console.log(userInfo);

  return (
    <>
      {(statistics && (
        <Grid container spacing={3}>
          {userInfo && (
            <Grid item xs={12}>
              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <div align="left" className="user-detail">
                    Username: {userInfo.username}
                  </div>
                </Grid>
                <Grid item xs={4}>
                  <div align="left" className="user-detail">
                    Email: {userInfo.email}
                  </div>
                </Grid>
                <Grid item xs={4}>
                  <div
                    align="left"
                    className="user-detail"
                    style={{ cursor: "pointer" }}
                    onClick={() => {
                      navigate("/account/change");
                    }}
                  >
                    Change Password
                  </div>
                </Grid>
              </Grid>
            </Grid>
          )}
          <br />
          <Grid item xs={12} sm={6} md={4}>
            <div align="left">
              <ResultBox
                _key="Tests Started"
                value={statistics.tests_started}
              />
            </div>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <div align="left">
              <ResultBox
                _key="Tests Completed"
                value={statistics.tests_completed}
              />
            </div>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <div align="left">
              <ResultBox
                _key="Time Typing"
                value={convertSecondsToTime(statistics.time_typing.toFixed(0))}
              />
            </div>
          </Grid>
          {testRecords && (
            <Grid item xs={12}>
              <TableContainer
                component={Paper}
                style={{ backgroundColor: "#313131" }}
              >
                <Table sx={{ minWidth: 700 }} aria-label="customized table">
                  <TableHead>
                    <TableRow>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        Quote Id
                      </StyledTableCell>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        CPM
                      </StyledTableCell>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        WPM
                      </StyledTableCell>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        ACC
                      </StyledTableCell>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        Time
                      </StyledTableCell>
                      <StyledTableCell
                        align="center"
                        style={{ fontFamily: "Roboto mono !important" }}
                      >
                        Date
                      </StyledTableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {testRecords.map((row, index) => (
                      <StyledTableRow key={index}>
                        <StyledTableCell
                          align="center"
                          scope="row"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {row.quote_id}
                        </StyledTableCell>
                        <StyledTableCell
                          align="center"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {row.cpm}
                        </StyledTableCell>
                        <StyledTableCell
                          align="center"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {Math.round(row.cpm / 5)}
                        </StyledTableCell>
                        <StyledTableCell
                          align="center"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {row.accuracy}
                        </StyledTableCell>
                        <StyledTableCell
                          align="center"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {row.time.toFixed(2)}
                        </StyledTableCell>
                        <StyledTableCell
                          align="center"
                          style={{ fontFamily: "Roboto mono !important" }}
                        >
                          {convertDateToFormattedTime(row.date)}
                        </StyledTableCell>
                      </StyledTableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          )}
          <Grid item xs={4}></Grid>
        </Grid>
      )) || <CircularProgress />}
    </>
  );
};
