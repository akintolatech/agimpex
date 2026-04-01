document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".wishlist-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const url = this.dataset.url;
            const icon = this.querySelector("img");

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest",
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.is_favorite) {
                    button.classList.add("active");
                    if (icon) {
                        icon.src = "/static/img/faved.svg";
                    }
                } else {
                    button.classList.remove("active");
                    if (icon) {
                        icon.src = "/static/img/fave.svg";
                    }
                }

                const favCount = document.getElementById("favorite-count");
                if (favCount) {
                    favCount.textContent = data.favorite_count;
                }
            })
            .catch(error => console.error("Favorite error:", error));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});