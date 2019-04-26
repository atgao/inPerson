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
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';
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
        padding: 20,
    },
}))(MuiExpansionPanelDetails);

class FollowerDisplay extends React.Component {
    constructor(props) {
        super(props)
        let arr = []
        for (let i = 0; i < this.props.user['connections']['followers'].length; i++) arr.push(false)
        this.state = {
            expanded: false,
            user: this.props.user,
            openAlert: arr
        };

    }
    

    componentDidUpdate(prevProps) {
        if (prevProps.user !== this.props.user) {
            let arr = []
            for (let i = 0; i < this.props.user['connections']['followers'].length; i++) arr.push(false)
            this.setState({user: this.props.user, openAlert: arr})
        }
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
        this.props.removeFollower(this.props.user['connections']['followers'][index].id)
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

    userDisplay = (connection, index) => (
        <div>
            <ListItem key={connection['netid']} divider={true}>
                <ListItemText primary={this.getName(connection)} secondary={connection['netid']}/>
                <Dialog
                    open={this.state.openAlert[index]}
                    onClose={() => this.handleClose(index)}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                >
                    <DialogTitle id={`alert-dialog-title-${index}`}>{this.getName(connection)}</DialogTitle>
                    <DialogContent>
                        <DialogContentText id={`alert-dialog-description-${index}`}>
                            Are you sure you want to remove this follower?
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleRemove(index)} color="secondary">
                            Yes
                        </Button>
                        <Button onClick={() => this.handleClose(index)} color="primary">
                            No
                        </Button>
                    </DialogActions>
                </Dialog>
                <ListItemSecondaryAction>
                    <IconButton aria-label="info" onClick={()=>{
                        let copy = JSON.parse(JSON.stringify(this.state.openAlert))
                        copy[index] = true;
                        this.setState({openAlert: copy})
                    }}>
                        <DeleteIcon />
                    </IconButton>
                </ListItemSecondaryAction>
            </ListItem>
        </div>
    )
 
    render() {
        return (
            <div>
                <ExpansionPanel
                    square
                    expanded={this.state.expanded}
                    onChange={this.handleChange()}
                >
                    <ExpansionPanelSummary>
                        <Typography>Followers</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <List>
                            {this.state.user['connections']['followers'].map((connection, index) => this.userDisplay(connection, index))}
                        </List>
                        
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </div>
        );
}
}

export default FollowerDisplay;