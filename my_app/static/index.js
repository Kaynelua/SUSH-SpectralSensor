
var {Component} = React;


var messageCount =0;


function Greeting(props) {
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
    this.handleLoginClick = this.handleLoginClick.bind(this);
    this.handleLogoutClick = this.handleLogoutClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange2 = this.handleChange2.bind(this);
    this.handleSubmit2 = this.handleSubmit2.bind(this);
    this.updatemsgReceived = this.updatemsgReceived.bind(this);
    this.state = {inUserMode: false , items :[], inputCost1: '',inputCost2: '', totalNumPlates : 3 ,msgReceived : 0, colors:[]};
  }

  //Called via callback from messageArrived
  updatemsgReceived(message){
    if(this.state.inUserMode){

    }
    else{
      messageCount = messageCount +1;
      console.log("Message : "+message.payloadString + "    message count:" +messageCount);
      console.log(typeof message.payloadString)
      const newColor ={
        id : messageCount,
        text :message.payloadString
      };
      this.setState(state=> ({
        colors : state.colors.concat(newColor)
      }));
      this.setState({msgReceived : messageCount});
    }
  }

  handleLoginClick() {
  	//Switch to user Mode
    this.setState({inUserMode: true});
  }

  handleLogoutClick() {
  	//Switch to Admin Mode
    this.setState({inUserMode: false});
  }

  handleChange(e) {
    this.setState({ inputCost1: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!this.state.inputCost1.length) {
      return;
    }
    const newItem = {
      text: this.state.inputCost1,
      id: Date.now()
    };
    this.setState(state => ({
      items: state.items.concat(newItem),
      inputCost1 :''
    }));
  }

  handleChange2(e) {
    this.setState({ inputCost2: e.target.value });
  }

  handleSubmit2(e) {
    e.preventDefault();
    if (!this.state.inputCost2.length) {
      return;
    }
    const newItem = {
      text: this.state.inputCost2,
      id: Date.now()
    };
    this.setState(state => ({
      items: state.items.concat(newItem),
      inputCost2 :''
    }));
  }

  render() {
    const inUserMode = this.state.inUserMode;
    const msgReceived = this.state.msgReceived;
    let button;
    let plate_setup_1= ""
    let detected_1= ""
    let plate_setup_2= ""
    let detected_2= ""
    let plate_setup_3= ""
    let detected_3= ""
    let collate;

    if (inUserMode) {
      //IN USER MODE:
      var plate_count =0;

      //this.state.items.length = 0	//Clear our list when in user mode

      button = <GoToAdminButton onClick={this.handleLogoutClick} />;


    } else {
      //IN ADMIN MODE DO CALIBRATION
      	plate_setup_1= "Plate 1: " 
      	if(msgReceived >= 1) {
    		detected_1 = 
    		<form onSubmit={this.handleSubmit}>
			<label htmlFor="p1">
            	Detected! Price : $
          	</label> 
    		<input
            id="p1"
            onChange={this.handleChange}
            value={this.state.inputCost1}
            />
           	</form>
    	} 
    	plate_setup_2= "Plate 2: "
      	if(msgReceived >= 2) {
    		detected_2= 
    		<form onSubmit={this.handleSubmit2}>
			<label htmlFor="p2">
            	Detected! Price : $
          	</label> 
    		<input
            id="p2"
            onChange={this.handleChange2}
            value={this.state.inputCost2}
            />
           	</form>
    	}

    	plate_setup_3 = "Plate 3: "
      	if(msgReceived >= 3) {
    		detected_3= "Detected" 
    	}


    	button = <GoToUserButton onClick={this.handleLoginClick} />;
    	collate = <PriceList items={this.state.items} colors ={this.state.colors}/>

    }

    return (
      <div>
        <Greeting inUserMode={inUserMode} />
        {plate_setup_1}
        {detected_1} <br /> <br />
        {plate_setup_2}
        {detected_2} <br /> <br />
        {plate_setup_3}
        {detected_3} <br /> <br />
        {collate}
        {button}
      </div>
    );
  }
}

var element = <ModeControl />


const webPage = ReactDOM.render(element,
	document.getElementById('root')
);

var host = "test.mosquitto.org";
var port = 8081
var topic = "IC.Embedded/IOS/#"

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
  //let message = new Paho.MQTT.Message("Hello");
  //message.destinationName = topic;
  //client.send(message);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}





// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
//serviceWorker.register();
