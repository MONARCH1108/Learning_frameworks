import React, {useState}  from "react";

function MyComponent(){
    const [name, setName] = useState("");
    const [quantity, setQuantity] = useState();
    const [comment, setComment] = useState("");
    const [payment, setPayment] = useState("Credit");
    const [shipping, setShipping] = useState("")

    function handleNameChange(event){
        setName(event.target.value)
    }
    function hanfleQuantityChange(event){
        setQuantity(event.target.value)
    }
    function handleCommentChange(event){
        setComment(event.target.value)
    }
    function handlePaymentChange(event){
        setPayment(event.target.value)
    }
    function hangleShippingChange(event){
        setShipping(event.target.value)
    }

    return(
        <div>
            <input type="text" value={name} onChange={handleNameChange} />
            <p>Name: {name}</p>

            <input type="number" value={quantity} onChange={hanfleQuantityChange} />
            <p>Quantity: {quantity}</p>

            <input type="text" value={comment} onChange={handleCommentChange} placeholder="Enter Comment" />
            <p>Comment: {comment}</p>

            <select name="" id="" value={payment} onChange={handlePaymentChange}>
                <option value="">Select an option</option>
                <option value="Visa">Visa</option>
                <option value="MasterCard">MaterCard</option>
                <option value="GiftCard">GiftCard</option>
            </select>
            <p>Payment: {payment}</p>

            <label htmlFor="">
                <input type="radio" value="pickUp" checked={shipping==="pickUp"} onChange={hangleShippingChange}/>
                PickUp 
            </label>

            <label htmlFor="">
                <input type="radio" value="Delivery" checked={shipping==="Delivery"} onChange={hangleShippingChange}/>
                Delivery
            </label>

            <p>Shipping: {shipping}</p>

        </div>
    )
}
export default MyComponent