import React from "react";
import Paper from "@material-ui/core/Paper";

import Scheduler, { Resource } from 'devextreme-react/scheduler';

import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import { blue } from "@material-ui/core/colors";
import { appointments } from "../consts/dummydata/events";

import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.material.teal.light.css';

const theme = createMuiTheme({ palette: { type: "light", primary: blue } });



export default class Calendar extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      data: appointments
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
                    console.log(form.option("items"))
                    opts = opts.filter((e) => ((!e.dataField || e.dataField !== "allDay") && (!e.label || e.label.text !== "Repeat")))
                    // opts.push({
                    //     label: {
                    //         text:'Repeat weekly on'
                    //     },
                    //     editorType: 'dxTagBox',
                    //     dataField: 'days',
                    //     editorOptions: {
                    //         items: days,
                    //         value: [0, 1, 2, 3, 4, 5, 6],
                    //         displayExpr: "text",
                    //         valueExpr: "id",
                    //         showSelectionControls: true,
                    //         maxDisplayedTags: 3
                    //     },
                    //     validationRules: [{
                    //         type: 'required'
                    //     }]
                    // })
                    console.log(opts)
                    form.option("items", opts)
                    console.log(form.option("items"))

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
