document.addEventListener("DOMContentLoaded", function() {
    console.log("BuzzyBee is ready to buzz! 🐝");
 
    const addProfile = document.getElementById("add-profile");
    const modal = document.getElementById("add-modal");
    const closeModal = document.querySelector(".close");
 
    // Show modal when add profile is clicked
    addProfile.addEventListener("click", function() {
        modal.style.display = "flex";
    });
 
    // Close modal when 'X' is clicked
    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });
 
    // Close modal when clicking outside of the content
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
 
    // Function to generate a random profile image
    function getRandomProfileImage() {
        const randomIndex = Math.floor(Math.random() * 5) + 1;
        return `/static/images/kid${randomIndex}.png`;
    }
 
    // Function to add new subaccount
    // addButton.addEventListener("click", function() {
    //     const nameInput = document.getElementById("sub-account-name");
    //     const name = nameInput.value.trim();
 
    //     if (name !== "") {
    //         const newProfile = document.createElement("div");
    //         newProfile.classList.add("profile");
    //         newProfile.onclick = function() { goToSubAccount(name); };
 
    //         const img = document.createElement("img");
    //         img.src = getRandomProfileImage();
    //         img.alt = name;
 
    //         const p = document.createElement("p");
    //         p.textContent = name;
 
    //         newProfile.appendChild(img);
    //         newProfile.appendChild(p);
    //         profilesContainer.insertBefore(newProfile, addProfile);
    
    //     } else {
    //         alert("Please enter a name.");
    //     }
    // });
 
    // Logout function
    function logout() {
        window.location.href = "{{ url_for('login_register.logout') }}";
    }
 
    // Navigate to subaccount function
    function goToSubAccount(subAccountId) {
        // Store selected profile in localStorage
        localStorage.setItem("selectedProfile", subAccountId);

        // Debugging: Check if subAccountId is captured correctly
        console.log("Navigating to subaccount for:", subAccountId);

        // Redirect to the correct subaccount login route
        window.location.href = `/Subaccount/Login/${encodeURIComponent(subAccountId)}`;
    }
});