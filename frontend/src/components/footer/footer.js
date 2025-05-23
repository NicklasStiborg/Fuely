import React, { Component } from 'react'
import { langItems } from './langItems'
import './footer.css'


class Footer extends Component {
    render() {
        return (
            <footer className="fixed-bottom">
                <p>Created by Nicklas Stiborg⭐</p>
                <div className="lang-container">
                    <ul>
                    {langItems.map((item, index) => {
                        return (
                            <li><a href={item.url} className={item.cName}>
                            {item.flag}
                            </a></li>
                        )
                    })}
                    </ul>
                </div>
            </footer>
        )



    }



}

export default Footer