import React, { Component } from 'react';
import { menuItems } from './menuItems';
import './navbar.css'

class Navbar extends Component {
    state = {clicked: false}


    
    render() {
        return(
            <div className="header-container">
                <h1 className="navbarLogo">Fuely<i className="fab fa-react"></i></h1>
            <nav className="navbarItems">
                <ul>
                    {menuItems.map((item, index) => {
                        return (
                        <li key={index}>
                            <a className={item.cName} href={item.url}>
                            {item.title}
                            </a>
                        </li>
                        )
                    })}
                </ul>
            </nav>
            </div>
        )
    }
}

export default Navbar