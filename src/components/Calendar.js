import React from "react";
import Paper from "@material-ui/core/Paper";

import axios from 'axios'

import Scheduler, { Resource } from 'devextreme-react/scheduler';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';


import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.material.teal.light.css';

export default class Calendar extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      user: this.props.user,
      userid: this.props.userid,
      allApptsToBeRendered: [],
      followingUsersToBeRendered: [],
      startSemDate: {},
      endSemDate: {}
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
        if (prevProps.user !== this.props.user || 
            prevProps.userid !== this.props.userid ||
            prevProps.displayUsers !== this.props.displayUsers) {
            this.setState({
                user: this.props.user, 
                userid: this.props.userid,
                followingUsersToBeRendered: this.props.displayUsers
            })
            this.setAppointments()
        }
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
        fm['startDate'] =  new Date(this.state.startSemDate.year, 
                                    this.state.startSemDate.month,
                                    this.state.startSemDate.date,
                                    parseInt(appt.start_time.slice(0, 2)),
                                    parseInt(appt.start_time.slice(3, 5)))
        fm['endDate'] =new Date(this.state.startSemDate.year, 
                                this.state.startSemDate.month,
                                this.state.startSemDate.date,
                                parseInt(appt.end_time.slice(0, 2)),
                                parseInt(appt.end_time.slice(3, 5)))
        fm['id'] = appt['id']

        let st = ""
        appt.days.forEach((day) => st+=(this.formatApiDayToScheduler(day) +","))
        st = st.slice(0, st.length-1)
        fm['recurrenceRule'] = `FREQ=WEEKLY;BYDAY=${st};UNTIL=${this.state.endSemDate}`
        return fm

    }

    formatApptSchedulerToApi = (appt) => {
        let fm = {}
        fm['title'] = appt['text']
        let startH = "" + appt['startDate'].getHours()
        if (startH.length === 1) startH = '0' + startH
        let startM = "" + appt['startDate'].getMinutes()
        if (startM.length === 1) startM = '0' + startM
        let endH = "" + appt['endDate'].getHours()
        if (endH.length === 1) endH = '0' + endH
        let endM = "" + appt['endDate'].getMinutes()
        if (endM.length === 1) endM = '0' + endM

        fm['start_time'] = `${startH}:${startM}:00`
        fm['end_time'] = `${endH}:${endM}:00`
        fm['days'] = appt['day'].map(this.formatNumberDayToApi)

        console.log(fm)

        return fm
    }

    formatSchedulerDayToApi = (day) => {
        switch(day) {
            case 'MO': return 'M'
            case 'TU': return 'T'
            case 'WE': return 'W'
            case 'TH': return 'Th'
            case 'FR': return 'F'
            case 'SA': return 'Sa'
            case 'SU': return 'Su'
            default: console.log(day);
        }
        console.log("Something went wrong when fetching days from the scheduler")
    }

    formatNumberDayToApi = (day) => {
        switch(day) {
            case 0: return 'M'
            case 1: return 'T'
            case 2: return 'W'
            case 3: return 'Th'
            case 4: return 'F'
            case 5: return 'Sa'
            case 6: return 'Su'
            default: console.log(day);
        }
        console.log("Something went wrong when fetching days from the number")
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

        this.setState({allApptsToBeRendered: all})
    }

    setSemesterDates = async () => {
        await axios.get("/api/events/semester/")
        .then((res) => {
            console.log(res)
            const startYear = parseInt(res.data.start_date.slice(0, 4))
            const startMon = parseInt(res.data.start_date.slice(5, 7)) - 1
            const startDate = parseInt(res.data.start_date.slice(8, 10))

            this.setState({
                startSemDate: {
                    date: startDate,
                    month: startMon,
                    year: startYear
                },
                endSemDate: res.data.end_date.replace('-', '').replace('-', '')
            })
        })
    }

  render() {
    // const data = this.state.data;
    const data = this.state.allApptsToBeRendered;
    const views = ['day', 'week', 'month'];
    return (
        <MuiThemeProvider>
        <Paper style = {{paddingTop: 55, width:'100%'}}>
            <Scheduler
                dataSource={data}
                editing={{allowUpdating: false}}
                views={views}
                defaultCurrentView={'week'}
                showCurrentTimeIndicator={true}
                height={'80%'}
                startDayHour={7} 
                onAppointmentAdded={async (e) => {
                    console.log(e)
                    await axios.post('/api/events/user/',
                        this.formatApptSchedulerToApi(e.appointmentData),
                        {user: {userid: this.state.userid},
                        headers: {
                            'X-CSRFToken': this.state.csrf_token
                        }
                    })
                    .then((res) => {
                        console.log(res)
                        this.props.addToSchedule(res.data)
                    })
                    .catch(console.log)
                    this.forceUpdate()
                }}
                onAppointmentUpdated={async (e) => {
                    console.log(e)
                    this.forceUpdate()
                }}
                onAppointmentDeleted={async (e) => {
                    console.log(e)

                    await axios.delete(`/api/events/${e.appointmentData.id}/`,
                        this.formatApptSchedulerToApi(e.appointmentData),
                        {user: {userid: this.state.userid},
                        headers: {
                            'X-CSRFToken': this.state.csrf_token
                        }
                    })
                    .then((res) => {
                        console.log(res)
                        this.props.removeFromSchedule(e.appointmentData.id)
                    })
                    .catch(console.log)

                    this.forceUpdate()
                }}
                onAppointmentFormOpening={(data) => {
                    let form = data.form;
                    let opts = form.option("items")
                    opts = opts.filter((e) => ((!e.dataField || e.dataField !== "allDay") && 
                                                (!e.label || e.label.text !== "Repeat") &&
                                                (!e.dataField || e.dataField !== "description")))
                    // console.log(opts)
                    form.option("items", opts)

                }}>
                    <Resource
                        label={'Days'}
                        fieldExpr={'day'}
                        dataSource={this.days}
                        allowMultiple={true}
                        required={true}
                        />
                </Scheduler>
        </Paper>
        </MuiThemeProvider>
    );
  }
}
