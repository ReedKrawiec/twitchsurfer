import React from 'react';
import Carousel from "react-spring-3d-carousel"
import uuidv4 from "uuid";

class Timeslot extends React.Component {
   state = {
    goToSlide: 0,
    offsetRadius: 2,
    showNavigation: true,
  };

    slides = [
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/800/?random" alt="1" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/800/?random" alt="2" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/600/800/?random" alt="3" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/500/?random" alt="4" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/800/?random" alt="5" />
    },
    {
      key:uuidv4(), 
      content: <img src="https://picsum.photos/500/800/?random" alt="6" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/600/?random" alt="7" />
    },
    {
      key: uuidv4(),
      content: <img src="https://picsum.photos/800/800/?random" alt="8" />
    }
  ].map((slide, index) => {
    return { ...slide, onClick: () => this.setState({ goToSlide: index }) };
  });


  render() {
    
    return (
      <div style={{
        // Background styling
        backgroundColor: "red", 
        position: "absolute", 
        width: "100%",
        height: "100%",


        //Outline styling 
        outlineWidth: "10px",
        outlineStyle: "solid",
        outlineColor: "blue",
        outlineOffset: "-10px"
        }}>
            <Carousel
                slides={this.slides}
                goToSlide={this.state.goToSlide}
                offsetRadius={this.state.offsetRadius}
            />
        </div>
    );
  }
}

export default Timeslot;