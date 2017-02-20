(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var DynamicSearch = React.createClass({displayName: "DynamicSearch",

    getInitialState: function() {
        return {searchString: ''};
    },

    handleChange: function(event) {
        this.setState({searchString: event.target.value});
        console.log("scope updated!");
    },

    render: function() {

        var countries = this.props.items;
        var searchString = this.state.searchString.trim().toLowerCase();

        if (searchString.length >0 ) {
            countries = countries.filter(function(country) {
                return country.name.toLowerCase().match(searchString);
            });
        }

        return (
        React.createElement("div", null, 
            React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placehodler: "Search!"}), 
            React.createElement("ul", null, 
                countries.map(function(country) {
                    return React.createElement("li", null, country.name)
                })
            )
        )
        )
    }
});

var countries = [
  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
];

ReactDOM.render(
    React.createElement(DynamicSearch, {items: countries}),
    document.getElementById('main')
);

},{}]},{},[1]);
