import React from 'react';
import ReactDOM from 'react-dom';
import OrderTable from './src/order_table';

ReactDOM.render(<OrderTable fields={['Item Name', 'Description', 'Quantity', 'Order Price', 'Unit', 'Subtotal']} />, document.getElementById('root'));