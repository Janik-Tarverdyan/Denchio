var bars = document.getElementsByClassName('mobile-bars')[0];
var mobileMenu = document.getElementsByClassName('mobile-menu')[0];
bars.addEventListener('click', () => {
    if (mobileMenu.style.left == "-100%") {
        mobileMenu.style.left = "0";
  } else {
    mobileMenu.style.left = "-100%";
  }
    
})

var ul = mobileMenu.getElementsByTagName("ul");
for(let i=0; i<mobileMenu.querySelectorAll("li").length; i++){
    mobileMenu.querySelectorAll("li")[i].addEventListener('click', () => {
        mobileMenu.style.left = "-100%";
    })
}