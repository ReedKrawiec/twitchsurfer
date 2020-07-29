import React, { useState, useContext, useEffect } from 'react';
import logo from './logo.svg';
import Timeslot from './Components/ChannelTimeslot.js'
import 'react-calendar-timeline/lib/Timeline.css'
import './css/reset.css';
import './css/App.css';
import moment from 'moment'
import Timeline from 'react-calendar-timeline'
import ReactTwitchEmbedVideo from "react-twitch-embed-video"


let HOUR_PX = window.innerWidth/24;
if(HOUR_PX < 70){
  HOUR_PX = 70;
}

const StreamerContext = React.createContext({})
const TimeContext = React.createContext({});
const UserContext = React.createContext({});


let TimelineHeaderLabel = (props)=>{
  const context = useContext(TimeContext);
    let handleClick = () => {
      context.setTime(props.time.subtract(2,"hours"));
    }
    let style = {width:HOUR_PX};
    if(props.index === 2){
      style["backgroundColor"] = "purple";
    }
    if(props.time.hours() === 0 && props.time.minutes() === 0){
      return(
        <div className="timeline-header-label timeline-header-label-day" style={style} onClick={()=>{handleClick()}}>
          <p className="timeline-header-day">{props.time.format("M/D")}</p>
          <p>{props.time.format("h:mm a")}</p>
        </div>
      )
    } else {
      return(<div className="timeline-header-label" style={style} onClick={()=>{handleClick()}}>
        <p>{props.time.format("h:mm")}</p>
        <p>{props.time.format("a")}</p>
       </div>
      )
    }
}

function TimelineHeader(props){
  let time_clone = moment(props.start);
  //Need to offset the time, because we add 30 minutes everytime 
  //We add a new time label
  time_clone.subtract(1,"hour");
  let hours_arr = [];
  for(let a = 0,b = 0;a < window.innerWidth; a += HOUR_PX, b++){
    hours_arr.push(
      <TimelineHeaderLabel time={moment(time_clone.add(1,"hour"))} index={b} key={b}/>
    )
  }
  
  return(
    <div className="timeline-header-holder">
      {hours_arr}
    </div>

  )
}

function TimelineStreamLineRender(props){
  const context = useContext(UserContext);

  let start = moment(props.start);  
  let streams_arr = [];
  for(let stream of props.streams){
    let start_x = moment.duration(stream.start_time.diff(start)).asMinutes()/60 * HOUR_PX;
    let duration = moment.duration(stream.end_time.diff(stream.start_time)).asMinutes()/60 * HOUR_PX;
    streams_arr.push(
      <div className="time-stream-container" style={{left:start_x}}>
      <img className="time-stream-picture" src={stream.profile_picture} />
      <svg style={{fill:props.color}} className="timeline-stream" height="50" width={duration+25} onClick={()=>{context.setUser({name:stream.name,description:stream.description})}}>
        <g>
          <circle cx="15" cy="25" r="15"></circle>
          <rect x="15" y="17.5" width={duration} height="15" />
          <text x="50%" y="20%" dominant-baseline="middle" text-anchor="middle">{stream.name}</text> 
          <circle cx={duration+10} cy="25" r="15"></circle>
        </g>
      </svg>
      </div>);
  }
  return (
    <div className="timeline-render-line">
      {
        streams_arr
      }
    </div>
    );
}

function TimelineStreamRender(props) {
  let groups = [];
  for (let a = 0; a < props.grouped_streams.length;a++){
    groups.push(<TimelineStreamLineRender start={props.start} color={props.color} streams={props.grouped_streams[a]}/>)
  }
  return(<div>
    {groups}
  </div>)
}

