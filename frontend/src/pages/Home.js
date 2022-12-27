import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import UserNavBar from "../components/Navbar";
import { getCookie, setCookie } from "../utils/cookies";
// Json encoding
import jwt_decode from "jwt-decode";
import Whitelist from "../components/Whitelist";

function handleSignOut() {
  setCookie("jwt_cookie", {}, 1);
  window.location.replace("http://localhost:3000");
}

export default function Home() {
  const [visible, setVisible] = useState(false);

  function toggleVisibility() {
    setVisible((prevVisible) => !prevVisible);
  }

  var obj = getCookie("jwt_cookie");
  var useObject;
  try {
    useObject = jwt_decode(obj);
  } catch (error) {
    useObject = false;
    console.log(error);
  }
  console.log(useObject);

  console.log(visible);

  return (
    <>
      {!useObject && handleSignOut()}
      {useObject.email_verified && (
        <div className="">
          <UserNavBar
            handleSingOut={handleSignOut}
            objectValList={[
              useObject.picture,
              useObject.given_name,
              useObject.family_name,
            ]}
            onToggle={toggleVisibility}
          />
          {visible && (
            <aside>
              <Whitelist />
            </aside>
          )}
          <div class="col-lg-7">
            <h3 class="mt-5">Multiple Live Streaming</h3>
            <img
              src="{{ url_for('video_feed', id='0') }}"
              width="100%"
              alt=" camera 1"
            />
            <img
              src="{{ url_for('video_feed', id='1') }}"
              width="100%"
              alt=" camera 2"
            />
          </div>
          <img src="{{ url_for('video_feed', id='1') }}" width="100%" alt="" />
        </div>
      )}
    </>
  );
}
