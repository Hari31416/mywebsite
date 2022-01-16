"use strict";
const resizeBtn = document.getElementById("resize");
const reshapeBtn = document.getElementById("reshape");
const reformatBtn = document.getElementById("reformat");
const reshapeForm = document.getElementById("reshapeForm");
const resizeForm = document.getElementById("resizeForm");
const reformatForm = document.getElementById("reformatForm");

reshapeBtn.addEventListener("click", function () {
  reshapeForm.classList.toggle("d-none");
});

resizeBtn.addEventListener("click", function () {
  resizeForm.classList.toggle("d-none");
});

reformatBtn.addEventListener("click", function () {
  reformatForm.classList.toggle("d-none");
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();
