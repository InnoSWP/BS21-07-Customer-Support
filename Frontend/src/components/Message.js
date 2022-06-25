import React from 'react'
import './Message.css'
function Message(props) {
  return (
    
    <div>
        {props.msg.map((elem)=>{
            return (<div className='msgOut'>
                {elem}
            </div>);
        })}
    </div>
  )
}

export default Message;