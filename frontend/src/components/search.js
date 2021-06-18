import React, { Component } from 'react';


class SearchBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            symbols: [],
            fields: {
                date: '', 
                currentSymbol: ''
            }
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        fetch('http://localhost:8000/stocks/symbols/', {})
        .then(response=> response.json())
        .then(data=>{
            this.setState({
                symbols: data.symbols
            })
        })
    }

    handleClick() {
        this.props.onSearch(this.state.fields)
    }

    handleChange(event) {
        let fields = this.state.fields;
        fields[event.target.name] = event.target.value;
        this.setState({ fields })
    }

    render() {
        return (
            <div>
                <input type="date" placeholder="Enter date" name='date' value={this.state.fields.date} onChange={this.handleChange}/>
                <select name="currentSymbol" value={this.state.fields.currentSymbol} onChange={this.handleChange}>
                    {this.state.symbols.map(symbol=> (
                        <option value={symbol} >{symbol}</option>
                    ))}
                </select>
                <button onClick={this.handleClick}>Submit</button>
            </div>
        )
    }
}

export default SearchBar;