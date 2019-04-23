import React from 'react';
import InputBase from '@material-ui/core/InputBase';
import { fade } from '@material-ui/core/styles/colorManipulator';
import { withStyles } from '@material-ui/core/styles';
import SearchIcon from '@material-ui/icons/Search';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import axios from 'axios';


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
            userid: props.userid
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.userid !== this.userid) {
            this.setState({userid: this.props.userid})
        }
    }

    onSearch = async (query) => {
        await axios.get(`/api/user/?search=${query}`)
        .then((res) => this.setState({searchResults: res.data}))
        .catch((err) => console.log(err))
    }

    followUser = async (userid) => {
        await axios.put(`/api/follow/${userid}`, {user: {userid: this.state.userid}})
        .then((res) => console.log(res))
        .catch((err) => console.log(err))
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
                />
                <Button onClick={this.handleClickOpen('body')}>scroll=body</Button>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          scroll={this.state.scroll}
          aria-labelledby="scroll-dialog-title"
        >
          <DialogTitle id="scroll-dialog-title">Subscribe</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac
              facilisis in, egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum
              at eros. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus
              sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum
              nulla sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur
              et. Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla. Cras
              mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
              egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
              Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus sagittis
              lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum nulla
              sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
              Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla. Cras mattis
              consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
              egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
              Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus sagittis
              lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum nulla
              sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
              Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla. Cras mattis
              consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
              egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
              Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus sagittis
              lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum nulla
              sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
              Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla. Cras mattis
              consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
              egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
              Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus sagittis
              lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum nulla
              sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
              Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla. Cras mattis
              consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
              egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
              Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Vivamus sagittis
              lacus vel augue laoreet rutrum faucibus dolor auctor. Aenean lacinia bibendum nulla
              sed consectetur. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.
              Donec sed odio dui. Donec ullamcorper nulla non metus auctor fringilla.
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleClose} color="primary">
              Subscribe
            </Button>
          </DialogActions>
        </Dialog>
        </div>
        );
    }
}



export default withStyles(styles)(SearchBar);
