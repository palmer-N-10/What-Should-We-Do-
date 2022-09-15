console.log("script test");
const logins = document.querySelectorAll(".login");
const signups = document.querySelectorAll(".signup");
const page = document.querySelector("#page");
const tabs = document.querySelector(".tabs");
const ts = document.querySelectorAll(".tab-special")

function tab1() {
    page.style.marginLeft = "0";
    logins.forEach(login => login.classList.toggle("not-hidden"));
    signups.forEach(signup => signup.classList.toggle("not-hidden"));
}
function tab2() {
    page.style.marginLeft = "-100%";
    logins.forEach(login => login.classList.toggle("not-hidden"));
    signups.forEach(signup => signup.classList.toggle("not-hidden"));
}
