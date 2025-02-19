import './App.css'
import { CreateButton } from './CreateButton';

function Registrarse() {
    return (
      <>
        <div>
            <div className='login'>
                <div className='form-container'>
                    <h1 className="title-cuenta">My account</h1>

                    <form  className="form">
                            <label htmlFor="name" className="label">Name</label>
                            <input type="text" id="name" placeholder="Pedro" className="input input-name"></input>

                            <label htmlFor="email" className="label">Email</label>
                            <input type="text" id="new-email" placeholder="correo@example.com" className="input input-email"></input>
                            
                            <label htmlFor="password" className="label">Password</label>
                            <input type="password" id="password" placeholder="********" className="input input-password"></input>

                            <CreateButton />
                    </form>
                </div>
            </div> 
        </div>
      </>
    );
  }
export { Registrarse};