import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import InvoiceTable from './src/invoice_table';
import SearchWidget from './src/search_widget';
import $ from 'jquery';

var populated = document.getElementById('populated-item-table');


function addHandler(item, count){
    $("<input>")
            .attr({
                "type": "hidden",
                "name": "items[]",
                "id": "item_" + item.code,
                "value": item.code + "-" + item.quantity
                }).appendTo("form");
}

function removeHandler(id){
    $("#item_" + toString(id)).remove();
}

function searchHandler(data){
    var decomposed = data.split('-');
    $("#id_customer").val(decomposed[0]);
}



if(populated){
    ReactDOM.render(<InvoiceTable populated={true} addHandler={
        addHandler} removeHandler={removeHandler} />, 
        document.getElementById('populated-item-table'));
    
    ReactDOM.render(<SearchWidget url="/invoicing/api/customer/" handler={
        searchHandler} />, document.getElementById('customer-search'));
}else{
    ReactDOM.render(<InvoiceTable populated={false} addHandler={addHandler} removeHandler={
        removeHandler} />, document.getElementById('item-table'));
    
    ReactDOM.render(<SearchWidget  url="/invoicing/api/customer/" handler={
        searchHandler} />, document.getElementById('customer-search'));
}
