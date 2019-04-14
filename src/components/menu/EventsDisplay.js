import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import MuiExpansionPanel from '@material-ui/core/ExpansionPanel';
import MuiExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import MuiExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import events from '../../consts/dummydata/events'
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

const ExpansionPanel = withStyles({
  root: {
    border: '1px solid rgba(0,0,0,.125)',
    boxShadow: 'none',
    '&:not(:last-child)': {
      borderBottom: 0,
    },
    '&:before': {
      display: 'none',
    },
  },
  expanded: {
    margin: 'auto',
  },
})(MuiExpansionPanel);

const ExpansionPanelSummary = withStyles({
  root: {
    backgroundColor: 'rgba(0,0,0,.03)',
    borderBottom: '1px solid rgba(0,0,0,.125)',
    marginBottom: -1,
    minHeight: 56,
    '&$expanded': {
      minHeight: 56,
    },
  },
  content: {
    '&$expanded': {
      margin: '12px 0',
    },
  },
  expanded: {},
})(props => <MuiExpansionPanelSummary {...props} />);

ExpansionPanelSummary.muiName = 'ExpansionPanelSummary';

const ExpansionPanelDetails = withStyles(theme => ({
  root: {
    padding: theme.spacing.unit * 2,
  },
}))(MuiExpansionPanelDetails);

class EventsDisplay extends React.Component {
    constructor(props) {
        super(props)
        let arr = []
        for (let i = 0; i < events.length; i++) arr.push(false)
        this.state = {
            expanded: false,
            events: events,
            openAlert: arr
        };

    }

    handleClose = (index) => {
        let copy = JSON.parse(JSON.stringify(this.state.openAlert))
        copy[index] = false;
        this.setState({openAlert: copy})
    }

    handleChange = () => (event) => {
        this.setState({
            expanded: !this.state.expanded,
        });
    };

    render() {
        return (
            <div>
                <ExpansionPanel
                    square
                    expanded={this.state.expanded}
                    onChange={this.handleChange()}
                    >
                    <ExpansionPanelSummary>
                        <Typography>Events</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <List>
                            {this.state.events.map((event, index) => 
                                (<div key={event['id']}  divider={true}>
                                    <ListItem>
                                        <ListItemText primary={event['title']} secondary={event['location']}/>
                                        <Dialog
                                            open={this.state.openAlert[index]}
                                            onClose={() => this.handleClose(index)}
                                            aria-labelledby="alert-dialog-title"
                                            aria-describedby="alert-dialog-description"
                                        >
                                            <DialogTitle id={`alert-dialog-title-${index}`}>{event['title']}</DialogTitle>
                                            <DialogContent>
                                                <DialogContentText id={`alert-dialog-description-${index}`}>
                                                    {/* <Typography>{event['description']}</Typography> */}
                                                </DialogContentText>
                                            </DialogContent>
                                            <DialogActions>
                                                <Button onClick={() => this.handleClose(index)} color="primary">
                                                    Close
                                                </Button>
                                                {group['admin'][0]['netid'] === this.props.netid?
                                                    <div>
                                                        <Button onClick={() => this.handleRemove(index)} color="secondary" autoFocus>
                                                            Remove Group 
                                                        </Button>
                                                        <Button onClick={() => this.handleCreateEvent(index)} color="default" autoFocus>
                                                            Create Event
                                                        </Button>
                                                    </div>
                                                    :
                                                    <div></div>
                                                }
                                            </DialogActions>
                                        </Dialog>
                                        <ListItemSecondaryAction>
                                            <IconButton aria-label="info" onClick={()=>{
                                                let copy = JSON.parse(JSON.stringify(this.state.openAlert))
                                                copy[index] = true;
                                                this.setState({openAlert: copy})
                                            }}>
                                                <InfoIcon />
                                            </IconButton>
                                        </ListItemSecondaryAction>
                                    </ListItem>
                                </div>))}
                        </List>
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </div>
        );
    }
}

export default EventsDisplay;