import React from 'react';
import './App.css';
import {  FormGroup, ControlLabel, SelectPicker,  Button, Input, ButtonGroup } from 'rsuite';
import api from './api'

class App extends React.Component {
  ref = React.createRef() as any
  state = {
    type: 'tag',
    value: '3.0.6',
    could_exec: false
  }
  checkoutData = [
                {
                  "label": "Branch",
                  "value": "branch",
                },
                {
                  "label": "Tag",
                  "value": "tag",
                },
                {
                  "label": "Hash",
                  "value": "hash",
                },
              ]
  checkIdle() {
    api.executorState().then(res => {
      this.setState({could_exec: res.status == 200})
    }).catch(res => {
      this.setState({could_exec: false})
    })
  }
  componentDidMount() {
    this.checkIdle()
    setInterval(() => {
      this.checkIdle()
    }, 5000)

  }
  render() {
    return (
      <div>
        <form ref={this.ref} method='post' target='log' action={api.HOST + "/executor"}>
          <div style={{display: 'flex', justifyContent: 'space-between', margin: '1rem 0'}}>
          <FormGroup>
            <ControlLabel style={{marginRight: '1rem'}}>Type</ControlLabel>
            <input style={{display: "none"}} value={this.state.type} name='type'/>
            <SelectPicker
              cleanable={false}
              value={this.state.type}
              onChange={(e) => {
                this.setState({type: e})
              }}
              style={{width: 128}}
              data={this.checkoutData}/>
          </FormGroup>
          <FormGroup>
            <ControlLabel>Value</ControlLabel>
            <Input name="value" value={this.state.value} style={{width: '40vw'}}
              onChange={e => {
                this.setState({value: e})
              }}
            />
          </FormGroup>
            <ButtonGroup>
          <Button disabled={!this.state.could_exec} size='sm' style={{ margin: '0, 1rem'}} appearance='primary' onClick={() => {
            this.ref.current.submit()
          }}>Submit</Button>
          <Button size='sm' style={{ margin: '0, 1rem'}} onClick={() => {
            this.setState({value: '', type: 'branch'})
          }}>Clean</Button>
          </ButtonGroup>
          </div>
        </form>
        <iframe name="log" src={api.HOST + "/log"} style={{width: '100%', height: '600px'}}/>
      </div>
    );
  }
}

export default App;
