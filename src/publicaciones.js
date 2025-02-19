import './App.css'
import { useState, useEffect } from "react";
import axios from "axios";

function Publicaciones(){
    
    const [posts, setPosts] = useState([]);
    const [content, setContent] = useState("");
    const [token, setToken] = useState(localStorage.getItem("token") || "");
  
    useEffect(() => {
      if (token) {
        axios.get("http://localhost:8000/posts/", { params: { token } })
          .then(res => setPosts(res.data))
          .catch(err => console.error(err));
      }
    }, [token]);
  
    const handlePost = () => {
      axios.post("http://localhost:8000/posts/", { content, token })
        .then(res => {
          setPosts([...posts, { id: Date.now(), content }]);
          setContent("");
        })
        .catch(err => console.error(err));
    };
  
    const handleDelete = (id) => {
      axios.delete(`http://localhost:8000/posts/${id}`, { params: { token } })
        .then(() => setPosts(posts.filter(p => p.id !== id)))
        .catch(err => console.error(err));
    };
    return (
      <>
       <div className="publicaciones-container">
      <h1>Mis Publicaciones</h1>
      <textarea type="text" value={content} onChange={(e) => setContent(e.target.value)} placeholder="Publica algo..." />
      <button className="secondary-buttonP login-button" onClick={handlePost}>Publicar</button>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            {post.content} <button className="primary-buttonP login-button" onClick={() => handleDelete(post.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
      </>
    );
};
export {Publicaciones};