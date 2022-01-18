import React, { Component } from 'react';
// import { langItems } from './langItems';
import './fuelTable.css'
import { fuelItems } from './fuelItems';

class fuelTable extends Component {
    state = {clicked: false}

    render() {
        return(
            <div className="fuel-table-container">
                <h1 className="fuelHeading">Gas prices</h1>
                <p className="last-update-text">Updated: 12:00</p>
                    <table className="table table-striped">
                            <tr>
                                <th scope="col"><a >Name</a></th>
                                <th scope="col"><a >95</a></th>
                                <th scope="col"><a >Diesel</a></th>
                                <th scope="col"><a >Expected price</a></th>
                            </tr>
                    {fuelItems.map((item, index) => {
                        return (
                            <tr>
                                <td className="rowItems"><img src={item.logo} alt={item.logo_alt}/><p className="leftAlign">{item.name}</p></td>
                                <td className="rowItems"><p>{item.price95}</p></td>
                                <td className="rowItems"><p>{item.priceD}</p></td>
                                <td className="rowItems"><p>placeholder</p></td>
                            </tr>   
                        ) 
                    })}
                    </table>
            </div>
        )
    }
}

export default fuelTable
