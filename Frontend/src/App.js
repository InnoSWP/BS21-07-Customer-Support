import React, { useState } from 'react'
import './Styles/App.css'
import Chat from './components/Chat'

function App() {
  const [triggerState, settrtiggerState] = useState(false);
  function setTR(){
    settrtiggerState(!triggerState);
    console.log (triggerState);
  }
  return (  
    <div className="App">

        <h1>support chat</h1>
        <button onClick={setTR} id='innoOPlogo' className="open-button" ></button>
        <main>
          <Chat trigger={triggerState} setTrigger = {settrtiggerState}></Chat>
        </main> 

    </div>
  );
}

export default App;
