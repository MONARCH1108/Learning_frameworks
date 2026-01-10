import propTypes from 'prop-types'

function GreetingAdvanced(props){

    const welcomeMessage = <h2 className="welcome-message">Welcome {props.username}</h2>

    const loginPrompt = <h2 className="loginPrompt">please log in to continue {props.username}</h2>



    return(
        props.isLoggedIn ?  welcomeMessage:loginPrompt
    )
}

GreetingAdvanced.propTypes={
    isLoggedIn: propTypes.bool,
    username: propTypes.string,
}
GreetingAdvanced.defaultProps={
    isLoggedIn: false,
    username: "Guest"
}


export default GreetingAdvanced