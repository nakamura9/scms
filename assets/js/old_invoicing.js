import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import InvoiceTable from './src/invoice_table';
import SearchWidget from './src/search_widget';

class InvoiceApp extends Component{
    constructor(props){
        super(props);
        this.state = {
            customer: "",
            date: "",
            terms: "",
            comments: "",
            paid_in_full: "",
            items: [],
            account: "",
            retrievedAccounts: [],
            "csrfmiddlewaretoken": $("#page-token").val()
        }
    }
    handleCustomer(data){
        var decomposed = data.split('-')
        this.setState({customer: parseInt(decomposed[0])});
    }

    handleDate(data){
        this.setState({date: data});
    }

    handleAccount(data){
        this.setState({account: data});
    }

    handleItems(data){
        this.setState({items: data})
    }

    handleComments(data){
        this.setState({comments: data});
    }

    handleTerms(data){
        this.setState({terms: data});
    }


    submitForm(){
        
        $.ajax({
            url: this.props.url,
            method: "POST",
            data: { customer: this.state.customer,
                        date: $("#id-datepicker").val(),
                        terms: this.state.terms,
                        comments: this.state.comments,
                        paid_in_full: this.state.paid_in_full,
                        items: this.state.items,
                        account: this.state.account,
                        "csrfmiddlewaretoken": this.state.csrfmiddlewaretoken
        },
        }).then(res => {
            window.location.href=this.props.redirect_url;
        }, error => {console.log(error)});
        
        console.log(this.state);
    }
    componentDidMount(){
        $.ajax({
            url: this.props.accounts_url,
            method: "GET",
            data: {}
        }).then(res => {
            this.setState({retrievedAccounts: res});
        });
    }

    render(){
        return(
            <div>
            <div className="col-sm-4 well">
                <table className="table">
                    <tbody>
                        <tr>
                            <td><label>Customer: </label></td>
                            <td><SearchWidget handler={this.handleCustomer.bind(this)} url="/invoicing/api/customer/" /></td>
                        </tr>
                        <tr>
                            <td><label>Date: </label></td>
                            <td><input onChange={event => this.handleDate(event.target.value)} id="id-datepicker" className="form-control" type="text" /></td>
                        </tr>
                        <tr>
                            <td><label>Account: </label></td>
                            <td><select onChange={event => this.handleAccount(event.target.value)} className="form-control" >
                                <option value="null" >--------</option>
                                {this.state.retrievedAccounts.map((acc, index) =>(<option key={index} value={acc.id}>{acc.name}</option>
                                ))}
                            </select></td>
                        </tr>
                        <tr>
                            <td><label>Comments: </label></td>
                            <td><textarea className="form-control" onChange={event => this.handleComments(event.target.value)} ></textarea></td>
                        </tr>
                        <tr>
                            <td><label>Terms: </label></td>
                            <td><textarea className="form-control" onChange={event => this.handleTerms(event.target.value)}></textarea></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div className="col-sm-8">
                <InvoiceTable handler={this.handleItems.bind(this)} />
                <button onClick={this.submitForm.bind(this)} className="btn btn-primary pull-right">Create Invoice</button>
            </div>
        </div>
        );
    }
}

ReactDOM.render(<InvoiceApp accounts_url="/invoicing/api/account/" url="/invoicing/api/invoice/" redirect_url="/invoicing/" />, document.getElementById('root'));