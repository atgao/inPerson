import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Badge from '@material-ui/core/Badge';
import Button from '@material-ui/core/Button';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import { fade } from '@material-ui/core/styles/colorManipulator';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import AccountCircle from '@material-ui/icons/AccountCircle';
import NotificationsIcon from '@material-ui/icons/Notifications';
import MoreIcon from '@material-ui/icons/MoreVert';
import MenuIcon from '@material-ui/icons/Menu';

import SearchBar from './navbar/SearchBar';

import { drawerWidth } from '../consts/ui'
import axios from 'axios';

const styles = theme => ({
    root: {
        width: '100%',
    },
    appBar: {
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: drawerWidth,
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
        display: 'block',
        },
    },
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
    },
    sectionDesktop: {
        display: 'none',
        [theme.breakpoints.up('md')]: {
            display: 'flex',
        },
    },
    sectionMobile: {
        display: 'flex',
        [theme.breakpoints.up('md')]: {
            display: 'none',
        },
    },
});

class AccountMenu extends React.Component {
    state = {
        anchorEl: null,
        open: this.props.open,
        csrf_token: this.props.csrf_token,
        followRequestsUsers: [],
        noFollowReqs: 0
    };
    
    async componentDidUpdate (prevProps) {
        if (prevProps.open !== this.props.open || 
            prevProps.csrf_token !== this.props.csrf_token ) {
                this.setState({
                    open: this.props.open, 
                    csrf_token: this.props.csrf_token,
                    followRequests: this.props.followRequests,
                    noFollowReqs: this.props.followRequests.length
                })
        }
    }

    handleProfileMenuOpen = event => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleMenuClose = () => {
        this.setState({ anchorEl: null });
    };

    populateReqsUsers = async () => {
        let arr = []
        await this.state.followRequests.forEach(async (req, index) => {
            console.assert((req.to_user+'') === (this.props.userid+''))
            await axios.get(`/api/user/${req.from_user}`, {user:{userid: this.props.userid}})
            .then ((res) => arr.push({
                user: res.data,
                index: index
            }))
        })
        this.setState({followRequestsUsers: arr})
    }

    renderFollowReq = (req) =>{

        return (
            <MenuItem></MenuItem>
        )
    }

    render() {
        const { anchorEl } = this.state;
        const isMenuOpen = Boolean(anchorEl);

        const renderMenu = (
        <Menu
            anchorEl={anchorEl}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={isMenuOpen}
            onClose={this.handleMenuClose}
        >
            <MenuItem onClick={() => window.location.pathname = '/accounts/logout'}>Logout</MenuItem>
        </Menu>
        );

        return (
        <div>
            <Button
                aria-owns={isMenuOpen ? 'material-appbar' : undefined}
                aria-haspopup="true"
                onClick={this.handleProfileMenuOpen}
                color="inherit"
            >
                {this.state.user.first_name}
            </Button>
            {renderMenu}
        </div>
        );
    }
}


export default withStyles(styles, { withTheme: true })(AccountMenu);
