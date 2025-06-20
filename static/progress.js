function pollProgress(onComplete) {
    const fill = document.getElementById("fill");
    const status = document.getElementById("status");

    function check() {
        fetch("/progress")
            .then(res => res.json())
            .then(data => {
                fill.style.width = data.percent + "%";
                status.innerText = `Status: ${data.status} (${data.percent}%)`;
                if (data.status === "done") {
                    onComplete();
                } else {
                    setTimeout(check, 1000);
                }
            });
    }

    check();
}
