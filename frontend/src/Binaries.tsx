import React from 'react';
import './App.css';
import {List} from 'rsuite';
import api from './api';


class App extends React.Component {
  state = {
    files: [] as string[]
  }
  componentDidMount() {
    api.binaries().then((res) => {
      let files = res.data.data
      this.setState({files})
    })
  }
  render() {
    return (
      <div>
        <List>
          {this.state.files.map((item, index) => {
             return (<List.Item key={index} index={index}>
                  <a href={api.HOST + item} target='_blank'>
                     {item.split('/')[item.split('/').length - 1]}
                  </a>
                </List.Item>)
          })}
        </List>


      </div>
    );
  }
}

export default App;
