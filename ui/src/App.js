import React from 'react';
import logo from './logo.svg';
import Timeslot from './Components/ChannelTimeslot.js'
import 'react-calendar-timeline/lib/Timeline.css'
import './App.css';
import moment from 'moment'
import Timeline from 'react-calendar-timeline'


function App() {
  const groups = [{ id: 1, title: 'group 1' }, { id: 2, title: 'group 2' }]

  const items = [
    {
      id: 1,
      group: 1,
      title: 'item 1',
      start_time: moment(),
      end_time: moment().add(1, 'hour')
    },
    {
      id: 2,
      group: 2,
      title: 'item 2',
      start_time: moment().add(-0.5, 'hour'),
      end_time: moment().add(0.5, 'hour')
    },
    {
      id: 3,
      group: 1,
      title: 'item 3',
      start_time: moment().add(2, 'hour'),
      end_time: moment().add(3, 'hour')
    }
  ]


  return (
    //Setup the App viewport
    <div
      style={{
        position: "absolute",
        width: "100%",
        height: "100%"
      }}
    >
      //Header for channel description and preview
      <div style={{
        backgroundColor: "blue",
        height: "30%",
        width: "100%"
      }}>
        
      </div>

      //Channel guide
      <div style={{
        backgroundColor: "red",
        height: "70%",
        width: "100%"
      }}>

        <div>
    Rendered by react!
    <Timeline
      groups={groups}
      items={items}
      defaultTimeStart={moment().add(-12, 'hour')}
      defaultTimeEnd={moment().add(12, 'hour')}
    />
  </div>,



      </div>
    </div>

    //<Timeslot></Timeslot>


    //<div className="App">
    //  <header className="App-header">
    //    <img src={logo} className="App-logo" alt="logo" />
    //    <p>
    //      Edit OWO <code>src/App.js</code> and save to reload.
    //    </p>
    //    <a
    //      className="App-link"
    //      href="https://reactjs.org"
    //      target="_blank"
    //      rel="noopener noreferrer"
    //    >
    //      Learn React
    //    </a>
    //  </header>
    //</div>
  );
}

export default App;
