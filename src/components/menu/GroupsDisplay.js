import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import MuiExpansionPanel from '@material-ui/core/ExpansionPanel';
import MuiExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import MuiExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import IconButton from '@material-ui/core/IconButton';
import InfoIcon from '@material-ui/icons/Info';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

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

class GroupsDisplay extends React.Component {
    constructor(props) {
        super(props)
        let arr = []
        for (let i = 0; i < props.groups.length; i++) arr.push(false)
        this.state = {
            expanded: false,
            groups: props.groups,
            openAlert: arr
        };

    }
    

    componentDidUpdate(prevProps) {
        if (prevProps.groups !== this.props.groups) {
            let arr = []
            for (let i = 0; i < this.props.groups.length; i++) arr.push(false)
            this.setState({groups: this.props.groups, openAlert: arr})
        }
    }

    membersList = (group) => {
        let isFirst = true
        let list = ""
        group['members'].forEach(member => {
            if (isFirst) isFirst = false
            else list += ", "
            list += this.getName(member)
        })
        return list
    }
    
    handleChange = () => (event) => {
        this.setState({
            expanded: !this.state.expanded,
        });
    };

    handleClose = (index) => {
        let copy = JSON.parse(JSON.stringify(this.state.openAlert))
        copy[index] = false;
        this.setState({openAlert: copy})
    }

    handleRemove = (index) => {
        this.handleClose(index)
    }

    handleCreateEvent = (index) => {
        this.handleClose(index)
    }

    getSignature = admin => {
        let sign = "Created by "
        sign += this.getName(admin)
        sign += "."
        return sign
    }

    getName = (student) => {
        let sign = ""
        if (student['netid'] === this.props.netid) sign += "You"
        else {
            sign += student["first_name"]
            sign += " "
            sign += student["last_name"]
            sign += " '"
            sign += (student["class_year"] % 100)
        }
        return sign
    }
 
    render() {
        return (
            <div>
                <ExpansionPanel
                    square
                    expanded={this.state.expanded}
                    onChange={this.handleChange()}
                >
                    <ExpansionPanelSummary>
                        <Typography>Groups</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <List>
                            {this.state.groups.map((group, index) => (
                                <ListItem key={group['groupid']} divider={true}>
                                    <ListItemText primary={group['name']} secondary={this.getSignature(group['admin'][0])}/>
                                    <Dialog
                                        open={this.state.openAlert[index]}
                                        onClose={() => this.handleClose(index)}
                                        aria-labelledby="alert-dialog-title"
                                        aria-describedby="alert-dialog-description"
                                    >
                                        <DialogTitle id={`alert-dialog-title-${index}`}>{group['name']}</DialogTitle>
                                        <DialogContent>
                                            <DialogContentText id={`alert-dialog-description-${index}`}>
                                                <Typography>{this.membersList(group)}</Typography>
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
                            ))}
                        </List>
                        
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </div>
        );
}
}

export default GroupsDisplay;