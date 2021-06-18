import React from 'react';
import * as d3 from 'd3';
import SearchBar from './components/search';



class Chart extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            stocks: []
        }
        this.handleSearch = this.handleSearch.bind(this);

    }
    
    handleSearch(fields) {
        var parseDate = d3.utcParse("%Y-%m-%d")
        fetch('http://localhost:8000/stocks/get-stocks/', {
            method: "POST",
            body: JSON.stringify({
                symbol: fields.currentSymbol,
                date: fields.date
            }),
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
        })
        .then(response => response.json())

        .then(data => {
            this.setState({
                stocks: data.map(d => {d.date = parseDate(d.date);d.open=d.open_price;return d;})
            });
            this.drawChart(this.state.stocks)
        })
    }

    
    formatChange (y0, y1) {
        const f = d3.format("+.2%");
        return f((y1 - y0) / y0);
    }
    
    componentDidMount() {
        var parseDate = d3.utcParse("%Y-%m-%d")
        
        fetch('http://localhost:8000/stock/', {})
            .then((response) => {
                return response.json()
            })
            .then((stockData) => {
                this.setState({
                    stocks: stockData.slice(-100).map(d => {d.date = parseDate(d.date);d.open=d.open_price;return d;})
                });
              this.drawChart(this.state.stocks);
            })
    }

    drawChart(data) {
        document.querySelector('.chart-area').innerHTML = '';
        const height = 500;
        const width = 1000;
        const margin = { top: 20, right: 30, bottom: 30, left: 40 };
        
        const svg = d3.select('.chart-area').append('svg').attr('width', width).attr('height', height)
        
        var x = d3.scaleBand()
            .domain(d3.utcDay
                .range(data[0].date, +data[data.length - 1].date + 1)
                .filter(d => d.getUTCDay() !== 0 && d.getUTCDay() !== 6))
            .range([margin.left, width - margin.right])
            .padding(0.2)
    
        // -----------------------------------
        var y = d3.scaleLog()
            .domain([d3.min(data, d => d.low), d3.max(data, d => d.high)])
            .rangeRound([height - margin.bottom, margin.top])
    
        // --------------------------------------
        var xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x)
                .tickValues(d3.utcMonday
                    .every(width > 720 ? 1 : 2)
                    .range(data[0].date, data[data.length - 1].date))
                .tickFormat(d3.utcFormat("%-m/%-d")))
            .call(g => g.select(".domain").remove())
    
        // -----------------------------------------
        var yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y)
                .tickFormat(d3.format("$~f"))
                .tickValues(d3.scaleLinear().domain(y.domain()).ticks()))
            .call(g => g.selectAll(".tick line").clone()
                .attr("stroke-opacity", 0.2)
                .attr("x2", width - margin.left - margin.right))
            .call(g => g.select(".domain").remove())
    
        // -------------------------------------
        var formatDate = d3.utcFormat("%B %-d, %Y");
    
        var formatValue = d3.format(".2f");
    
    
        svg.append("g")
            .call(xAxis);
    
        svg.append("g")
            .call(yAxis);
    
        const g = svg.append("g")
            .attr("stroke-linecap", "round")
            .attr("stroke", "black")
            .selectAll("g")
            .data(data)
            .join("g")
            .attr("transform", d => {return `translate(${x(d.date)},0)`});
    
    
        g.append("line")
            .attr("y1", d => y(d.low))
            .attr("y2", d => y(d.high));
    
        g.append("line")
            .attr("y1", d => y(d.open))
            .attr("y2", d => y(d.close))
            .attr("stroke-width", x.bandwidth())
            .attr("stroke", d => d.open > d.close ? d3.schemeSet1[0]
                : d.close > d.open ? d3.schemeSet1[2]
                    : d3.schemeSet1[8]);
    
        g.append("title")
            .text(d => `${formatDate(d.date)}
            Open: ${d.open}
            Close: ${formatValue(d.close)} (${this.formatChange(d.open, d.close)})
            Low: ${formatValue(d.low)}
            High: ${formatValue(d.high)}`);
    
        }

    render() {

        return (
            <div>
                <SearchBar onSearch={this.handleSearch}></SearchBar>
            </div>
        );
    }
}

export default Chart;