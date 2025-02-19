import './App.css'
import { useNavigate } from "react-router-dom";


function RegistrarseButton() {

    const navigate = useNavigate();

    return (
      <button className='secondary-button signup-button' 
      onClick={
        () => navigate("/Registrarse")   
      }
      >Registrarse</button>
    );
  }
export { RegistrarseButton};