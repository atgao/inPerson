import React from "react";
import Paper from "@material-ui/core/Paper";

import axios from 'axios'

import Scheduler, { Resource } from 'devextreme-react/scheduler';

import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import { teal } from "@material-ui/core/colors";
import { appointments } from "../consts/dummydata/events";

import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.material.teal.light.css';
import { ContentBackspace } from "material-ui/svg-icons";

const theme = createMuiTheme({ palette: { type: "light", primary: teal } });

/* 
FORMAT OF EVENTS

{
    text: "New Brochures",
    startDate: new Date(2019, 6, 3, 14, 30),
    endDate: new Date(2019, 6, 3, 13, 42),
    id: 21,
},

*/

export default class Calendar extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      data: appointments,
      user: this.props.user,
      userid: this.props.userid,
      allApptsToBeRendered: [],
      followingUsersToBeRendered: [],
      startSemDate: null,
      endSemDate: null
    };
  }
  
    days = [
        {id: 0, text: "Monday"},
        {id: 1, text: "Tuesday"},
        {id: 2, text: "Wednesday"},
        {id: 3, text: "Thursday"},
        {id: 4, text: "Friday"},
        {id: 5, text: "Saturday"},
        {id: 6, text: "Sunday"},
    ]

    componentDidUpdate(prevProps) {
        if (prevProps.user !== this.props.user, prevProps.userid !== this.props.userid) {
            this.setState({user: this.props.user, userid: this.props.userid})
            this.setAppointments()
        }
    }

    makeAppt = (appt) => {

    }

    formatApiDayToScheduler = (day) => {
        switch(day) {
            case 'M': return "MO"
            case 'T': return "TU"
            case 'W': return "WE"
            case 'Th': return "TH"
            case 'F': return "FR"
            case 'Sa': return "SA"
            case 'Su': return "SU"
            default: console.log(day);
        }
        console.log("Something went wrong when fetching days from api")
    }

    formatApptApiToScheduler = (appt) => {
        let fm = {}
        fm['text'] = appt['title']
        fm['startDate'] = appt['start_date']
        fm['endDate'] = appt['end_date']
        fm['id'] = 0 ///// do something

        let st = ""
        appt.days.forEach((day) => st+=(this.formatApiDayToScheduler(day) +","))
        st = st.slice(0, st.length-1)
        fm['reccurenceRule'] = `FREQ=WEEKLY;BYDAY=${st}`
        return fm

    }
    

    setAppointments = async () => {
        await this.setSemesterDates()
        // this user
        let all = []
        this.state.user.schedule.forEach((appt) => all.push(this.formatApptApiToScheduler(appt)))
        await this.state.followingUsersToBeRendered.forEach(async (userid) => {
            await axios.get(`/api/schedule/${userid}/`, {user: {userid: this.state.userid}})
            .then((res)=> {
                console.log(res)
                res.data.forEach((appt) => all.push(this.formatApptApiToScheduler(appt)))
                all.push(this)
            })
        })
        return all
    }

    setSemesterDates = async () => {
        await axios.get("/api/events/semester/")
        .then((res) => {
            console.log(res)
            this.setState({
                startSemDate: res.data.start_date,
                endSemDate: res.data.end_date
            })
        })
    }

  render() {
    const { data } = this.state;
    const views = ['day', 'week', 'workWeek', 'month'];
    return (
      <MuiThemeProvider theme={theme}>
        <Paper style = {{paddingTop: 55, width:'100%'}}>
            <Scheduler
                dataSource={data}
                views={views}
                defaultCurrentView={'week'}
                showCurrentTimeIndicator={true}
                height={'80%'}
                startDayHour={0} 
                onAppointmentAdded={(e) => {
                    console.log(e)
                }}
                onAppointmentUpdated={(e) => {
                    console.log(e)
                }}
                onAppointmentDeleted={(e) => {
                    console.log(e)
                }}
                onAppointmentFormOpening={(data) => {
                    let form = data.form;
                    let opts = form.option("items")
                    opts = opts.filter((e) => ((!e.dataField || e.dataField !== "allDay") && (!e.label || e.label.text !== "Repeat")))
                    form.option("items", opts)

                }}>
                    <Resource
                        label={'Days'}
                        fieldExpr={'day'}
                        dataSource={this.days}
                        allowMultiple={true}
                        />
                </Scheduler>
        </Paper>
      </MuiThemeProvider>
    );
  }
}
