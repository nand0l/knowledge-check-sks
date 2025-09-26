import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { v4 as uuidv4 } from 'uuid';

const LoginComponent = () => {
  const [username, setUsername] = useState('');
  const [userID, setUserID] = useState('');

  // On component mount, check if the username and userID cookies are present
  useEffect(() => {
    const storedUsername = Cookies.get('username');
    const storedUserID = Cookies.get('userID');

    if (storedUsername) {
      setUsername(storedUsername); // Prefill the username input if the cookie is present
    }

    if (storedUserID) {
      setUserID(storedUserID); // Set the userID if the cookie is present
    } else {
      // Generate a new userID and store it in a cookie if not already present
      const newUserID = uuidv4(); // Generate a unique ID
      setUserID(newUserID);
      Cookies.set('userID', newUserID, { expires: 7 }); // Save the new userID in a cookie
      console.log('New userID generated and stored:', newUserID);
    }
  }, []);

  const handleInputChange = (event) => {
    setUsername(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (username) {
      // Set the cookie with the username, expires in 7 days
      Cookies.set('username', username, { expires: 7 });
      console.log('Username stored in cookie:', username);
      console.log('UserID:', userID); // Use the generated userID
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input
          type="text"
          value={username}
          onChange={handleInputChange}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default LoginComponent;
