import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { getCookie } from "../utils/cookies";
import jwt_decode from "jwt-decode";

// Load cookie value.
const obj = getCookie("jwt_cookie");
let useObject;
try {
  useObject = jwt_decode(obj);
} catch (error) {
  useObject = false;
  console.error(error);
}

const addUserToWhitelist = async (newUser) => {
  const response = await fetch("/whitelist/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify([newUser, { email: useObject.email }]),
  });

  //const result = response.json(); // await kekw
  console.log("***************************************************");
  console.log(response);
  console.log(response.ok);
  //console.log(result);
  console.log("***************************************************");

  if (response.ok) {
    window.alert("User added to whitelist successfully");
    return response;
  } else {
    window.alert("Error adding user to whitelist ");
    throw new Error(response);
  }
};

const AddUserForm = () => {
  const [emailAdd, setEmail] = useState("");
  const [admin, setAdmin] = useState(false);
  const [owner, setOwner] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Create the new user object with the form data
      const newUser = {
        email: emailAdd,
        admin: admin,
        owner: owner,
      };
      // Call the addUserToWhitelist function with the new user object
      const result = await addUserToWhitelist(newUser);
      console.log(result);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="addUser">
        <h3> Add User</h3>
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={emailAdd}
            required
            onChange={(event) => setEmail(event.target.value)}
          />
          <br />
          <label htmlFor="admin">Admin:</label>
          <input
            type="checkbox"
            id="admin"
            checked={admin}
            onChange={(event) => setAdmin(event.target.checked)}
          />
          <br />
          <label htmlFor="owner">Owner:</label>
          <input
            type="checkbox"
            id="owner"
            alt=""
            checked={owner}
            onChange={(event) => setOwner(event.target.checked)}
          />
          <br />
          <button type="submit">Add User</button>
        </form>
      </div>
    </>
  );
};

export default AddUserForm;
