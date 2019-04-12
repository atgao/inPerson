import React from "react";
import Paper from "@material-ui/core/Paper";
import { ViewState, EditingState } from "@devexpress/dx-react-scheduler";
import {
  Scheduler,
  DayView,
  WeekView,
  Appointments,
  AppointmentForm,
  AppointmentTooltip,
  Toolbar,
  ViewSwitcher,
  DateNavigator,
  MonthView
} from "@devexpress/dx-react-scheduler-material-ui";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import { blue } from "@material-ui/core/colors";
import { appointments } from "../consts/dummydata/events";

const theme = createMuiTheme({ palette: { type: "light", primary: blue } });

export default class Calendar extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      data: appointments
    };
  }

  commitChanges = ({ added, changed, deleted }) => {
    console.log("added")
    console.log(added)
    console.log("changed")
    console.log(changed)
    console.log("deleted")
    console.log(deleted)
  }

  render() {
    const { data } = this.state;
    return (
      <MuiThemeProvider theme={theme}>
        <Paper>
            <Scheduler data={data}>
                <ViewState defaultCurrentViewName="Week"/>
                <EditingState  onCommitChanges={this.commitChanges}/>

                <DayView startDayHour={7} endDayHour={24} />
                <WeekView startDayHour={7} endDayHour={24} />
                <MonthView />

                <Toolbar />  
                <DateNavigator />
                <ViewSwitcher />
                
                <Appointments />
                <AppointmentTooltip
                    showOpenButton
                    showDeleteButton
                />
                <AppointmentForm />
                
            </Scheduler>
        </Paper>
      </MuiThemeProvider>
    );
  }
}
