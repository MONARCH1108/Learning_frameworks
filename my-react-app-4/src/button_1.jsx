function ButtonNew(){

    let count = 0
    const handleClick=(name)=>{
        if(count<3){
            count++,
            console.log(`${name} you activated event ${count} time/s`)
        }
        else{
            console.log(`${name} stop clicking me!`)
        }
    };

    return(
        <div>
            <button onClick={()=>handleClick("abhay")}>Click me</button>
        </div>
    )
}
export default ButtonNew