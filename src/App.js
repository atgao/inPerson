import React, { Component } from 'react';
import './App.css';

import CssBaseline from '@material-ui/core/CssBaseline';


import Calendar from './components/Calendar'
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";

import { drawerWidth } from './consts/ui'

// dummy data
import { user } from './consts/dummydata/user'
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

class App extends Component {
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
