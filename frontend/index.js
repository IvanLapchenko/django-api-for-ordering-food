document.addEventListener("DOMContentLoaded", function () {
    const orderDataContainer = document.getElementById("orderDataContainer");
    const addButton = document.getElementById("addOrderField");
    const orderForm = document.getElementById("orderForm");

    function gatherFormData() {
        const pointId = document.getElementById("point_id").value;
        const orderId = document.getElementById("order_id").value;
        const orderItemInputs = document.querySelectorAll(".order");
        const orderItemValues = Array.from(orderItemInputs).map(input => input.value);

        const jsonData = {
            'order_id': orderId,
            'point_id': pointId,
            'order_items': orderItemValues
        };
        return jsonData;
    }

    addButton.addEventListener("click", function () {
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "order";
        newInput.classList.add("order");

        orderDataContainer.appendChild(newInput);
    });

    orderForm.addEventListener("submit", function ( event ) {
        event.preventDefault();
        const formData = gatherFormData();
        console.log(formData)
        fetch('http://localhost:8000/api/create_check/', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: {
             'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    })
});

