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
    // used to remove hidden inputs from the form
    console.log(id);
    $("#item_" + id).remove();
}

function populatedRemoveHandler(code){
    // used in update views to remove existing items
    console.log("code: " + code);
    $("<input>")
            .attr({
                "type": "hidden",
                "name": "removed_items[]",
                "id": "removed_item_" + code,
                "value": code
                }).appendTo("form");
}

function searchHandler(data){
    var decomposed = data.split('-');
    $("#id_customer").val(decomposed[0]);
}

function populatedHandler(widget){
    console.log(window.location.href);
            var urlElements = window.location.href.split("/");
            var invNo = urlElements[urlElements.length- 1]; 
            $.ajax({
                url: "/invoicing/api/invoice/" + invNo + "/",
                data: {},
                method: "GET"
            }).then(res => {
                console.log(res.customer);
                $.ajax({
                    url: '/invoicing/api/customer/' + res.customer + "/",
                    data: {},
                    method: "GET"
                }).then(res => {
                    console.log(res);
                    widget.setState({
                        selected: true,
                        inputVal: res.id + " - " +
                                  res.first_name + 
                                  " " + res.last_name
                    })
                });
            });
}

if(populated){
    ReactDOM.render(<InvoiceTable populated={true} populatedRemoveHandler={populatedRemoveHandler} addHandler={
        addHandler} removeHandler={removeHandler} />, 
        document.getElementById('populated-item-table'));
    
    ReactDOM.render(<SearchWidget populated={true} populatedHandler={populatedHandler} url="/invoicing/api/customer/" handler={
        searchHandler} />, document.getElementById('customer-search'));
}else{
    ReactDOM.render(<InvoiceTable populated={false} addHandler={addHandler} removeHandler={
        removeHandler} />, document.getElementById('item-table'));
    
    ReactDOM.render(<SearchWidget  url="/invoicing/api/customer/" handler={
        searchHandler} />, document.getElementById('customer-search'));
}
