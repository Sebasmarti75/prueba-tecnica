import './App.css'
import { useNavigate } from "react-router-dom";

function CreateButton() {

  const navigate = useNavigate()

    return (
      <button className='secondary-button signup-button' 
      onClick={
        () => navigate("/")   
      }
      >Crear Cuenta</button>
    );
  }
export { CreateButton};