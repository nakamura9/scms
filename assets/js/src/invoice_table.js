import React, {Component} from 'react';
import $ from 'jquery';

class InvoiceTable extends Component{
    constructor(props){
        super(props);
        /*
        No props
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
            var url = window.location.href;
            console.log(url);
            var url_elements = url.split("/")
            var pk = url_elements[url_elements.length-1];

            $.ajax({
                url: "/invoicing/api/invoice/" + pk +"/",
                method: "GET",
                data: {}
            }).then(res => {
                console.log(res);
                var items = res.items;
                var i=0;
                for(i in items){
                    console.log(items[i]);
                    $.ajax({
                        url: "/invoicing/api/item/" + (items[i]-1),
                        method:"GET"
                    }).then(item =>{
                        this.state.items.concat({
                            code: 1,
                            description: 1,
                            price: 1,
                            quantity: item.quantity
                        })
                    })
                }
            });
            }
        }
    
    removeItem(index){
        //removes an item from the state and the table
        var newState = this.state;
        newState.items.splice(index, 1)
        this.setState(newState);
        this.props.removeHandler(index);
    }

    addItem(data){
        //adds items to the state 
        this.setState({items: this.state.items.concat(data)});
        this.state.items.length
        this.props.addHandler(data, this.state.items.length);
    }

    render(){
        const headStyle = {
            borderLeft: "1px solid white",
        };
     
        return(
            <div>
                <h3>Invoice Item Table</h3>
                <table className="table table-striped">
                    <thead style={{backgroundColor: "blue",
                                    color: "white"}}>
                        <tr>
                            <td style={{maxWidth: "30px"}}></td>
                            <td style={headStyle}>Item Code</td>
                            <td style={headStyle}>Item Description</td>
                            <td style={headStyle}>Quantity</td>
                            <td style={headStyle}>Unit Price</td>
                            <td style={headStyle}>Subtotal</td>
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
                                <td>{item.code}</td>
                                <td>{item.description}</td>
                                <td>{item.quantity}</td>
                                <td>{item.price}</td>
                                <td>{item.price * item.quantity}</td>
                            </tr>
                        ))}
                    <EntryRow url="/invoicing/api/item" addItem={this.addItem.bind(this)} />    
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
                <td colSpan="2">
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

export default InvoiceTable;