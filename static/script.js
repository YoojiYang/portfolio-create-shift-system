document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('start').addEventListener('click', () => {
        fetch('/run_script', {
            method: 'POST',
        })
        .then(response => response.text())
        .then(data => {
            alert(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    document.getElementById('close').addEventListener('click', () => {
        window.close();
    });
    });
