import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { getCookie } from "../utils/utils";
import jwt_decode from "jwt-decode";

// Load cookie value.
const obj = getCookie("jwt_cookie");
let jwt_decode_object;
try {
  jwt_decode_object = jwt_decode(obj);
} catch (error) {
  jwt_decode_object = false;
  console.log(error);
}

// API code post to add user to whitelist
const addUserToWhitelist = async (add) => {
  const response = await fetch("/whitelist/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(add),
  });

  if (response.ok) {
    window.alert("User added to whitelist successfully");
    return response;
  } else {
    window.alert("Error adding user to whitelist ");
    throw new Error(response);
  }
};

// API code post to remove user from whitelist
const removeUserFromWhitelist = async (remove) => {
  const response = await fetch("/whitelist/remove", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(remove),
  });

  if (response.ok) {
    window.alert("User removed from whitelist successfully");
    return response;
  } else {
    window.alert("Error removing user from whitelist ");
    throw new Error(response);
  }
};

const promoteUser = async (promote) => {
  const response = await fetch("/whitelist/promote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(promote),
  });
  if (response.ok) {
    window.alert("User has been promoted sucessfully");
    return response;
  } else {
    window.alert("Error promoting user ");
    throw new Error(response);
  }
};

const demoteUser = async (demote) => {
  const response = await fetch("/whitelist/demote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(demote),
  });
  if (response.ok) {
    window.alert("User has been demoted sucessfully");
    return response;
  } else {
    window.alert("Error demoting user ");
    throw new Error(response);
  }
};

export const AddUserForm = () => {
  const [email, setEmail] = useState("");
  const [admin, setAdmin] = useState(false);
  const [owner, setOwner] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (window.confirm("Are you sure you want to add this user?")) {
      try {
        // Create the new user object with the form data
        const newUser = {
          current_user_email: jwt_decode_object.email,
          target_user_email: email,
          owner_web: owner,
          admin_web: admin,
          jwt_web: obj,
        };
        // Call the addUserToWhitelist function with the new user object
        const result = await addUserToWhitelist(newUser);
        console.log(result);
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <>
      <div className="apicontent">
        <h3 className="apicontenth3">Add User</h3>
        <div className="user">
          <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                required
                onChange={(event) => setEmail(event.target.value)}
                className="form-control"
              />
            </div>
            <div className="form-group">
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="admin"
                  checked={admin}
                  onChange={(event) => setAdmin(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="admin" className="form-check-label">
                  Admin
                </label>
              </div>
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="owner"
                  alt=""
                  checked={owner}
                  onChange={(event) => setOwner(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="owner" className="form-check-label">
                  Owner
                </label>
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Add User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export const RemoveUserForm = () => {
  const [email, setEmail] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (window.confirm("Are you sure you want to remove this user?")) {
      try {
        // Create the user object with the form data
        const user = {
          current_user_email: jwt_decode_object.email,
          target_user_email: email,
          jwt_web: obj,
        };
        // Call the removeUserFromWhitelist function with the user object
        const result = await removeUserFromWhitelist(user);
        console.log(result);
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <>
      <div className="apicontent mt-4">
        <h3 className="apicontenth3">Remove User</h3>
        <div className="user">
          <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                required
                onChange={(event) => setEmail(event.target.value)}
                className="form-control"
              />
            </div>

            <button type="submit" className="btn btn-primary mt-4">
              Remove User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export const PromoteUserForm = () => {
  const [email, setEmail] = useState("");
  const [admin, setAdmin] = useState(false);
  const [owner, setOwner] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (window.confirm("Are you sure you want to promote this user?")) {
      try {
        // Create the user object with the form data
        const userToPromote = {
          current_user_email: jwt_decode_object.email,
          target_user_email: email,
          owner_web: owner,
          admin_web: admin,
          jwt_web: obj,
        };
        // Call the promoteUser function with the user object
        const result = await promoteUser(userToPromote);
        console.log(result);
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <>
      <div className="apicontent">
        <h3 className="apicontenth3">Promote User</h3>
        <div className="user">
          <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                required
                onChange={(event) => setEmail(event.target.value)}
                className="form-control"
              />
            </div>
            <div className="form-group">
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="admin"
                  checked={admin}
                  onChange={(event) => setAdmin(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="admin" className="form-check-label">
                  Admin
                </label>
              </div>
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="owner"
                  alt=""
                  checked={owner}
                  onChange={(event) => setOwner(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="owner" className="form-check-label">
                  Owner
                </label>
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Promote User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export const DemoteUserForm = () => {
  const [email, setEmail] = useState("");
  const [admin, setAdmin] = useState(false);
  const [owner, setOwner] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (window.confirm("Are you sure you want to demote this user?")) {
      try {
        // Create the user object with the form data
        const userToDemote = {
          current_user_email: jwt_decode_object.email,
          target_user_email: email,
          owner_web: owner,
          admin_web: admin,
          jwt_web: obj,
        };
        // Call the demoteUser function with the user object
        const result = await demoteUser(userToDemote);
        console.log(result);
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <>
      <div className="apicontent">
        <h3 className="apicontenth3 mt-4">Demote User</h3>
        <div className="user">
          <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                required
                onChange={(event) => setEmail(event.target.value)}
                className="form-control"
              />
            </div>
            <div className="form-group">
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="admin"
                  checked={admin}
                  onChange={(event) => setAdmin(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="admin" className="form-check-label">
                  Admin
                </label>
              </div>
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="owner"
                  alt=""
                  checked={owner}
                  onChange={(event) => setOwner(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="owner" className="form-check-label">
                  Owner
                </label>
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Demote User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};