function groupStreams(streams){
  console.log(JSON.parse(JSON.stringify(streams)));
  let groups = [];
  let streams_sorted = 0;
  let selected_group = 0;
  
  while(streams.length > 0){
    let stream_to_be_sorted = streams[0];
    streams.splice(0,1);
    let stream_sorted = false;
    for(let a = 0; a < groups.length && !stream_sorted;a++){
      for(let b = 0;b < groups[a].length;b++){
        let saved = groups[a][b];
        if(b === groups[a].length - 1){
          if(stream_to_be_sorted.start_time.isAfter(moment(saved.end_time).add(1,"hour"))){
            stream_sorted = true;
            groups[a].push(stream_to_be_sorted);
            break;
          }
        }
        else{
          if(stream_to_be_sorted.start_time.isAfter(moment(saved.end_time).add(1,"hour") && stream_to_be_sorted.end_time.isBefore(moment(groups[a][b+1].start_time)))){
            stream_sorted = true;
            groups[a].push(stream_to_be_sorted);
            break;
          }
        }
      }
    }
    if(!stream_sorted){
      groups.push([])
      groups[groups.length - 1].push(stream_to_be_sorted);
    }
  }
  console.log(groups);
  return groups;
}

function TimelineCategory(props){
  
    if(props.streams.length > 0){
    let grouped = groupStreams(props.streams)
    return(
      <div className="category-container">
        <div style={{color:props.color}} className="timeline-category">
          <div className="timeline-category-container">
            <p className="timeline-category-name">{props.name}</p>
            <div style={{backgroundColor:props.color}} className="timeline-category-bar"></div>
          </div>
          
        </div>
        <div className="category-holder"></div>
        <TimelineStreamRender grouped_streams={grouped} start={props.start} color={props.color} />
      </div>
    )
  }
  return <div></div>;
}

function StreamerInfo(props){
  const context = useContext(UserContext);

  let component = <a className="site_login" href={props.auth_string}>Login With Twitch</a>;
  if(props.username){
    component = <p className="site_login">{props.username} <a className="site_logout" href="./">LOGOUT</a></p>
  }
  return(
    <div className="header-bar">
        <div className="header-container">
          <div className="info-box">
              <p className="site_logo">TWITCH SURFER</p>
              {component}           
            <div className="streamer-info">
              <p className="streamer-name">{context.user.name}</p>
              <div className="streamer-desc">
              <p>{context.user.description}</p>
              </div>
            </div>

          </div>
          <ReactTwitchEmbedVideo targetClass="streamer-embed" channel={context.user.name} width="500px" height="100%" layout="video" />
        </div>
      </div>
  )
}

let TimeLineBody = (props) => {
  
  const [time, setTime] = useState(moment().subtract(1,"hour").subtract(moment().minutes(),'minutes'));
  const streamers = useContext(StreamerContext);
  let start = time;
  let streams = [];
  if (streamers.valid) {
    let start_of_week = moment(start).startOf("week");
    let range_start = moment(start).diff(start_of_week, "minutes") / 30;
    let range_end = range_start + (window.innerWidth / HOUR_PX) * 2;
    let range_end_moment = moment(start).add((window.innerWidth / HOUR_PX) * 60, "minutes");
    let looking_for_end = false;
    streamers.data.forEach((x) => {
      let current_start = undefined;
      for (let a = 0; a < x.schedule.length; a++) {
        if (looking_for_end) {
          streams.push({
            name: x.streamer,
            profile_picture: "https://static-cdn.jtvnw.net/jtv_user_pictures/xqcow-profile_image-9298dca608632101-300x300.jpeg",
            description: "Overwatch Professional tank player and full time streamer. EZ Clap",
            start_time: current_start,
            end_time: moment(start_of_week).add(x.schedule[a] * 30, "minutes")
          })
          streams.push({
            name: x.streamer,
            profile_picture: "https://static-cdn.jtvnw.net/jtv_user_pictures/xqcow-profile_image-9298dca608632101-300x300.jpeg",
            description: "Overwatch Professional tank player and full time streamer. EZ Clap",
            start_time: moment(current_start).add(1, "week"),
            end_time: moment(start_of_week).add(x.schedule[a] * 30, "minutes").add(1,"week")
          })
          looking_for_end = false;
        }
        else {
          current_start = moment(start_of_week).add(x.schedule[a] * 30, "minutes");
          looking_for_end = true;
        }
      }
      if(looking_for_end){
        streams.push({
          name: x.streamer,
          profile_picture: "https://static-cdn.jtvnw.net/jtv_user_pictures/xqcow-profile_image-9298dca608632101-300x300.jpeg",
          description: "Overwatch Professional tank player and full time streamer. EZ Clap",
          start_time: moment(start_of_week).add(x.schedule[x.schedule.length - 1] * 30, "minutes"),
          end_time: moment(start_of_week).add(336 * 30, "minutes")
        })
        streams.push({
          name: x.streamer,
          profile_picture: "https://static-cdn.jtvnw.net/jtv_user_pictures/xqcow-profile_image-9298dca608632101-300x300.jpeg",
          description: "Overwatch Professional tank player and full time streamer. EZ Clap",
          start_time: moment(start_of_week).add(x.schedule[x.schedule.length - 1] * 30, "minutes").add(1,"week"),
          end_time: moment(start_of_week).add(336 * 30, "minutes").add(1,"week")
        })
      }
      looking_for_end = false;
    })
    console.log(streams);
    streams = streams.filter((x) => (x.start_time.isAfter(start) && x.start_time.isBefore(range_end_moment)) || (x.end_time.isAfter(start) && x.end_time.isBefore(range_end_moment)));
  }
  return (
    <TimeContext.Provider value={{ time: time, setTime: setTime }}>
      <div className="timeline">
        <div className="timeline-time-labels">
          <TimelineHeader start={start} />
        </div>
        <div className="timeline-body">
          <TimelineCategory start={start} streams={streams} name="FOLLOWING" color="#88fffb" />
        </div>
      </div>
    </TimeContext.Provider>
  )
} 

