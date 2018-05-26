import React, {Component} from 'react';
import $ from 'jquery';

class Heading extends Component{
    //props of an array
    render(){
        var style = {
                backgroundColor: 'steelblue',
                color: 'white',
                padding: '10px',
                borderLeft: '1px solid white'
            };
        return(
            <thead style={style}>
                <tr>
                <td></td>
                    {this.props.fields.map((field, index) =>(
                        <td style={style} key={index} > {field} </td>
                    ))}
                </tr>
            </thead>
        );
    }
}

class TableContent extends Component{
    render(){
        return(
            <tbody>
                {this.props.contents.map((row, index) =>(
                    <tr key={index}>
                        <td>
                            
                            <button type="button" 
                                    className="btn btn-danger"
                                    onClick={() => (this.props.removeHandler(index))}
                                    >
                                    
                                <span className="glyphicon glyphicon-trash" ></span>
                                
                            </button>
                            
                        </td>
                        {this.props.fields.map((field, i) =>(
                            <td key={i}>{row[field]}</td>
                        ))}
                        <td>
                            {row.order_price * row.quantity}
                        </td>
                    </tr>
                ))}
            </tbody>
        ); 
    }
}

class OrderTableEntry extends Component{
    constructor(props){
        super(props);
        this.state = {
            inputs: {}
        }
    }
    insertHandler(){
        console.log('self handler');
        this.props.insertHandler(this.state.inputs);
    }
    inputHandler(event){
        var name= event.target.name;
        var value = event.target.value;
        var newVals = this.state.inputs;
        newVals[name] = value;
        this.setState({inputs: newVals});
    }

    render(){
        return(
            <tfoot>
                <tr>
                    <td></td>
                    {this.props.fields.map((field, index) => (
                        <td key={index}><input type="text"
                               name={field} 
                               className="form-control"
                               onChange={event => (this.inputHandler(event))} />
                        </td>
                    ))}
                    
                    <td>
                        <button type="button" 
                                className="btn btn-default"
                                onClick={this.insertHandler.bind(this)}>Insert</button>
                    </td>
                </tr>
                <tr>
                    <td colSpan='6'style={{textAlign: 'right'}}><b>Total:</b></td>
                    <td>{this.props.total}</td>
                </tr>
            </tfoot>
        );
    }
}


class BaseTable extends Component{
    constructor(props){
        super(props);
        /*
        title: 
        populated: bool
        pop_func : function
        fields: array of strings
        #handlers alter hidden inputs in the forms
        removeHandler: function
        removePopHandler: function
        addHandler: function

        State consists of the running total of the table and a list of items
        parent component for the rows and the item form 
        child of the overall form component */
        this.state = {
            total: 0,
            items: []
        };
    }

    componentDidMount(){
        if(this.props.populated){
            // run when populating the data for the first time 
            this.props.popFunc();
        }
    }
    
    removeItem(index){
        //removes an item from the state and the table
        var newState = this.state;
        
        if ($("#item_" + index)){
            this.props.removeHandler(index);
        }
        // dont use else statement!
        if(this.props.populated){
            var pk = this.state.items[index].pk;
            this.props.populatedRemoveHandler(pk);
        }
        newState.items.splice(index, 1);
        this.setState(newState);
    }

    addItem(data){
        //adds items to the state 
        this.setState({items: this.state.items.concat(data)});
        this.props.addHandler(data, this.state.items.length);
    }

    render(){
        const headStyle = {
            borderLeft: "1px solid white",
        };
     
        return(
            <div>
            <h3>{this.props.title}</h3>
                <table className="table table-striped">
                    <thead style={{backgroundColor: "blue",
                                    color: "white"}}>
                        <tr>
                            <td style={{minWidth: "50px"}}></td>
                            {this.props.fields.map((field, i) =>(
                                <td key={i} style={headStyle} >{field}</td>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.items.map((item, index) =>(
                            <tr key={index} >
                                <td style={{maxWidth: "30px"}}>
                                    <button onClick={
                                         () => (this.removeItem(index))
                                        } className="btn btn-danger">
                                            <span className="glyphicon glyphicon-trash" aria-hidden="true"></span>
                                    </button>
                                </td>
                                {this.props.fields.map((field, key)=>(
                                    <td key={key}>{item[field]}</td>
                                ))}                               
                            </tr>
                        ))}
                    <EntryRow url={this.props.populateOptionsUrl} 
                                addItem={this.addItem.bind(this)} />    
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colSpan={5}><b><u>Total:</u></b></td>
                            <td><b>{(this.state.items.length === 0) ? 0 :
                                         this.state.items.reduce(
                                             function(a,b){
                                                return a + b.subtotal
                                            }, 0
                                    )}
                            </b></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        );
    }
}

class EntryRow extends Component {
    constructor(props){
        super(props);
        this.state = {
            itemText: "",
            itemQuantity: 0,
            options: []
        };
    }
    
    componentDidMount(){
        $.ajax({
            url: this.props.url,
            data: {},
            method: "GET",
        }).then(res => {
        this.setState({options: res});
        });
    }

    addItem(){
        var decomposed = this.state.itemText.split("-");
        var data = {};
        data.code = decomposed[0];
        data.description = decomposed[1];
        data.price = parseFloat(decomposed[2]);
        data.quantity = this.state.itemQuantity;
        data.subtotal = data.price * data.quantity;
        this.props.addItem(data);
        $('#entry-row-item').val("");
        $('#entry-row-quantity').val("");
        
    }

    updateDescription(data){
        this.setState({itemText: data});
    }

    updateQuantity(data){
        this.setState({itemQuantity: data});
    }

    render(){
        return(
            <tr>
                <td colSpan="3">
                    <input placeholder="Select Item..." className="form-control" id="entry-row-item" type="text" list="item-datalist"  onChange={event => this.updateDescription(event.target.value)} />
                    <datalist id="item-datalist">
                    {this.state.options.map((item, index) =>( 
                        <option key={index} >{item.code} - {item.item_name} - {item.unit_price}</option>
                        ))}
                    </datalist>
                </td>
                <td>
                    <input className="form-control" id="entry-row-quantity" type="number" onChange={event => this.updateQuantity(event.target.value)} />
                </td>
                <td colSpan="2">
                    <center>
                        <button className="btn btn-primary" onClick={this.addItem.bind(this)}>
                            Add Item
                        </button>
                    </center>
                </td>
            </tr>
        );
    }
}

export {BaseTable, TableContent, OrderTableEntry, Heading};