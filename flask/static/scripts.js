
function validateForm() {
    var imageInput = document.getElementById("image");
    var submitButton = document.getElementById("submit");

    if (imageInput.value == "") {
        submitButton.disabled = true;
        return false;
    } else {
        submitButton.disabled = false;
        submitButton.value = 'Generating...';
        submitButton.disabled = true;
// add event listener to image input element
        imageInput.addEventListener('change', function() {
            if (submitButton.value === 'Generating...') {
                submitButton.disabled = true;
            }
        });

        return true;
    }
}

function activateSubmit() {
    var submitButton = document.getElementById("submit");
    submitButton.disabled = false;
}





function previewImage() {
    var preview = document.getElementById('uploaded-image');
    var file = document.getElementById('image').files[0];
    if (!file.type.match('image.*')) {
        alert('Please select an image file');
        document.getElementById('image').value = '';
        preview.innerHTML = '';
        return;
    }
    if (file.size > 3 * 1024 * 1024) {
        alert('File size should be less than 3MB');
        document.getElementById('image').value = '';
        preview.innerHTML = '';
        return;
    }
    var reader = new FileReader();
    reader.onloadend = function() {
        var img = new Image();
        img.src = reader.result;
        img.onload = function() {
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            canvas.width = 420;
            canvas.height = 420;
            ctx.drawImage(img, 0, 0, 420, 420);
            preview.innerHTML = '<img src="' + canvas.toDataURL() + '" alt="Uploaded Image">';
        };
    };
    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}
document.getElementById('image').addEventListener('change', previewImage);





