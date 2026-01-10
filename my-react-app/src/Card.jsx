import profilePic from './assets/1.png'

function Card(){
    return(
        <div className="card">
            <img src={profilePic} className='card-img'  alt="Profile-picture" />
            <h2 className='card-header'>Monarch Codes</h2>
            <p>This is a react tutorial</p>
            <p>Practise session</p>
        </div>
    );
}
export default Card