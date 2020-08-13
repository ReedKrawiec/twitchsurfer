
class If extends{
  render(){
    let {condition} = this.props;
    if(condition)
      return this.props.children;
    return <div></div>;
  }
}