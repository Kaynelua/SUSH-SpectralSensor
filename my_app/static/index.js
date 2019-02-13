
var {Component} = React;


var messageCount =0;


function Heading(props) {
  const modeName = props.modeName;
  const checked = (props.modeName == "Bill") ? "checked" : "";

  return (

   <h4 class="d-flex justify-content-between align-items-center">
        <span class="text-muted mb-1">{modeName}</span>
        <div class="custom-switch custom-switch-sm custom-switch-label-io">
          <input class="custom-switch-input" id="example_1" type="checkbox" onClick={props.onClick} defaultChecked={checked}/>

          <label class="custom-switch-btn" htmlFor="example_1"></label>
        </div>  
  </h4>
  );
}

function combinePriceColour(props){
  return(
      props.items.map( (item,index) =>
        ({color:props.colors[index].text,price:item.text})
        )
  );
}



class ModeControl extends React.Component {
  constructor(props) {
    super(props);
    this.handleLoginClick = this.handleLoginClick.bind(this);
    this.handleLogoutClick = this.handleLogoutClick.bind(this);
    this.updatemsgReceived = this.updatemsgReceived.bind(this);
    this.handlePriceTextChange = this.handlePriceTextChange.bind(this);  
    this.state = {inUserMode: false ,
                  items :[], 
                  inputCost1: '',
                  inputCost2: '',
                  totalNumPlates : 3,
                  msgReceived : 0,
                  colors:[{key:'Blue',price:""},{key:'Red',price:""},{key:'White',price:""},{key:'Orange',price:""},{key:'Pink',price:""}],
                  orderTally: []};
  }

  updatemsgReceived(message){
    if(this.state.inUserMode){
      let plateColor = message.payloadString;
      let mapIdx =  this.state.orderTally.findIndex(x => x.key==plateColor)
      if(mapIdx == -1){
        this.setState(state => ({ orderTally : state.orderTally.concat( ({key:plateColor,count:1}) )}));
      }
      else{
        let orderTally  = this.state.orderTally
        let plateRecord = orderTally[mapIdx]
        plateRecord.count = plateRecord.count + 1
        orderTally[mapIdx] = plateRecord
        this.setState(state=>({ orderTally : orderTally }));
      }
      console.log("Message : " + plateColor);
      console.log(this.state.orderTally);
    }
  }

  handleLoginClick(e) {
    this.setState({inUserMode: true});
  }

  handleLogoutClick(e) {
    this.setState({inUserMode: false});
  }


  handlePriceTextChange(newColorObj){
    let colors = this.state.colors
    let idx = this.state.colors.findIndex(x => x.key==newColorObj.key)
    colors[idx] = newColorObj
    this.setState({
      colors: colors
    });
  }

  render() {
    const inUserMode = this.state.inUserMode;
    const msgReceived = this.state.msgReceived;
    let modeButton;  
    let adminInput;
    let heading;
    let orderTotal;
    const rows = [];
    const orderLine = [];
    let logo = "/static/logonew.png"

    let uMode = [];
    let aMode = [];

    if(inUserMode){  
      heading       = <Heading onClick={this.handleLogoutClick} key="toggle" modeName='Bill' />;
      this.state.orderTally.forEach( (orderTally) => {
          let colorObj   = this.state.colors.find(x=>x.key==orderTally.key)
          orderLine.push(
            <OrderLine
              key      = {orderTally.key}
              order    = {orderTally}
              colorObj = {colorObj  }
            />
      )});
      orderTotal = <OrderTotal
                      key     = "orderTotal"
                      orders  = {this.state.orderTally}
                      colors  = {this.state.colors    }
                   />
      uMode.push(heading)
      uMode.push(orderLine)
      uMode.push(orderTotal)
    } 
    else{
      heading    = <Heading onClick={this.handleLoginClick} key="toggle" modeName='Price Settings' />;
      this.state.colors.forEach( (colorObj) => {
          rows.push(
            <ColorRow
              key      ={colorObj.key}
              colorObj ={colorObj    }
              onPriceTextChange={this.handlePriceTextChange}
            />
      )});
      aMode.push(heading)
      aMode.push(rows)
    }

    return (
      <div class="row align-items-center">
        <div class="col-md-4 order-md-2 mb-4"/> 
        <div class="col-md-4 order-md-2 mb-4"> 
            <div class="text-center">
                <img src={logo} height="120" />
            </div>
            <hr/>
              <ul class="list-group mb-3">
                {aMode}
                {uMode}
              </ul>
        </div>
        <div class="col-md-4 order-md-2 mb-4"/> 
       </div>
    );
  }
}

