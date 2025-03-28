//Este script vai monitorar os inputs e ativar a animação das labels quando o usuário digitar ou focar no campo.
document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll(".input-group input");

    inputs.forEach((input) => {
        const label = input.previousElementSibling;

        input.addEventListener("focus", () => {
            label.classList.add("ativo");
        });

        input.addEventListener("blur", () => {
            if (input.value === "") {
                label.classList.remove("ativo");
            }
        });
    });
});
