import React from "react"

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import classNames from 'classnames';


import Calendar from '../components/Calendar'
import Navbar from "../components/Navbar";
import Menu from "../components/Menu";

import { drawerWidth } from '../consts/ui'

// dummy data
import { user } from '../consts/dummydata/user'
// import axios from "axios";


const styles = theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    padding: '0 8px',
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  },
  drawerPaper: {
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: -drawerWidth,
  },
  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  },
  toolbar: theme.mixins.toolbar,
});

class IndexPage extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            user: user,
            openDrawer: false
        }
    }

    componentDidMount() {
        // axios.get('localhost:8080/api/recurrevent/user', {user: {userid: 1}})
        // .then((res) => {console.log(res.data)})
        // .catch((err) => console.log(err))


        // get follow requests
    }

    handleDrawerOpen = () => {
        this.setState({ openDrawer: true })
    };

    handleCloseAlert = () => {}
    
    handleDrawerClose = () => {
        this.setState({ openDrawer: false })
    };

    render() {
        const { classes, theme } = this.props;
        return (
            <div className={classes.root}>
                <CssBaseline />
                <Navbar classes={classes} 
                        theme={theme}
                        user={this.state.user} 
                        handleDrawerOpen={this.handleDrawerOpen} 
                        open={this.state.openDrawer}/>
                <Menu classes = {classes} 
                        user={this.state.user} 
                        theme={theme}
                        handleDrawerClose={this.handleDrawerClose} 
                        open={this.state.openDrawer}/>
                <main className={classNames(classes.content, {
                        [classes.contentShift]: this.state.openDrawer,
                    })}>
                    <div className={classes.drawerHeader} />
                    <Calendar/>
                </main>
            </div>
        );
    }
}

IndexPage.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired
};

export default withStyles(styles, { withTheme: true })(IndexPage);
