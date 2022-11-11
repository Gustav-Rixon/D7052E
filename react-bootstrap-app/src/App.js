import React, { useEffect, useState, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// Json encoding
import jwt_decode from "jwt-decode";

//Local
import data from "./utils/whitelist.json";
import "./App.css";
import UserNavBar from "./components/userNavbar";
import WhiteListContent from "./components/whiteListContent";

function App() {
  const [user, setUser] = useState({});

  function handleCallbackResponse(response, error) {
    var useObject = jwt_decode(response.credential);

    if (data.Whitelist.find((e) => e.email === useObject.email)) {
      document.getElementById("signInDiv").hidden = true;

      for (var i = 0; i < data.Whitelist.length; i++) {
        if (
          data.Whitelist[i].email === useObject.email &&
          data.Whitelist[i].admin === true
        ) {
          Object.assign(useObject, { admin: data.Whitelist[i].admin });
        }
      }

      setUser(useObject);
    } else alert("Not a Whitelisted user!");

    console.log("Error: " + error);
    console.log("Encoded JWT ID token: " + response);
    console.log("Credentials: " + response.credential);
    console.log(useObject);
  }

  const handleSingOut = () => {
    setUser({});
    google.accounts.id.prompt(); //ful lösning, tittas på när jag ork. så man får prompt efter man logat ut
    document.getElementById("signInDiv").hidden = false;
  };

  const divRef = useRef(null);

  useEffect(() => {
    /* global google */
    if (user.name === undefined) {
      google.accounts.id.prompt();
    }

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
  }, [divRef.current]);

  return (
    <div className="App">
      <div id="signInDiv" class="font-monospace">
        <center>
          <span style={{ marginRight: ".5rem" }}>Login: </span>
          <div ref={divRef} />
        </center>
      </div>

      {user.email_verified && (
        <div id="content">
          <UserNavBar
            handleSingOut={handleSingOut}
            picture={user.picture}
            given_name={user.given_name}
            family_name={user.family_name}
          />
          {user.admin && <WhiteListContent></WhiteListContent>}
        </div>
      )}
    </div>
  );
}

export default App;

/**
  {Object.keys(user).length != 0 && (
          <button onClick={(event) => handleSingout(event)}>
            {" "}
            Sign Out
          </button>
        )}
                    <UserNavBar
              picture={user.picture}
              given_name={user.given_name}
              family_name={user.family_name}
              handleSignout={handleSingOut}
            />

          {isAdmin && (
            <AdminNavBar
              handleSingOut={handleSingOut}
              picture={user.picture}
              given_name={user.given_name}
              family_name={user.family_name}
            />
          )}
          {!isAdmin && (
            <UserNavBar
              handleSingOut={handleSingOut}
              picture={user.picture}
              given_name={user.given_name}
              family_name={user.family_name}
            />
          )}
 */
