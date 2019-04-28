import React from 'react';
import Snackbar from 'material-ui/Snackbar';

let openSnackbarFn;

const styles = theme => ({
  root: {
    position: 'absolute',
    right: '100px'
  },
  snackbar: {
    position: 'absolute',
  }
});

class Notifier extends React.Component {
  state = {
    open: false,
    message: ''
  };

  componentDidMount() {
    openSnackbarFn = this.openSnackbar;
  }

  handleSnackbarClose = () => {
    this.setState({
      open: false,
      message: '',
    });
  };

  openSnackbar = ({ message }) => {
    this.setState({ open: true, message });
  };


render() {
  const message = (
      <span
        id="snackbar-message-id"
        dangerouslySetInnerHTML={{ __html: this.state.message }} />
    );
return (
      <Snackbar
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        message={message}
        autoHideDuration={3000}
        onRequestClose={this.handleSnackbarClose}
        open={this.state.open}
        SnackbarContentProps={{
          'aria-describedby': 'snackbar-message-id',
        }}
      />
    );
  }
}

export function openSnackbar({ message }) {
  openSnackbarFn({ message });
}

export default Notifier;
