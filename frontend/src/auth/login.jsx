import React, { Component } from "react";
import { Button, FormGroup, FormControl} from "react-bootstrap";
import {getUrl, Action} from "../endpoints"

function FieldGroup({ id, label, help, ...props }) {
  return (
    <FormGroup controlId={id}>
      <FormControl {...props} />
    </FormGroup>
  );
}

export default class Login extends Component{
  constructor(props){
    super(props);
    this.state = {
      username:"",
      password:""
    }
 }

  handleChange=event=>{
    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  handleRegistration = e =>{
    e.preventDefault() ;
    let url = getUrl(Action.Register);
    let data = this.state;
    fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({'username': data.username, 'password': data.password})
    }).then( res => res.json())
    .then(data=>{
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('username', data.username);
      if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token")!=="undefined") {
        window.location.replace("/")
      }else{
          alert(data.message)
      }
    }).catch(err => console.log(err));
  }

  handleSignIn = e =>{
    e.preventDefault() ;
    let url = getUrl(Action.Login)
    let data = this.state;

    fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({'username': data.username, 'password': data.password})
    }).then( res => res.json())
    .then(data=>{
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('username', data.username);

      if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token")!=="undefined") {
        window.location.replace("/")
      }else{
          alert(data.error);
      }
    }).catch(err => console.log(err));
  }
  render(){
    return (
      <div className="LoginForm">
        <form>
          <FieldGroup
            id="formControlsEmail"
            name="username"
            label="username"
            value={this.state.username}
            onChange={this.handleChange}
            placeholder="username"
          />
          <FieldGroup
          id="formControlsPassword"
          type="password"
          name="password"
          label="Password"
          value={this.state.password}
          onChange={this.handleChange}
          placeholder="Password"
          help="Password length should be atleast 8 characters long." />
          <div className="btn-toolbar">
            <Button variant="primary" className='m-2' onClick={this.handleSignIn}  block>Log in</Button>
            <Button variant="secondary" className='m-2' onClick={this.handleRegistration}  block> Register</Button>
          </div>
        </form>
      </div>
    );
  }
}