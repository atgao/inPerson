import React, { Component } from 'react';
import './App.css';

import CssBaseline from '@material-ui/core/CssBaseline';
import { withStyles } from '@material-ui/core/styles';


import Calendar from './components/Calendar'
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";

import { drawerWidth } from './consts/ui'
import axios from "axios";

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

class App extends Component {
    constructor(props) {
        super(props)
        const emptyUser = {
            netid: '',
            first_name: '',
            last_name: '',
            class_year: '',
            connections: {
                followers: [],
                following: []
            }
        }
        this.state = {
            userid: null,
            user: emptyUser,
            csrf_token: null,
            followRequests: [],
            openDrawer: false
        }
    }

    componentDidMount() {
        if (this.state.userid === null || this.state.user.netid.length === 0 || this.state.csrf_token === null) {
            const userid = document.getElementById("userid").textContent
            let user = this.state.user
            const csrf_token = document.getElementById("csrf_token").textContent

            axios.get(`/api/user/${userid}`,)
            .then(async (res) => {
                Object.assign(user, res.data)
                await axios.get("/api/user/followers", {user:{ userid: userid }})
                .then((res) => 
                {
                    user['connections']['followers'] = res.data
                })
                .catch((err) => console.log(err))

                await axios.get("/api/user/following", {user:{ userid: this.state.userid }})
                .then((res) => 
                {
                    user['connections']['following'] = res.data
                    user['connections']['following'].push({
                        netid: user['netid'],
                        first_name: user['first_name'],
                        last_name: user['last_name'],
                        class_year: user['class_year']
                    })
                })
                .catch((err) => console.log(err))

                return user; 
            })
            .then((user) => {
                console.log("Updating user")
                this.setState({user:user, userid: userid, csrf_token: csrf_token})
                console.log("user updated")
            })
            .catch((err) => console.log(err))
        }
        else {
            console.log("User already set in state") // shouldn't happen
        }
        // get follow requests
    }



    handleDrawerOpen = () => {
        this.setState({ openDrawer: true })
    };

    
    handleDrawerClose = () => {
        this.setState({ openDrawer: false })
    };

  render() {
    return (
      <div className="App">
        <CssBaseline />
        <Navbar user={this.state.user} 
                handleDrawerOpen={this.handleDrawerOpen} 
                open={this.state.openDrawer}
                followRequests={this.state.followRequests}
                csrf_token={this.state.csrf_token} />
        <Menu user={this.state.user} 
                handleDrawerClose={this.handleDrawerClose} 
                open={this.state.openDrawer}/>
        <main style={Object.assign({}, styles.content, this.state.openDrawer? styles.contentShift: {})}>
            <div style={styles.drawerHeader} />
            <Calendar/>
        </main>
      </div>
    );
  }
}

export default withStyles(styles)(App);
