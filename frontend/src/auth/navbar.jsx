import React from "react";
import {Navbar,Nav,Button} from "react-bootstrap";
import {isLoggedIn, deleteTokens} from './auth.js';

const Log = () => {
    if (isLoggedIn()) {
        return (<Button onClick={() => {deleteTokens();window.location.replace("/")}}>Sign out</Button>)
    } else {
        return (<Nav.Link href="/login">Login</Nav.Link>)
    }
}

const NavBar = () =>{
        return(
            <Navbar className="nav-container" bg="primary" variant="dark">
              <Nav className="pull-right">
                <Log />
              </Nav>
            </Navbar>
        )
}

export default NavBar