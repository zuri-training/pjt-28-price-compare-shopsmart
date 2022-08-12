var show = true;
  
function showCategoryCheckboxes() {
    var checkboxes = 
        document.getElementById("checkBoxes");

    if (show) {
        checkboxes.style.display = "block";
        show = false;
    } else {
        checkboxes.style.display = "none";
        show = true;

    }
}

// show Brands Checkboxes

function showBrandsCheckboxes() {
    var checkboxes = 
        document.getElementById("brandsCheckBoxes");

    if (show) {
        checkboxes.style.display = "block";
        show = false;
    } else {
        checkboxes.style.display = "none";
        show = true;
        
    }
}