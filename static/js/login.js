document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll(".input-group input");

    inputs.forEach(input => {
        input.addEventListener("focus", function () {
            this.previousElementSibling.classList.add("ativo");
        });

        input.addEventListener("blur", function () {
            if (this.value === "") {
                this.previousElementSibling.classList.remove("ativo");
            }
        });
    });
});
