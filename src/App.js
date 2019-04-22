import React, { Component } from 'react';
import './App.css';

import CssBaseline from '@material-ui/core/CssBaseline';


import Calendar from './components/Calendar'
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";

import { drawerWidth } from './consts/ui'

// dummy data
import { user } from './consts/dummydata/user'
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
            connection: {
                followers: [],
                following: []
            }
        }
        this.state = {
            userid: null,
            // user: emptyUser,
            user: user,
            openDrawer: false
        }
    }

    componentDidMount() {
        if (this.state.userid === null) {
            console.log("updating userid...")
            let userid = document.getElementById("userid").textContent
            console.log(userid)
            this.setState({userid: userid})
            console.log("updated userid!")
            let user = this.state.user
            axios.get(`/api/user/${userid}`,)
            .then((res) => {
                Object.assign(user, res.data)
                // user['connections'] = {}
                axios.get("/api/user/followers", {user:{ userid: userid }})
                .then((res) => 
                {
                    user['connections']['followers'] = res.data
                    console.log(user)
                })
                .catch((err) => console.log(err))

                axios.get("/api/user/following", {user:{ userid: userid }})
                .then((res) => 
                {
                    user['connections']['following'] = res.data
                    console.log(user)
                })
                .catch((err) => console.log(err))

                return user;
                
            })
            .then((user) => {
                console.log("Updating user")
                console.log(user)
                // this.setState({user:user})
                console.log("user updated")
            })
            .catch((err) => console.log(err))
        }
        else {
            console.log("User already set in state")
            console.log(this.state.userid)
            console.log(this.state.user)
        }
        
        


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
    return (
      <div className="App">
        <CssBaseline />
        <Navbar user={this.state.user} 
                handleDrawerOpen={this.handleDrawerOpen} 
                open={this.state.openDrawer}/>
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

export default App;
