import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import OrderTable from './src/order_table';
import SearchWidget from './src/search_widget';
import $ from 'jquery';


ReactDOM.render(<OrderTable  fields={['Item Name', 'Description', 'Quantity', 'Order Price', 'Unit', 'Subtotal']} />, document.getElementById('root'));
    