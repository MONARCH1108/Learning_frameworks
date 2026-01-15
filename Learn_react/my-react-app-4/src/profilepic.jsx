function ProfilePic(){

    const imageURL = './src/assets/react.svg'
    const handleClick4=(e)=>{
        e.target.style.display = "none"
    }
    return(
        <div>
            <img onClick={(e) => handleClick4(e)}  src={imageURL} alt="" />
        </div>
    )

}
export default ProfilePic