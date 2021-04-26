var modal = document.getElementsByClassName("hidden");
var obj = document.getElementsByClassName("wrapper");
console.log(modal)
console.log(obj)

obj.addEventListener('click', function() {
  modal.style.display = "flex";
  console.log('Click-flex')
})

window.onclick = function(event) {
  if (modal.style.display == "flex") {
    modal.style.display = "none";
  }
}
