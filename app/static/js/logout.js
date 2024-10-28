const divLogout = document.getElementById("divLogout");
const not = document.getElementById("not");
const yes = document.getElementById("yes");
const logout = document.getElementById("logout");
const body = document.getElementById("body");
function toggleLogout() {
  divLogout.classList.toggle("none");
  body.classList.toggle("blur");
  body.classList.toggle("hidden");
}

logout.addEventListener("click", toggleLogout);
not.addEventListener("click", toggleLogout);
