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
import InputBase from '@material-ui/core/InputBase';
import SearchIcon from '@material-ui/icons/Search';
import DeleteIcon from '@material-ui/icons/Delete';
import AddIcon from '@material-ui/icons/Add';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';

import Notifier from "./../Notifier";
import {openSnackbar} from "./../Notifier";

import axios from 'axios';

// for csrf token
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

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
    searchIcon: {
      width: theme.spacing.unit * 9,
      height: '100%',
      position: 'absolute',
      pointerEvents: 'none',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 'small',
    },
    inputRoot: {
      color: 'inherit',
      width: '100%',
    },
    inputInput: {
      paddingTop: theme.spacing.unit,
      paddingRight: theme.spacing.unit,
      paddingBottom: theme.spacing.unit*.5,
      paddingLeft: theme.spacing.unit * 10,
      transition: theme.transitions.create('width'),
      width: '100%',
      [theme.breakpoints.up('md')]: {
        width: 200,
      },
    }
}))(MuiExpansionPanelDetails);

class ClassesDisplay extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            expanded: true,
            userid: this.props.userid,
            user: this.props.user,
            searchQuery: '',
            searchResults: [],
            addedClasses: []
        };

    }


    componentDidUpdate(prevProps) {
        if (prevProps.user !== this.props.user || prevProps.userid !== this.props.userid) {
            this.setState({user: this.props.user, userid: this.props.userid})
        }
    }

    addClassToSchedule = async (cls) => {
        if (this.isClassInSchedule(cls)) return
        await axios.post('/api/user/schedule/classes/', {
            user: {user: this.state.userid},
            body: {class: cls},
            headers: {
              'X-CSRFToken': this.props.csrf_token
            }
        })
        .then((res) => {
            openSnackbar({ message: 'Class Added!' });
        })
        .catch((err) => {
          openSnackbar({ message: 'Error' });
        })
        let arr = this.state.addedClasses
        arr.push(cls)
        this.setState({addedClasses: arr})
        this.props.refresh()
    }

    removeClassFromSchedule = async (cls) => {
        if (!this.isClassInSchedule(cls)) return
        // idk ???
    }


    classCode = (cls) => (cls.code + cls.catalog_number)

    className = (cls) => (this.classCode(cls) + ', ' + cls.section)

    classTime = (cls) => {
        let days = ''
        cls.days.forEach((day) => days += day)
        if (days.length  === 0) return ''

        return `${days} ${cls.start_time.slice(0, 5)} - ${cls.end_time.slice(0, 5)}`
    }

    getSearchResults = async () => {
        await axios.get(`/api/classes/?search=${this.state.searchQuery}`, {user: {userid: this.state.userid}})
        .then((res) => this.setState({searchResults: res.data}))
        .catch(console.log)
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

    isClassInSchedule = (cls) => {
        const name = this.className(cls)
        for (let i = 0; i < this.state.addedClasses.length; i++) {
            if (this.className(this.state.addedClasses[i]) === name) return true;
        }

        return false;
    }

    classDisplay = (cls) => (
        <div>
            <ListItem key={this.className(cls)} divider={true}>
                <ListItemText
                    primary={this.classCode(cls)}
                    secondary={
                        <React.Fragment>
                          <Typography component="span" style={{display: 'inline'}} color="textPrimary">
                            {cls.section}
                          </Typography>
                          {this.classTime(cls)}
                        </React.Fragment>
                    } />

                <ListItemSecondaryAction>
                    {this.isClassInSchedule(cls)?
                    <IconButton aria-label="delete" onClick={()=>console.log(cls)}>
                    </IconButton>
                    :
                    <IconButton aria-label="add" onClick={()=>this.addClassToSchedule(cls)}>
                        <AddIcon />
                    </IconButton>
                    }
                </ListItemSecondaryAction>
            </ListItem>
        </div>
    )

    render() {
        const { classes } = this.props
        return (
            <div>
                <ExpansionPanel
                    square
                    expanded={this.state.expanded}
                    onChange={this.handleChange()}
                >
                    <ExpansionPanelSummary>
                        <Typography>Classes</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <div>

                            <SearchIcon  fontSize = {'small'}/>
                            <InputBase
                                placeholder="Search for classes…"
                                // classes={{
                                //     root: classes.inputRoot,
                                //     input: classes.inputInput,
                                // }}
                                onChange={(event)=>{
                                    this.setState({searchQuery: event.target.value})
                                }}
                                onKeyPress= {(e) => {
                                    if (e.key === 'Enter') {
                                    console.log('Enter key pressed');
                                    this.getSearchResults()
                                    }
                                }}
                            />
                            <List>
                                {this.state.searchResults.map(this.classDisplay)}
                            </List>

                        </div>
                        <div>


                        </div>
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            </div>
        );
}
}

export default ClassesDisplay;