class ColorRow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: this.props.colorObj.price};
    this.handlePriceTextChange = this.handlePriceTextChange.bind(this);
  }
  handlePriceTextChange(event) {
    let newPrice = event.target.value
    this.setState({value: newPrice});
    this.props.colorObj.price = newPrice
    this.props.onPriceTextChange(this.props.colorObj);
  }
  render() {
    const name = this.props.colorObj.key;
    const id   = name + "_form" ;
    let padding = 6-name.length;
    let padded_name = name.padEnd(padding); 
    return (
      <li class="list-group-item d-flex justify-content-between lh-condensed">
        <div class="col">
          <label class="mt-2" htmlFor={id}>
            <h6 class="my-0"> {padded_name} </h6> 
          </label> 
        </div>
        <div class="col-sm-7">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text">£</span>
            </div> 
            <input id={id}  class="form-control" placeholder="0.00" value={this.state.value} onChange={this.handlePriceTextChange} />
          </div>         
        </div>
      </li>
    );
  }
}

class OrderLine extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const name  = this.props.order.key;
    const id    = "orderline_"+name;
    const count = this.props.order.count 
    console.log( parseFloat(count))
    console.log(parseFloat(this.props.colorObj.price))
    const totalAmount = parseFloat(count) * parseFloat(this.props.colorObj.price)
    return (
        <li class="list-group-item d-flex justify-content-between lh-condensed">
          <div>
            <h6 class="my-0">{name}</h6>
            <small class="text-muted">{count}</small>
          </div>
          <span class="text-muted">£ {totalAmount}</span>
        </li>
    );
  }
}

class OrderTotal extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let colors = this.props.colors
    let orders = this.props.orders
    let orderLineTotal = orders.map(orderLine=>{
      let colorObj = colors.find(x=>x.key==orderLine.key);
      return parseFloat(orderLine.count) * parseFloat(colorObj.price)
    })

    let subTotal=0;
    if(orders.length){ subTotal = orderLineTotal.reduce((a,b)=>a+b); }
    let serviceCharge = 0.125*subTotal;
    let total = subTotal + serviceCharge;
    let subTotal2dp      = subTotal.toFixed(2);
    let serviceCharge2dp = serviceCharge.toFixed(2);
    let total2dp         = total.toFixed(2);

    return (
    <div class="list-group-item">
        <div class="d-flex justify-content-between lh-condensed">
          <div> <h6 class="my-0">Subtotal : </h6> </div>
          <span>£{subTotal2dp}</span>
        </div>
        
        <div class="d-flex justify-content-between lh-condensed">
          <div> <h6 class="my-0">Service Charge : </h6> </div>
          <span>£{serviceCharge2dp}</span>
        </div>

        <div class="d-flex justify-content-between lh-condensed">
          <div> <h6 class="my-0">Total : </h6> </div>
          <span>£{total2dp}</span>
        </div>
    </div>      
    );
  }
}


/*

*/

var element = <ModeControl />
const webPage = ReactDOM.render(element,
	document.getElementById('root')
);

var host = "test.mosquitto.org";
var topic = "IC.Embedded/IOS/#"
var port = 8081

// Client Instance
var client = new Paho.MQTT.Client(host,port,"Main")
client.onMessageArrived = webPage.updatemsgReceived;//onMessageArrived;//window.element.updatemsgReceived;
client.onConnectionLost = onConnectionLost;

// Callback handler
client.connect({onSuccess:onConnect,
        useSSL   :true
         })

function onConnect() {
  console.log("Connection Succesful");
  client.subscribe(topic)
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}