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
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/data")
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/autenticar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email, 
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error en la autenticación");
      }

      console.log("Token recibido:", data.access_token);
      localStorage.setItem("token", data.access_token); 
      alert("¡Login exitoso!");
    } catch (error) {
      setError(error.message);
    }
  };


  return (
    
    <>
      <div className='login'>
        <div className='form-container'onSubmit={handleLogin}>
          <form className='form'>
              <label htmlFor="email" className='label'>Email</label>
              <input type="text" id="email" placeholder="correo@example.com" className="input input-email" value={email}
            onChange={(e) => setEmail(e.target.value)}></input>

              <label htmlFor="password" className='label'>Password</label>
              <input type="password" id="password" placeholder="********" className="input input-password"  value={password}
            onChange={(e) => setPassword(e.target.value)}></input>


              <LoginButton />
              {error && <p className="error">{error}</p>}
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


