
import { apiRequest } from "./api.js";

export async function registerUser(
  email,
  branch
){

  const data = await apiRequest(

    "/users/register",

    {
      method:"POST",

      body:JSON.stringify({
        email,
        branch
      })
    }
  );

  localStorage.setItem( "user_id", data.user.user_id ); localStorage.setItem( "user_email", data.user.email ); window.location.href = "home.html";

  return data;
}

export async function loginUser(
  email
){

  const data = await apiRequest(

    "/users/login",

    {
      method:"POST",

      body:JSON.stringify({
        email
      })
    }
  );

  localStorage.setItem(
    "token",
    data.access_token
  );

  localStorage.setItem(
    "user_id",
    data.user.user_id
  );

  window.location.href =
    "home.html";

  return data;
}

export function logout(){

  localStorage.removeItem(
    "token"
  );

  localStorage.removeItem(
    "user_id"
  );

  window.location.href =
    "index.html";
}
