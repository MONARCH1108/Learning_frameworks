function Button(){

    //const handleClick = () => console.log("Event Activated");
    const handleClick1 = (name) => console.log(`${name} event is activated again`)

    return(
        <div>
            <button onClick={() => handleClick1("abhay")}>Click Here</button>
        </div>
    );
}
export default Button