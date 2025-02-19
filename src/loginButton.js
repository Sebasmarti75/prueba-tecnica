import './App.css'
import { useNavigate } from "react-router-dom";


function LoginButton() {

    const navigate = useNavigate();

    return (
      <button className='primary-button login-button' 
      onClick={
        () => navigate("/publicaciones")   
      }
      >Login</button>
    );
  }
export { LoginButton};