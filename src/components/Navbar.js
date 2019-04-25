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

class Navbar extends React.Component {
    state = {
        anchorEl: null,
        mobileMoreAnchorEl: null,
        open: this.props.open,
        user: this.props.user,
        csrf_token: this.props.csrf_token,
        followRequests: [],
        followRequestsUsers: [],
        noFollowReqs: 0
    };
    
    async componentDidUpdate (prevProps) {
        if (prevProps.open !== this.props.open || 
            prevProps.user !== this.props.user || 
            prevProps.csrf_token !== this.props.csrf_token ||
            prevProps.followRequests !== this.props.followRequests) {
                if (prevProps.followRequests !== this.props.followRequests) {
                    const arr = this.populateReqsUsers()
                    this.setState({
                        open: this.props.open, 
                        user: this.props.user, 
                        csrf_token: this.props.csrf_token,
                        followRequests: this.props.followRequests,
                        noFollowReqs: this.props.followRequests.length,
                        followRequestsUsers: arr
                    })

                    return
                }
                this.setState({
                    open: this.props.open, 
                    user: this.props.user, 
                    csrf_token: this.props.csrf_token,
                })
        }
    }

    handleProfileMenuOpen = event => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleMenuClose = () => {
        this.setState({ anchorEl: null });
        this.handleMobileMenuClose();
    };

    handleMobileMenuOpen = event => {
        this.setState({ mobileMoreAnchorEl: event.currentTarget });
    };

    handleMobileMenuClose = () => {
        this.setState({ mobileMoreAnchorEl: null });
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
        return arr 
    }

    renderFollowReq = (req) =>{

        return (
            <MenuItem></MenuItem>
        )
    }

    render() {
        const { anchorEl, mobileMoreAnchorEl } = this.state;
        const { classes } = this.props;
        const isMenuOpen = Boolean(anchorEl);
        const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

        const renderMenu = (
        <Menu
            anchorEl={anchorEl}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={isMenuOpen}
            onClose={this.handleMenuClose}
        >
            {/* <MenuItem onClick={this.handleMenuClose}>{this.state.user.first_name} {this.state.user.last_name} '{(''+this.state.user.class_year).slice(2)}</MenuItem> */}
            <MenuItem onClick={() => window.location.pathname = '/accounts/logout'}>Logout</MenuItem>
        </Menu>
        );

        const renderMobileMenu = (
        <Menu
            anchorEl={mobileMoreAnchorEl}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={isMobileMenuOpen}
            onClose={this.handleMenuClose}
        >
            {/* <MenuItem onClick={this.handleMobileMenuClose}>
            <IconButton color="inherit">
                <Badge badgeContent={4} color="secondary">
                <MailIcon />
                </Badge>
            </IconButton>
            <p>Messages</p>
            </MenuItem> */}
            <MenuItem onClick={this.handleMobileMenuClose}>
                <IconButton color="inherit">
                    {this.noFollowReqs === 0?
                    <Badge badgeContent={this.noFollowReqs} color="secondary">
                        <NotificationsIcon />
                    </Badge>
                    :
                    <NotificationsIcon />
                    }
                </IconButton>
                <p>Folllow Requests</p>
            </MenuItem>
            <MenuItem onClick={this.handleProfileMenuOpen}>
                <IconButton color="inherit">
                    <AccountCircle />
                </IconButton>
                <p>{this.state.user.first_name}</p>
            </MenuItem>
        </Menu>
        );

        return (
        <div className={classes.appBar}>
            <AppBar position="fixed" 
                className={classNames(classes.appBar, {
                    [classes.appBarShift]: this.state.open,
                })}>
            <Toolbar disableGutters={!this.state.open}>
                <IconButton
                    color="inherit"
                    aria-label="Open drawer"
                    onClick={this.props.handleDrawerOpen}
                    className={classNames(classes.menuButton, this.state.open && classes.hide)}
                    >
                    <MenuIcon />
                </IconButton>
                <Typography className={classes.title} variant="h6" color="inherit" noWrap>
                inPerson
                </Typography>
                <SearchBar classes = {classes} csrf_token={this.state.csrf_token}/>
                <div className={classes.grow} />
                <div className={classes.sectionDesktop}>
                {/* <IconButton color="inherit">
                    <Badge badgeContent={4} color="secondary">
                    <MailIcon />
                    </Badge>
                </IconButton> */}
                <IconButton color="inherit" onClick={this.handleProfileMenuOpen}>
                    {this.state.noFollowReqs !== 0?
                    <Badge badgeContent={this.state.noFollowReqs} color="secondary">
                        <NotificationsIcon />
                    </Badge>
                    :
                    <NotificationsIcon />
                    }
                </IconButton>
                <Button
                    aria-owns={isMenuOpen ? 'material-appbar' : undefined}
                    aria-haspopup="true"
                    onClick={this.handleProfileMenuOpen}
                    color="inherit"
                >
                    {this.state.user.first_name}
                </Button>
                </div>
                <div className={classes.sectionMobile}>
                <IconButton aria-haspopup="true" onClick={this.handleMobileMenuOpen} color="inherit">
                    <MoreIcon />
                </IconButton>
                </div>
            </Toolbar>
            </AppBar>
            {renderMenu}
            {renderMobileMenu}
        </div>
        );
    }
}

Navbar.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(Navbar);
