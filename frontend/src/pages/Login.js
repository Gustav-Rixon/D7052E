import React, { useEffect, useState, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// Json encoding
import jwt_decode from "jwt-decode";

import "../styles/app.css";
import { setCookie } from "../utils/cookies";

export default function Login() {
  // State to track whether the Google OAuth 2 key is missing or invalid
  const [keyError, setKeyError] = useState(false);

  // State for users callback response values from google oAuth 2.0
  const [user, setUser] = useState({});
  const [jwt, setWEBJWT] = useState("");

  //Decodes the response from google oAuth 2.0.
  function handleCallbackResponse(response, error) {
    var jwt_decode_object = jwt_decode(response.credential);
    setUser(jwt_decode_object); // Decoded JWT webtoken, contains google user info
    setWEBJWT(response.credential); //JWT webtoken
    setCookie("jwt_cookie", response.credential, 1);

    console.log("Error: ");
    console.log(error);
    console.log("Encoded JWT ID token: ");
    console.log(response);
    console.log("Decoded JWT credentials: ");
    console.log(jwt_decode_object);
  }

  // Google login auth
  const divRef = useRef(null);
  useEffect(() => {
    /* global google */
    google.accounts.id.prompt();

    if (divRef.current) {
      window.google.accounts.id.initialize({
        client_id: process.env.REACT_APP_CLIENT_ID,
        callback: handleCallbackResponse,
      });
      window.google.accounts.id.renderButton(divRef.current, {
        theme: "outline",
        size: "large",
      });
    }

    if (user && jwt) {
      LoggedIn();
    }
    // eslint-disable-next-line
  }, [divRef.current]);

  async function LoggedIn() {
    async function setJWT() {
      try {
        const response = await fetch("/set_jwt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            jwt: jwt,
            email: user.email,
          }),
        });
        const data = await response.json();
        console.log(data);
      } catch (err) {
        console.log(err);
      }
    }

    await setJWT();
    window.location.replace("http://localhost:3000/home");
  }

  return (
    <div className="App">
      {keyError && (
        <div className="error-banner">
          Missing or Invalid Google OAuth 2 Key
        </div>
      )}
      <div id="signInDiv" class="font-monospace">
        <center>
          <h3 style={{ marginBottom: 90 }}>D7052E Camera Security AB</h3>
          <div ref={divRef} />
        </center>
      </div>
      {!process.env.REACT_APP_CLIENT_ID && setKeyError(true)}
    </div>
  );
}
