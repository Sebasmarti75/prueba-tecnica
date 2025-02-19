import './App.css';
import { CreateButton } from './CreateButton';
import { useEffect, useState } from "react";
import axios from "axios";
import { RegistrarseButton } from './RegistrarseButton';
import {Registrarse} from './Registrarse'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { LoginButton } from './loginButton';
import { Publicaciones } from './publicaciones';


function Home() {
  // const [data, setData] = useState(null);

  // useEffect(() => {
  //   axios.get("http://localhost:8000/data")
  //     .then(response => setData(response.data))
  //     .catch(error => console.error("Error fetching data:", error));
  // }, []);

  return (
    
    <>
      <div className='login'>
        <div className='form-container'>
          <form className='form'>
              <label htmlFor="email" className='label'>Email</label>
              <input type="text" id="email" placeholder="correo@example.com" className="input input-email"></input>

              <label htmlFor="password" className='label'>Password</label>
              <input type="password" id="password" placeholder="********" className="input input-password"></input>


              <LoginButton />
          </form>

          <RegistrarseButton />
        </div>
      </div>
    </>
  );
}
function App() {
  return (
    <Router>
      <Routes>
        
        <Route path="/" element={<Home />} />

        <Route path="/Registrarse" element={<Registrarse />} />

        <Route path="/Publicaciones" element={<Publicaciones />} />
      </Routes>
    </Router>
  );
}

export default App;


