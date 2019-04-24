import React from 'react';

import { fade } from '@material-ui/core/styles/colorManipulator';
import { withStyles } from '@material-ui/core/styles';

import InputBase from '@material-ui/core/InputBase';
import SearchIcon from '@material-ui/icons/Search';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';

import axios from 'axios';

// test
// axios.defaults.headers['X-CSRFTOKEN'] = this.props.csrf_token;
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true


const styles = theme => ({
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing.unit * 2,
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing.unit * 3,
      width: 'auto',
    },
  },
  searchIcon: {
    width: theme.spacing.unit * 9,
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inputRoot: {
    color: 'inherit',
    width: '100%',
  },
  inputInput: {
    paddingTop: theme.spacing.unit,
    paddingRight: theme.spacing.unit,
    paddingBottom: theme.spacing.unit,
    paddingLeft: theme.spacing.unit * 10,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: 200,
    },
  }
});

class SearchBar extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            searchResults: [],
            query: '',
            userid: props.userid
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.userid !== this.props.userid) {
            this.setState({userid: this.props.userid})
        }
    }



    followUser = async (userid) => {
        // axios.defaults.headers['X-CSRFTOKEN'] = this.props.csrf_token;
        // axios.defaults.xsrfCookieName = 'csrftoken'
        // axios.defaults.xsrfHeaderName = 'X-CSRFToken'
        // axios.defaults.withCredentials = true
        console.log(this.props.csrf_token)
        await axios.put(`/api/follow/${userid}/`, {
            user: {userid: this.state.userid},
            // csrfmiddlewaretoken: this.props.csrf_token // this didn't work
            // 'X-CSRFToken': this.props.csrf_token
            headers: {
              'X-CSRFToken': this.props.csrf_token
            }
        },
        )
        .then((res) => console.log(res))
        .catch((err) => console.log(err))
    }

    getName = (student) => {
        let sign = ""
        if (student['id'] === this.state.userid) sign += "You"
        else {
            sign += student["first_name"]
            sign += " "
            sign += student["last_name"]
            sign += " '"
            sign += (student["class_year"] % 100)
        }
        return sign
    }

    handleClickOpen = async () => {
        await this.onSearch()
        this.setState({ open: true });
        console.log(this.state.searchResults)
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    onSearch = async () => {
        await axios.get(`/api/user/?search=${this.state.query}`)
        .then((res) => this.setState({searchResults: res.data}))
        .catch((err) => console.log(err))
    }

    renderResults = () =>
    {
        return(
            <List>
                {this.state.searchResults.map((user) => (
                    <ListItem key={user.id}>
                        <ListItemText>{this.getName(user)}</ListItemText>
                        <ListItemSecondaryAction>
                            <Button variant="contained" color="primary" onClick={()=>this.followUser(user.id)}>
                                Follow
                            </Button>
                        </ListItemSecondaryAction>
                    </ListItem>
                ))}
            </List>
        )
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.search}>
                <div className={classes.searchIcon}>
                    <SearchIcon />
                </div>
                <InputBase
                    placeholder="Search…"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                    onChange={(event)=>{
                        this.setState({query: event.target.value})
                    }}
                    onKeyPress= {(e) => {
                        if (e.key === 'Enter') {
                          console.log('Enter key pressed');
                          this.handleClickOpen()
                        }
                    }}
                />
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          scroll="paper"
          aria-labelledby="scroll-dialog-title"
          maxWidth='xs'
          fullWidth={true}
        >
          <DialogTitle id="scroll-dialog-title">Search Results</DialogTitle>
          <DialogContent>

                {this.state.searchResults.length === 0?
                    <DialogContentText> No results found.</DialogContentText>
                :
                    this.renderResults()
                }

          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} variant="outlined" color="secondary">
              Cancel
            </Button>
          </DialogActions>
        </Dialog>
        </div>
        );
    }
}



export default withStyles(styles)(SearchBar);
