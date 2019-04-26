import React, { Component } from 'react';
import './App.css';
import classNames from 'classnames';

import CssBaseline from '@material-ui/core/CssBaseline';
import { withStyles } from '@material-ui/core/styles';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'


import Calendar from './components/Calendar'
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";
import Notifier from "./components/Notifier";
import {openSnackbar} from "./components/Notifier";

import { drawerWidth } from './consts/ui'
import axios from "axios";

// for csrf token
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

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
      marginLeft: 0,
    },
    contentShift: {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: drawerWidth,
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
            frSent: [],
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
                await this.getFollower(user, userid)

                await this.getFollowing(user, userid)

                return user;
            })
            .then((user) => {
                this.setState({
                    user:user,
                    userid: userid,
                    csrf_token: csrf_token
                })
            })
            .then(async () => {
                await axios.get('/api/user/requests', {user: {userid:userid}})
                .then((res) => {
                    this.setState({followRequests: res.data})
                })
                .catch((err) => console.log(err))

            })
            .then(async () => {
                await axios.get('/api/user/requests/sent', {user: {userid:userid}})
                .then((res) => {
                    let arr = []
                    res.data.forEach((req) => arr.push(req.to_user))
                    this.setState({frSent: arr})
                })
                .catch((err) => console.log(err))

            })
            .catch((err) => console.log(err))
        }
        else {
            console.log("User already set in state") // shouldn't happen
        }
    }


    acceptFollowRequest = async (userid) => {
        await axios.post(`/api/user/requests/${userid}/`,
            {user: {userid: this.state.userid},
            headers: {
                'X-CSRFToken': this.state.csrf_token
            }
        })
        .then(console.log)
        .catch(console.log)

        this.removeFollowRequest(userid)

        let user = this.state.user
        // await this.getFollower(user, this.state.userid)
        let follower = await this.getUser(userid)
        user['connections']['followers'].push(follower)
        this.setState({user})

    };

    cantFollow = (userid) => { // returns 0 if can follow, 2 if following, 1 if follow request sent

        for (let i = 0; i < this.state.user.connections.following.length; i++) {
            if((userid+'') === (this.state.user.connections.following[i].id+'')) return 2
        }
        for (let i = 0; i < this.state.frSent.length; i++) {
            if((userid+'') === (this.state.frSent[i]+'')) return 1
        }
        return 0
    }

    deleteFollowRequest = async (userid) => {
        await axios.delete(`/api/follow/${userid}`, {
            user: {userid: this.state.userid},
            headers: {
                'X-CSRFToken': this.state.csrf_token
            }
        })
        .then(console.log)
        .catch(console.log)

        this.removeFollowRequest(userid)
    }

    followUser = async (userid) => {
        await axios.put(`/api/follow/${userid}/`, {
            user: {userid: this.state.userid},
            headers: {
              'X-CSRFToken': this.props.csrf_token
            }
        },
        )
        .then((res) => {
            let arr = this.state.frSent;
            arr.push(userid)
            this.setState({frSent: arr})
          openSnackbar({ message: 'Request Sent!' });
        })
        .catch((err) => {
          openSnackbar({ message: 'Error' });
        })
    }

    getFollower = async (user, userid) => {
        await axios.get("/api/user/followers", {user:{ userid: userid }})
        .then((res) =>
        {
            let arr = []
            res.data.forEach(async (req) => {
                let follower = await this.getUser(req.follower)
                arr.push(follower)
            })
            user['connections']['followers'] = arr
        })
        .catch((err) => console.log(err))
    }

    getFollowing = async (user, userid) => {
        await axios.get("/api/user/following", {user:{ userid: userid }})
        .then((res) =>
        {
            let arr = []
            res.data.forEach(async (req) => {
                let followee = await this.getUser(req.followee)
                arr.push(followee)
            })
            user['connections']['following'] = arr
        })
        .catch((err) => console.log(err))
    }

    getUser = async (userid) => {
        let user = {}
        await axios.get(`/api/user/${userid}`, {user:{userid: this.state.userid}})
        .then ((res) => {
            user = res.data
        })
        .catch((err) => console.log("OH NO ERROR ERROR WTF WENT WRONG"))
        return user
    }


    handleDrawerOpen = () => {
        this.setState({ openDrawer: true })
    };


    handleDrawerClose = () => {
        this.setState({ openDrawer: false })
    };

    removeFollower = async (userid) => {
        await axios.delete(`/api/remove/${userid}`, {
            user: {userid: this.state.userid},
            headers: {
                'X-CSRFToken': this.state.csrf_token
            }
        })
        .then(console.log)
        .catch(console.log)

        let user = this.state.user
        user.connections.followers = user.connections.followers.filter((user) => user.id !== userid)
        this.setState({user})
    }

    removeFollowing = async (userid) => {
        await axios.delete(`/api/unfollow/${userid}`, {
            user: {userid: this.state.userid},
            headers: {
                'X-CSRFToken': this.state.csrf_token
              }
        })
        .then(console.log)
        .catch(console.log)

        let user = this.state.user
        user.connections.following = user.connections.following.filter((user) => user.id !== userid)
        this.setState({user})
    }

    removeFollowRequest = (userid) => {
        let arr = this.state.followRequests
        arr = arr.filter(e => e.from_user !== userid)
        this.setState({followRequests: arr})
    }



  render() {
    const { classes, theme } = this.props;
    return (
      <div className="App">
      <MuiThemeProvider>
        <CssBaseline />
            <Navbar user={this.state.user}
                    userid={this.state.userid}
                    handleDrawerOpen={this.handleDrawerOpen}
                    open={this.state.openDrawer}
                    followRequests={this.state.followRequests}
                    acceptFollowRequest={this.acceptFollowRequest}
                    deleteFollowRequest={this.deleteFollowRequest}
                    followUser={this.followUser}
                    cantFollow={this.cantFollow}
                    csrf_token={this.state.csrf_token} />
            <Menu user={this.state.user}
                    userid={this.state.userid}
                    handleDrawerClose={this.handleDrawerClose}
                    csrf_token={this.state.csrf_token}
                    open={this.state.openDrawer}
                    removeFollower={this.removeFollower}
                    removeFollowing={this.removeFollowing}/>

            {/*<main style={Object.assign({}, styles.content, this.state.openDrawer? styles.contentShift: {})}> */}
            <main className={classNames(classes.content, {
            [classes.contentShift]: this.state.openDrawer,
          })}>
                <div style={styles.drawerHeader} />
                <Calendar/>
            </main>
            <Notifier />
        </MuiThemeProvider>
      </div>


    );
  }
}

export default withStyles(styles)(App);
