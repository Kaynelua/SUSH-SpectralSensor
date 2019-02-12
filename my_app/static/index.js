
var {Component} = React;


var messageCount =0;


function Heading(props) {
  const inUserMode = props.inUserMode;
  if (inUserMode) {
    return <h1>User Mode</h1>;
  }
  return <h1>Admin Mode</h1>;
}

function GoToUserButton(props) {
  return (
    <button onClick={props.onClick}>
      Calibration Done
    </button>
  );
}

function GoToAdminButton(props) {
  return (
    <button onClick={props.onClick}>
      Back to Calbiration
    </button>
  );
}

function CollateOrderButton(props){
  return (
    <button onClick={props.onClick}>
      Collate Order
    </button>
  );
}


function combinePriceColour(props){
  return(
      props.items.map( (item,index) =>
        ({color:props.colors[index].text,price:item.text})
        )
  );
}

class PriceList extends React.Component {
  render() {
   const combined = combinePriceColour(this.props)
    return (
      <div>
        <ul>
              {combined.map(pair  =>
                <li key={pair.color}>
                <span> {pair.color} </span> 
                <span> {pair.price} </span> 
                </li>
                )} 
        </ul>
      </div>
    );
  }
}

class ModeControl extends React.Component {
  constructor(props) {
    super(props);
    this.handleCollateClick = this.handleCollateClick.bind(this);
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
                  colors:[{key:'blue',price:""},{key:'red',price:""},{key:'white',price:""},{key:'orange',price:""},{key:'pink',price:""}],
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

  handleCollateClick(e){
    let totalCost = this.state.orderTally.reduce( (a,b)=> a.count + b.count );
    console.log(totalCost);
  }

  handlePriceTextChange(newColorObj){
    let colors = this.state.colors
    let idx = this.state.colors.findIndex(x => x.key==newColorObj.key)
    colors[idx] = newColorObj
    this.setState({
      colors: colors
    });
    console.log(this.state.colors);
  }

  render() {
    const inUserMode = this.state.inUserMode;
    const msgReceived = this.state.msgReceived;
    let modeButton;
    let collateButton;
    let collateList;
    let adminInput;
    const rows = [];
    const orderLine = [];
    if(inUserMode){  
      modeButton    = <GoToAdminButton onClick={this.handleLogoutClick} />;
      collateButton = <CollateOrderButton onClick={this.handleCollateClick} />;
      this.state.orderTally.forEach( (orderTally) => {
          let colorObj   = this.state.colors.find(x=>x.key==orderTally.key)
          orderLine.push(
            <OrderLine
              key      = {orderTally.key}
              order    = {orderTally}
              colorObj = {colorObj  }
            />
      )});

    } 
    else{
    	modeButton = <GoToUserButton onClick={this.handleLoginClick} />;
    	collateList = <PriceList items={this.state.items} colors ={this.state.colors}/>
      this.state.colors.forEach( (colorObj) => {
          rows.push(
            <ColorRow
              key      ={colorObj.key}
              colorObj ={colorObj    }
              onPriceTextChange={this.handlePriceTextChange}
            />
      )});
    }
    return (
      <div>
        <Heading inUserMode={inUserMode} />
        {orderLine}
        {rows}
        {collateList}
        {modeButton}
        {collateButton}
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
    return (
      <div>
        <form>
          <label htmlFor={id}> {name}  £ </label> 
          <input id={id} value={this.state.value} onChange={this.handlePriceTextChange} /> 
        </form>
      </div>
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
      <div>
        <span> {name} x</span>
        <span> {count}</span>
        <span> {totalAmount}</span>
      </div>
    );
  }
}


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