function twitch_get(endpoint,access_token,client_id){
  let headers = {
    "Authorization": `Bearer ${access_token}`,
  };
  if(client_id){
    headers["Client-ID"] = client_id;
  }
  return fetch(endpoint,{ headers:headers });
}

function App() {
  const [user, setUser] = useState({ name: "Asmongold", description: "Sup yall it's me it's ya boy Asmongold" });
  const [streamer_data,setStreamerData] = useState({ valid : false, data: undefined});
  const [current_user,setCurrentUser] = useState(undefined);
  let client_id = "sh58je5z5mtatvjc7jfc1m6bgfvt94";
  let redirect_url = "http://localhost:3000";
  let response_type = "token+id_token";
  let scopes = "openid+user:edit:follows+user:read:email";
  let claims = JSON.stringify({
    userinfo: {
      email: null,
      email_verified: null,
      picture: null,
      preferred_username: null
    }
  });
  let auth_string = `https://id.twitch.tv/oauth2/authorize?client_id=${client_id}&redirect_uri=${redirect_url}&response_type=${response_type}&scope=${scopes}&claims=${claims}`;
  useEffect(() => {
    if (window.location.hash && !streamer_data.valid) {
      let query_string = window.location.hash.slice(1);
      let raw_auth_data = query_string.split("&").map((x) => x.split("="));
      console.log(raw_auth_data);
      let auth_data = {
        access_token: raw_auth_data[0][1],
        id_token: raw_auth_data[1][1],
        scope: raw_auth_data[2][1],
        token_type: raw_auth_data[3][1]
      }
      let d = async () => {
        let x = await twitch_get("https://id.twitch.tv/oauth2/userinfo", auth_data.access_token);
        x = await x.json();
        setCurrentUser(x.preferred_username);
        let y = await fetch(`http://127.0.0.1:5000/get_schedule?access=${auth_data.access_token}&id=${x.sub}`);
        y = await y.json();
        setStreamerData({valid:true,data: y});
      }
      d();
    }
  },[]);

  return (
    //Setup the App viewport
    <StreamerContext.Provider value={streamer_data}>
      <UserContext.Provider value={{ user: user, setUser: setUser }}>
        <div className="App">

          <StreamerInfo auth_string={auth_string} username={current_user}/>
          <TimeLineBody />
        </div>
      </UserContext.Provider>
    </StreamerContext.Provider>
  )
}

export default App;
