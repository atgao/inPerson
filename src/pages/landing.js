import React from "react"
import axios from "axios";

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/button'
import Image from '../images/background.jpeg'

import { domain } from '../consts/utils'


const styles = theme => ({
    root: {
        display: 'flex',
        flex: 1,
        flexDirection: 'column',
        backgroundImage: `url(${Image})`, 
        backgroundPosition: 'center',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        height: '100vh',
        alignItems: 'center',
        justifyContent: 'center',
        color:'white'
    },
    button: {
        margin: theme.spacing.unit,
        height: 45,
        color:'white',
        fontSize: 22,
        backgroundColor: 'orange'
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing.unit * 3,
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    toolbar: theme.mixins.toolbar,
});

class LandingPage extends React.Component {
    handleError = (err) => {
        // !!!!!!!!!!!!!!!!!!!!!!
        // !!! DEAL WITH THIS !!!
        // !!!!!!!!!!!!!!!!!!!!!!
        // alert(err)
        console.log(err)
    }
    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root} >
                <p style={{ fontSize: 40}}>Welcome to inPerson!</p>
                <p>
                    <Button variant="outlined" color='inherit' className={classes.button} onClick={()=>{
                        // if (typeof(Storage) !== "undefined" && localStorage.getItem("userid") !== null) {
                        //     alert("already logged in")
                        // }
                        // else {
                            axios.post('/login')
                            .then((res) => {
                                
                                
                                //
                                //
                                // settle CAS here
                                //
                                //
                                const userid = 1
                                // request server for more info
                                localStorage.setItem("userid", userid)

                                // axios.get('/api/user',  {
                                axios.get('localhost:8080/api/user',  {
                                    user: {
                                        userid: userid
                                    }
                                }).then((res) => {
                                    alert("here")
                                    if (res.status === 200) {
                                        console.log(res.data)
                                    }
                                })
                                .catch(this.handleError)
                            })
                            .catch(this.handleError)

                        // }
                        window.location.assign("/")
                    }}>
                        Click here to login
                    </Button>
                </p>
            </div>
        );
    }
}

LandingPage.propTypes = {
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired
};

export default withStyles(styles, { withTheme: true })(LandingPage);
