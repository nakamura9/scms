import React, {Component} from 'react';
import {Heading, TableContent, OrderTableEntry} from './base_table';

class OrderTable extends Component{
    constructor(props){
        super(props);
        this.state = {
            contents: [],
            total: 0
        }
        console.log(props.cummulativeField);
    }

    
    insertHandler(vals){
        var newContents = this.state.contents;
        newContents.push(vals);
        var total = newContents.reduce((a, b) =>{
            return a + parseInt(b[this.props.cummulativeField]);
        }, 0);
        this.setState({
            contents: newContents,
            total: total
            });
    }

    removeHandler(id){
        var newContents = this.state.contents;
        newContents.splice(id, 1);
        var total = newContents.reduce((a, b) =>{
            //cheating
            return(a + (b.unit_price * b.quantity));
        }, 0);
        this.setState({
            contents: newContents,
            total: total
            });
    }

    render(){
        var field_names = ['item_name', 'description', 'quantity', 'order_price', 'unit'];
        return(
            <table>
                <Heading fields={this.props.fields}/>
                <TableContent contents={this.state.contents}
                              fields={field_names}
                              removeHandler={this.removeHandler.bind(this)}/>
                <OrderTableEntry total={this.state.total} fields={field_names}  
                                insertHandler={this.insertHandler.bind(this)} />
            </table>
        )
    }
}

export default OrderTable;