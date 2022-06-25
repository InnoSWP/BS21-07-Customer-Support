import React, { useState, useEffect } from 'react'
import './Chat.css'
import Message from './Message';

const server_url = 'http://localhost:3001/';
const axios = require('axios').default;

function Chat(props) {
  const [chatId, setChatId] = useState (0);
  const [msg, setMsg] = useState ("");
  const [messages, setMessages] = useState([]);
  useEffect(() => {
      getID();
  }, []);


  function pressEnt(e){
      e.preventDefault();
  }

  function clickHedler(){
    axios.get(server_url, {params: {message: msg}});
    setMessages((prevMsg) => {

      return [...prevMsg, msg];

    });
    setMsg("");
  }

  function getID(){  
    axios.get(server_url + 'getChatId')
    .then((res) => {
      setChatId(res.data.chatId);
      console.log(res, 'res');
    })
  }

  return (props.trigger) ? (
    <div className='chat'>
        <div className='chat-inner'>
            <div className='header' >
               User id: {chatId}
            </div>

            <div className='msgPoll'>
              <Message msg={messages}/>
            </div>

            <div className='typePoll'>
              <form onSubmit={pressEnt} className='sendBox'>
                <input type={"text"} className='areaType' value={msg} onChange={e=>setMsg(e.target.value)}></input>
                <button onClick={clickHedler} id='send' className='sendBtn'></button>
              </form>
            </div>

            {props.children}
        </div>
    </div>
  ) : "";
}

export default Chat