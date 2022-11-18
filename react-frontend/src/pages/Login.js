import React, { useEffect, useState, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// Json encoding
import jwt_decode from "jwt-decode";

import "../styles/app.css";
import { setCookie } from "../utils/cookies";

export default function Login() {
  // State for users callback response values from google oAuth 2.0
  const [user, setUser] = useState({});

  //Decodes the response from google oAuth 2.0 and decodes it.
  function handleCallbackResponse(response, error) {
    var useObject = jwt_decode(response.credential);
    setUser(useObject);
    setCookie("jwt_cookie", response.credential, 1);

    console.log("Error: ");
    console.log(error);
    console.log("Encoded JWT ID token: ");
    console.log(response);
    console.log("Decoded JWT credentials: ");
    console.log(useObject);
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
    // eslint-disable-next-line
  }, [divRef.current]);

  function LoggedIn() {
    // check whitelist (api towards flask, user.email)
    // send JWT token || access token.
    // rederict to homepage
    window.location.replace("http://localhost:3000/test");
  }

  return (
    <div className="App">
      <div id="signInDiv" class="font-monospace">
        <center>
          <div ref={divRef} />
        </center>
      </div>

      {user.email_verified && LoggedIn()}
    </div>
  );
}
